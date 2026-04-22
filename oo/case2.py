from datetime import datetime

class Note:
    def __init__(self, memo:str, tags:list[str]):
        self.memo: str = memo
        self.tags: list[str] = tags
        self.__creation_date: datetime = datetime.now()

    def match(self,criteria:str):
        pass

    def __repr__(self):
        return f"#{self.id} - {self.memo} ({self.__creation_date})"

class Notebook:
    __current_note_id: int = 0 # als je hem hier zet wordt het aangepast voor beide notebooks

    def __init__(self):
        self.__notes: list[Note] = []
    @property
    def number_of_notes(self):
        return len(self.__notes)
    
    def search(self, criteria):
        pass

    #def new_note(self, memo:str, tags: list[str]=None):
     #   if tags is None:
      #      tags = []
       # note = Note(memo,tags)
        #self.__notes.append(note)

    def add_note(self, note:Note):
        Notebook.__current_note_id += 1
        note.id = self.__current_note_id
        self.__notes.append(note)

    def modify_memo(self, note_id:int, memo:str):
        pass

    def modify_tags(self, note_id:int, tags:str):
        pass
    def __repr__(self):
        return f"Notebook with {len(self.__notes)} notes"

def main():
    notebook = Notebook()

    note1= Note("Hello World", ["English"])
    notebook.add_note(note1)
    #notebook.new_note("Bonjour le monde",["French"])

    print(notebook.__dict__)
    print(notebook)
    print(note1)

    notebook2 = Notebook()
    note2 = Note("hallo wereld",["Dutch"])
    notebook2.add_note(note2)
    notebook2.add_note(note1)
    print(notebook2.__dict__)

    print(note2.__dict__)

if __name__ == "__main__":
    main()