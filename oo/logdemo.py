import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO) #aanpassen naar logging.DEBUG als je DEBUGT - minimum naar file en minimum naar scherm, mss nog naar emailer loggen voor fatals en criticals

handler = logging.StreamHandler() #rotating streamhandler - best roteren, smijt automatisch buiten.
#één groot probleem met standaard logging, multithreading. kan er voro zorgen als 2 dingen tegelijk willen wegschrijven, met multiprocessing moet je met een andere manier gaan loggen, loggen naar een queue
#logoere als alternatief, heeft ook nadelen
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

handler.setFormatter(formatter)
logger.addHandler(handler)

class MyClass:
    def __init__(self):
        logger.debug("MyClass.__init__")
    def my_method(self):
        logger.debug("MyClass.my_method")

def main():
    my_class = MyClass()
    my_class.my_method()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.fatal(e) #alle info schrijven, die je kan helpen bij te zoeken of het wekrt