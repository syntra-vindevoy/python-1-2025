from datetime import date

class Note:
    def __init__(self, memo:str = "", tags: list[str] = None):
        self.memo = memo
        self.__creation_date = date(0,0,0)
        self.tags = tags

    def match(self, criteria: str):
        pass

    def __repr__(self):
        return f"{self.id} - {self.memo} ({self.__creation_date})"

class Notebook:
    __current_note_id: int = 0

    def __init__(self):
        self.__notes: list[Note] = []
        # self.__current_note_id = 0

    def search(self, criteria: str):
        pass

    def add_note(self, note: Note):
        self.__current_note_id += 1
        note.id = self.__current_note_id

        self.__notes.append(note)

    def modify_memo(self, memo: str):
        pass

    def modify_tags(self, tags: list[Note] = None):
        if tags is None:
            tags = []

    def __repr__(self):
        return f"Notebook with {len(self.__notes)} notes"

def main():
    notebook = Notebook()

    note1 = Note(memo="Hello world", tags=["English"])
    notebook.add_note(note1)

    print(note1)

    notebook2 = Notebook()
    note2 = Note(memo="Hallo wereld", tags=["Dutch"])
    notebook2.add_note(note2)

    pass

if __name__ == '__main__':
    main()