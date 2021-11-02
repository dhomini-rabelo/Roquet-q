from models.eraser import delete_comments_by_folder
from for_project import project_name, bp
from models.app import DjangoApp
from time import sleep

app_name = 'asks'
app = DjangoApp(bp, app_name)

#* CRIAR TESTES
# app.create_py_folder(f'Support/tests/{app_name}')
# tests = ['models', 'views', 'forms']
# for test in tests:
#     app.create_test_archive(f'{app_name}/{test}')

#* CRIAR FORMS
# app.add_form('Pessoa')

#* REGISTRAR ADMIN
# app.register_admin('Gente')

#* REGISTRAR VIEW
# app.register_view('form', logged=False)

#* APÓS CRIAÇÃO
# sleep(1)
delete_comments_by_folder(bp, app_name)
# app.create_templates_folder(app_name)
# sleep(1)
app.create_url_archive()
# sleep(1)
# app.create_forms_archive()
app.import_for_model()
app.register_app(project_name)
app.config_app()
