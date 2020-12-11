maxIntensity = 255
class Pixel:
    
    def __init__(self, r=0, g=0, b=0):
        self.r = int(self.limit(r))
        self.g = int(self.limit(g))
        self.b = int(self.limit(b))

    def toTuple(self):
        return (self.r, self.b, self.g)
    
    @staticmethod
    def limit(value):
        return min(value, maxIntensity)

    def __add__(self, other):
        if isinstance(other, Pixel):
            return Pixel(self.r + other.r, self.g + other.g, self.b + other.b)
        elif isinstance(other, tuple):
            if len(other) < 3:
                raise TypeError("tuple too smol u fuck")
            return Pixel(self.r + other[0], self.g + other[1], self.b + other[2])
        else:
            raise TypeError("incompatible types: {} and {}".format(type(self), type(other)))

    def __mul__(self, other):
        if isinstance(other, (float, int)):
            return Pixel(self.r * other, self.g * other, self.b * other)


    def __str__(self):
        return f'({self.r}, {self.g}, {self.b})'
    
    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        if isinstance(other, Pixel):
            return self.r == other.r and  self.g == other.g and self.b == other.b
        elif isinstance(other, tuple):
            if len(other) < 3:
                raise TypeError("tuple too smol u fuck")
            return self.r == other[0] and self.g == other[1] and self.b == other[2]
        else:
            raise TypeError("incompatible types: {} and {}".format(type(self), type(other)))

    def __le__(self, other):
        if isinstance(other, Pixel):
            return self.r <= other.r and  self.g <= other.g and self.b <= other.b
        elif isinstance(other, tuple):
            if len(other) < 3:
                raise TypeError("tuple too smol u fuck")
            return self.r <= other[0] and self.g <= other[1] and self.b <= other[2]
        else:
            raise TypeError("incompatible types: {} and {}".format(type(self), type(other)))

if __name__ == "__main__":
    test = Pixel(1,2,3)
    array = [Pixel()] * 31
    
    array[1] += (12, 256, 13)
    print(array)