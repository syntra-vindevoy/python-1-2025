from datetime import date
#from oo.basket import Basket   # In comment to avoid circular reference

#Class = a blueprint            -> A blueprint of a house
#Object = an executed blueprint -> The actual built house

class Orange:
    # PROPERTIES
    weight: float   # = 0   kan, maar misschien beter in __init__(self)?
    orchard: str
    date_picked: date

    # basket: Basket  # Basket is mutable en dus enkel een link naar de data.   # In comment to avoid circular reference