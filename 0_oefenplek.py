# Upper has no problem with special letters and when there are things other then letters.
for word in ["abc","123","a23","1-c","1ùc"]:
    print(word.upper())

















# class Spel:
#     # PROPERTIES
#     bord: list[list[str]]
#
#     #CONSTRUCTOR
#     def __innit__(self):
#         self.bord = [[]*8]*8
#
#     #METHODS
#     # def move(speler: Speler, piece: Piece, new_pos: str):
#     #     if Piece.color == Speler.color
#     #     piece.position = new_pos
#
#
# class Speler:
#     # PROPERTIES
#     clicked_tile: str
#     input_console: str
#
#     # CONSTRUCTOR
#     def __init__(self):
#         self.clicked_tile = ""
#         self.input_console = ""
#
# class Piece:
#     # PROPERTIES
#
#     # CONSTRUCTOR
#     def __init__(self):
#         self.tile = None
#         self.color = None
#
# def spel_gang(speler1: Speler, speler2: Speler):  # speler 1 = wit, speler2 = zwart
#     schaakmat = False
#     spelletje = Spel().__new__(Spel)
#     while schaakmat == False:
#         spelletje.move(speler1.clicked_tile, input(str))  # ("G4", "G6")
#         #speler1.move(speler1.clicked_tile, input(str))  # ("G4", "G6")
#         #speler2.move(speler2.clicked_tile, input(str))  # ("B4", "D6")
#
#         if True:
#             schaakmat = True