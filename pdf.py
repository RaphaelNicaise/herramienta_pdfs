import os
import humanize
from datetime import datetime as dt

class PDF:
    
    pdfs: list['PDF'] = []
    
    def __init__(self, path: str, content: str):
        self.__path = path
        self.__title = path.split('/')[-1].replace('.pdf', '')
        self.__content = content
        self.__space = humanize.naturalsize(os.stat(path).st_size)
        self.__last_changed = dt.fromtimestamp(os.stat(path).st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        self.__last_access = dt.fromtimestamp(os.stat(path).st_atime).strftime('%Y-%m-%d %H:%M:%S')
        
    def __str__(self):
        return f"{self.title} - {self.space} - {self.last_changed}"
    
    def __repr__(self):
        return f"{self.title}"



    @property
    def path(self):
        return self.__path
    
    @property
    def content(self):
        return self.__content
    
    @property
    def space(self):
        return self.__space
    
    @property
    def last_changed(self):
        return self.__last_changed
    
    @property
    def last_access(self):
        return self.__last_access
    
    @property
    def title(self):
        return self.__title
    
    def detailed_info(self):
        return f"""
        path = {self.path}
        space = {self.space}
        last_changed = {self.last_changed}
        last_access = {self.last_access}
        words = {len(self.content.split())}
        """

    @classmethod
    def print_pdfs(cls):
        print(cls.pdfs)
        
    @classmethod
    def exists(cls, path):
        for pdf in cls.pdfs:
            if pdf.path == path:
                return True
        return False