from .django_class import DjangoBase
from .editor import Editor
from pathlib import Path
from .support import *
import io


class DjangoApp(DjangoBase):
    def __init__(self, base_path: str, app: str):
        self.base_path = self.adapt_path(base_path)
        self.app = self.adapt_path(app)
        self.path = f'{self.base_path}/{self.app}'
        assert_folder_existence(self.path)
            
    def create_py_folder(self, folder_path):
        path = f'{self.base_path}/{folder_path}'
        Path(path).mkdir()
        sleep(0.5)
        with io.open(f'{path}/__init__.py', 'w') as file:
            pass
        
    def create_py_archive(self, archive_path):
        path = f'{self.path}/{self.adapt_pyname(archive_path)}'
        with io.open(path, 'w') as file:
            pass
        
    def create_archive(self, archive_path):
        path = f'{self.base_path}/{archive_path}'
        with io.open(path, 'w') as file:
            pass

    def create_templates_folder(self, name_space: str):
        try: 
            Path(f'{self.path}/templates').mkdir()
            sleep(0.3)
            Path(f'{self.path}/templates/{name_space}').mkdir()
            self.create_archive(f'{self.app}/templates/descriptions.txt')
            response(f'pasta templates foi criada no app {self.app}')
        except FileExistsError:
            response(f'a pasta templates já existe no app {self.app}')
            
    def create_test_archive(self, test_name: str):
        name = f'test_{self.adapt_pyname(test_name)}'
        with io.open(f'{self.base_path}/Support/tests/{name}', 'w', encoding='utf-8') as arc:
            arc.write('from django.test import TestCase\n')
            response(f'Criando {name} na pasta tests')
            
    def create_url_archive(self):
        with io.open(f'{self.path}/urls.py', 'w', encoding='utf-8') as arc:
            arc.write('from django.urls import path\nfrom .views import *\n')
            arc.write(f'\nurlpatterns = [\n{sp(4)}path(),\n]\n')
            response(f'arquivo urls.py criado no app {self.app}')
    
    def create_forms_archive(self):
        with io.open(f'{self.base_path}/Support/forms/{self.app}.py', 'w', encoding='utf-8') as arc:
            arc.write('from django.forms import ModelForm, ValidationError\n')
            arc.write(f'from {self.app}.models import *\n')
            response(f'arquivo forms.py criado no app {self.app}')

    def add_form(self, model_name: str):
        path = f'{self.base_path}/Support/forms/{self.app}.py'
        assert_file_existence(path)
        with io.open(path, 'a', encoding='utf-8') as arc:
            arc.write(f'\n\nclass {model_name}Form(ModelForm):\n')
            arc.write(f"    class Meta:\n      fields = '__all__'\n")
            arc.write(f"      model = {model_name}\n")
            response(f'criando form para {model_name}')
            
    def import_for_model(self):
        editor = Editor(self.path, 'models.py')
        current_import = 'from django.db import models'
        new_import = 'from django.db.models import (Model, CharField, DateTimeField, TextField, EmailField, ForeignKey, PositiveIntegerField, ImageField, RESTRICT, DecimalField, DateField, BooleanField)'
        nr = editor.replace_code(current_import, new_import) # new_reading
        editor.update(nr)
        response(f'import do model foi editado')
        
    def config_app(self):
        editor = Editor(self.path, '__init__.py')
        new_import = f"from django.apps import AppConfig\n\nclass {self.app.title()}Config(AppConfig):\n      default_auto_field = 'django.db.models.BigAutoField'\n    name = '{self.app}'"
        nr = editor.insert_code(0, new_import) # new_reading
        editor.update(nr)

    def register_app(self, project_name: str):
        editor  = Editor(self.base_path, f'{project_name}/settings.py')
        nr = editor.insert_code('    # My apps', f"    '{self.app}.{self.app.title()}Config',")
        editor.update(nr)

    def register_admin(self, model_name: str):
        editor  = Editor(self.path, f'admin.py')
        nr = editor.read(editor.path)
        model = model_name.title()
        nr.append(f"\n\n@admin.register({model})\nclass {model}Admin(admin.ModelAdmin):\n    list_display = '',\n    list_display_links = '',")
        editor.update(nr)
        
    def register_view(self, name_view, logged=True):
        editor  = Editor(self.path, f'views.py')
        nr = editor.read(editor.path)
        log = '@login_required\n' if logged else ''
        nr.append(f"{log}def {name_view}(request):\n    context = dict()\n    return render(request, '{self.app}/{name_view}.html', context)\n")
        editor.update(nr)
        
    def create_abstract_user_model(self):
        editor = Editor(self.path, 'models.py')
        nr = editor.read(editor.path)
        au_class = """\nclass User(AbstractUser):\n    photo = ImageField('Foto de perfil', upload_to='images/%Y/%m/%d/%M/%f', null=True, blank=True, default='images/default.jpg')\n\n    def __str__(self):\n        return self.username\n\n    @mark_safe\n    def icon(self):\n         return f'<a href="/media/{self.photo}" target="_blank"><img src="/media/{self.photo}" style="width: 35px; height: 25px;"></a>'\n"""
        nr.append(au_class)
        nr.insert(1, "from django.contrib.auth.models import AbstractUser\nfrom django.utils.safestring import mark_safe\nfrom django.utils import timezone\n")
        editor.update(nr)

    def register_abstract_user(self):
        editor  = Editor(self.base_path, f'settings.py')
        nr = editor.read(editor.path)
        nr.append(f"\nAUTH_USER_MODEL = 'accounts.User'\nACCOUNT_SESSION_REMEMBER = True\nACCOUNT_UNIQUE_EMAIL = True\n")
        editor.update(nr)
            
    