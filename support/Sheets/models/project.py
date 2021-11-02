from .django_class import DjangoBase
from .editor import Editor
from pathlib import Path
from time import sleep
from .support import *
import io


class DjangoProject(DjangoBase):
    def __init__(self, base_path: str, project: str):
        self.base_path = self.adapt_path(base_path)
        self.project = self.adapt_path(project)
        self.path = f'{self.base_path}/{self.project}'
        assert_folder_existence(self.path)
            
    def adapt_urls_py(self):
        editor = Editor(self.path, 'urls.py')
        nr = editor.insert_code('from django.urls', 'from django.conf import settings\nfrom django.conf.urls.static import static')  # new_reading
        nr = editor.insert_code(']\n', '\nurlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\nurlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)', nr)
        nr = editor.add_in_line('from django.urls', ', include', nr)
        editor.update(nr)
    
    def insert_important_comments(self):
        editor = Editor(self.path, 'settings.py')
        inserts = [("DEFAULT_AUTO_FIELD", "\n# My configurations"),
                   ("INSTALLED_APPS", '    # Django apps'),
                   ("    'django.contrib.staticfiles'", '    # My apps\n    # Others apps'),
        ]
        for index_, change in enumerate(inserts):
            if index_ == 0:
                nr = editor.insert_code(change[0], change[1])
            else:
                nr = editor.insert_code(change[0], change[1], nr)
        if len(inserts) > 0:
            editor.update(nr)
        
    def _settings_replaces(self):
        replaces = [
            ("        'DIRS': [],", "        'DIRS': [Path(BASE_DIR, 'Support/Layouts/Templates')],"),
            ("LANGUAGE_CODE = 'en-us'", "LANGUAGE_CODE = 'pt-br'"),
            ("TIME_ZONE = 'UTC'", "TIME_ZONE = 'America/Sao_Paulo'"),
            (f"{sp(12)}],", f"{sp(12)}],\n{sp(12)}'libraries':"+" {\n"+ f"{sp(12)}'filters': 'Support.TemplatesTags',\n{sp(12)}"+"}\n"),
            #("", ""),
        ]
        return replaces
        
    def _settings_inserts(self):
        inserts = [
            ("# My configurations", "\nSTATICFILES_DIRS = [Path(BASE_DIR, 'Support/Layouts/Static')]\nSTATIC_ROOT = Path('static')\n\nMEDIA_ROOT = Path(BASE_DIR,'Support/Layouts/Media')\nMEDIA_URL = '/media/'\n\nMESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'\nSESSION_COOKIE_AGE = 60*60*24*7\nACCOUNT_SESSION_REMEMBER = True\n"),
            #("", ""),
        ]
        return inserts
    
    def adapt_settings(self):
        editor = Editor(self.path, 'settings.py')
        replaces = self._settings_replaces()
        inserts = self._settings_inserts()
        for index_, change in enumerate(replaces):
            if index_ == 0:
                nr = editor.replace_code(change[0], change[1])
            else:
                nr = editor.replace_code(change[0], change[1], nr)
        if len(replaces) > 0:
            editor.update(nr)
        for index_, change in enumerate(inserts):
            if index_ == 0:
                nr = editor.insert_code(change[0], change[1])
            else:
                nr = editor.insert_code(change[0], change[1], nr)
        if len(inserts) > 0:
            editor.update(nr)
            
            

    