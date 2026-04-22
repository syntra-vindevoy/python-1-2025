

class Settings:

        def __init__(self):
            self.theme = "light"
            self.language = "en"

        @classmethod #als je een methode wilt op niveau van de class en niet op methode van de instantie
        def load(cls):
            cls.theme = "dark"
s = Settings
print(s.theme)
Settings().load()
print(Settings.theme)