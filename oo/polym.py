
class Animal:
    sound: str = None

    def make_sound(self):
        raise NotImplementedError(f"POLYMORPHISM: {self.__class__.__name__} must override make_sound()")

class Dog(Animal):
    sound = "Woof!"

    def make_sound(self):
        if self.sound is None:
            raise NotImplementedError("Dog has no sound set")

        print(self.sound)

class Cat(Animal):
    pass


d = Dog()
d.make_sound()

c = Cat()
c.make_sound()
