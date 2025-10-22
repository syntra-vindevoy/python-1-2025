def first_tree_plus_rest(opp_height:int, opp_width:int, tree_sqr_radius:int):
    # Bereken de kleinste driehoek die past, pak de breedte, en trek het af van de maximum breedte.
    
    # Deel de nieuwe breedte door de boom diameter
    #breedte - afstand eerste boom
    opp_height -= tree_sqr_radius
    return 0

def main():
    opp_height = 120
    opp_width = 210
    tree_sqr_radius = 8

    aantal_bomen = 0

    while opp_height > tree_sqr_radius & opp_height > tree_sqr_radius:
        aantal_bomen += first_tree_plus_rest(opp_height, opp_width, tree_sqr_radius)
        aantal_bomen += opp_width // tree_sqr_radius

    print(aantal_bomen)
    #HIER PROGRAMMEREN

if __name__ == "__main__":
    main()