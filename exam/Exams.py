import os
import re
import logging
from pathlib import *
from shutil import copyfile

class Exams:

    def __init__(self, source, target, students):
        self.source = source
        self.target = target
        self.students = students

    def files(self):
        for root, dirs,_ in os.walk(self.source):
            for dir in dirs:
                self.process_file(Path(root, dir))        

    def process_file(self, path):
        result = re.match(r"(\w{9}) - (.*)",path.stem)
        if result:
            id = result.group(1)
            if self.students.get(id):
                marker = self.students[id]['Marker']
                self.move_file(path, marker)
            else:
                logging.warning(f"Student '{id}' not found!")

    def move_file(self, path, marker):
        new = Path(self.target, marker, path.parent, path.name)
        new.mkdir(parents=True, exist_ok=True)
        for file in path.iterdir():
            p = Path(new, file.name)
            copyfile(file,p)
