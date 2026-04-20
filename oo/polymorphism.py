

class Animal:
    def make_sound(self):                            # class where this is called
        raise NotImplementedError(f"POLYMORPHISM: Class {self.__class__.__name__} must override this methode")
        # Used as standerd since this class is not used for making objects, but for inheritence. (this is just handy)

class Dog(Animal):
    def make_sound(self):
        print("Woof")

class Cat(Animal):
    pass


def main():
    pass

if __name__ == "__main__":
    main()