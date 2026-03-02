from datetime import datetime


class Note:
    def __init__(self, memo:str, tags:list[str]):
        self.id: int = 0
        self.memo: str = memo
        self.tags: list[str] = tags

        self.__creation_date: datetime = datetime.now()

    def match(self, criteria: str):
        pass

    def __repr__(self):
        return f"#{self.id} - {self.memo} ({self.__creation_date})"


class Notebook:
    __current_note_id: int = 0

    def __init__(self):
        self.__notes: list[Note] = []

    @property
    def number_of_notes(self):
        return len(self.__notes)

    def search(self, criteria: str):
        pass

    def add_note(self, note: Note):
        Notebook.__current_note_id += 1
        note.id = self.__current_note_id

        self.__notes.append(note)


    def modify_memo(self, note_id: int, memo: str):
        pass

    def modify_tags(self, note_id: int, tags: str):
        pass

    def __repr__(self):
        return f"Notebook with {len(self.__notes)} notes"


def main():
    notebook = Notebook()

    note1 = Note("Hello world", ["english"])
    notebook.add_note(note1)

    print(note1)

    notebook2 = Notebook()
    note2 = Note("Hallo", ["dutch"])
    notebook2.add_note(note2)
    notebook2.add_note(note1)

    print(note2)

    Notebook.add_note()
if __name__ == "__main__":
    main()