from models.eraser import *
from models.project import *
from models.editor import Editor
from time import sleep

bp = r'C:\Users\G-fire\OneDrive\Documentos\GITHUB\DJANGO\Live-Questions\project' # base_path
project_name = 'QUESTIONS'
project = DjangoProject(bp, project_name)


#* APÓS CRIAÇÃO
# delete_comments_by_folder(bp, project_name)
# sleep(1)
# project.adapt_urls_py()
# sleep(1)
# project.insert_important_comments()
# sleep(1)
# project.adapt_settings()