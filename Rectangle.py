#Problem 1

class Rectangle:
    def __init__(self, length, width):
        self.length = length
        self.width = width

    def calculate_area(self):
        return self.length * self.width

rect = Rectangle(5, 3)

print("The area of the rectangle is:", rect.calculate_area())