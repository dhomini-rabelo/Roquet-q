from pathlib import Path
from time import sleep
from .django_class import DjangoBase
from .support import *
import io


class Eraser(DjangoBase):
    def __init__(self, path: str):
        self.path = self.adapt_path(path)
        assert_file_existence(self.path)
        
    def one_line(self):
        reading = self.read(self.path)
        dels = []
        for line in reading:
            if line != '\n' and (not check_null(line.strip())) and line.strip()[0] == '#':
                dels.append(line)
        for disponsable_line in dels:
            reading.remove(disponsable_line)
        return reading
    
    def initial_lines(self):
        reading = self.read(self.path)
        if (not check_null(reading)) and (reading[0][:3] == '"""'):
            for index_, line in enumerate(reading[1:]):
                if '"""' in line:
                    end_comment = index_
                    reading = reading[end_comment+2: ]
                    break
        return reading 
                    
    
    def construct(self, new_reading: list):
        if check_null(new_reading):
            return
        with io.open(self.path, mode='w', encoding='utf-8') as code_file:
            start = 1 if new_reading[0] == '\n' else 0
            for line in new_reading[start:]:
                code_file.write(line)
            

def delete_comments_by_arquive(path: str):
    rubber = Eraser(path)
    reader1 = rubber.one_line()
    rubber.construct(reader1)
    sleep(0.3)
    reader2 = rubber.initial_lines()
    rubber.construct(reader2)


def delete_comments_by_folder(base_path: str, folder_name: str):
    wp = Path(f'{base_path}/{folder_name}') # work path
    if wp.exists():
        for item in wp.iterdir():
            if item.suffix == '.py':
                response(f'Apagando comentários {item.name}')
                delete_comments_by_arquive(str(item))
