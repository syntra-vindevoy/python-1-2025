import math

def solve(hoogte_x, hoogte_z, breedte_y, hoogte_boom, breedte_boom):
    trees = math.floor(min(hoogte_x, hoogte_z) / hoogte_boom) * math.floor(breedte_y / breedte_boom)
    trees += driehoek_calc(max(hoogte_x, hoogte_z) - min(hoogte_x, hoogte_z), breedte_y, hoogte_boom, breedte_boom)
    print(f"Trees: {trees}")

def driehoek_calc (x, y, hb, bb):
    #s = de hoogte van de kleine driehoek waar geen bomen in passen
    math.acos()
    driehoek_hoek_graden = x, hoek, y
    if s == bb:
        y -= onbruikbare_ruimte_breedte
        return math.floor(y / hb) + driehoek_calc(x - hb, y, hb, bb)

def main():
    print(solve(hoogte_x=220, hoogte_z=120, breedte_y=90, hoogte_boom=8, breedte_boom=8))
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    main()