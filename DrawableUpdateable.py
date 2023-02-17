import abc

class Updateables(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def Update(self, deltaTime):
        pass

class Drawable(metaclass=abc.ABCMeta):
    @abc.abstractclassmethod
    def Draw(self):
        pass