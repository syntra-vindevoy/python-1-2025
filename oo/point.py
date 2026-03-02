class Point:
    # PROPERTIES
    x: int = 0
    y: int = 0

    # GETTERS/SETTERS? #Not yet talked about

    # CONSTRUCTOR
    def __init__(self, *, x, y): # Every parameter after the * is required to be specified when instancing an object.
        self.x = x
        self.y = y

    # METHODES
    # This is a utility methode. Always "return self" as return value.
    def reset(self):    # Self means the object created from a class.
        self.x = 0
        self.y = 0

        return self

    def print(self):
        print(self.x, self.y)
        return self











# From here to +30 lines (22-51) writen when there was no constructor.
# import yaml
# "typing" is a method to set the type when you equate it to a function result where the value could be changed.
# An error gives the hint.
# toto: int# = None
#
# p1 = Point()
# p2 = Point()
#
# p1.x = 10
# p1.y = 20
#
# print(p1.x, p1.y)
# Next line error happens when the attribute is not mentioned in the class, and has no value.
#print(p2.x, p2.y)   # Attribute error. This is executable, but the value is never set, nor a type is given.

# Standerd setting class used with a lot of programs
# class Settings:
#     v = 0
#     t = 0
#
#     def init(self):
#         settings: dict = {}
#
#         def init(self):
#             with open("settings.yaml", "r") as f:
#                 self.settings = yaml.safe_load(f)
#
#         def get_user(self):
#             return