from typing import Optional as _Optional
from threading import Thread as _Thread


db_path = r"C:\Users\DANIEL\Desktop\rqaw\Documentos\Dev\Python\SelfCopy\brain.db"


otuple_str = _Optional[tuple[str]]
oint = _Optional[int]



class mainThread(object):
    def __init__(self) -> None:
        self.thread = _Thread(target=self.run, args=())
    
    def start(self):
        self.thread.daemon = True
        self.thread.start()
        
    def run(self):
        ...
    
    def stop(self):
        ...
