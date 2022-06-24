class Calculator ():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def addition (self):
        return f"{self.x} + {self.y} = {self.x + self.y}"
    def subtraction (self):
        return f"{self.x} - {self.y} = {self.x - self.y}"
    def multiplication (self):
        return f"{self.x} * {self.y} = {self.x * self.y}"
    def division (self):
        if self.y != 0:
            return f"{self.x} / {self.y} = {self.x / self.y}"
        else:
            return "Division by zero isn't allowed!"
    def exponentiation (self):
        return f"{self.x}^{self.y} = {self.x ** self.y}"



if __name__ == "__main__":
    while True:
        x = int (input ("Please enter first number: "))
        sign = input ("Please enter action sign: ")
        y = int (input ("Please enter second number: "))
        if sign != '0':
            if sign == '+':
                print (Calculator (x, y).addition ())
                continue
            elif sign == '-':
                print (Calculator (x, y).subtraction ())
                continue
            elif sign == '/':
                print (Calculator (x, y).division ())
                continue
            elif sign == '*':
                print (Calculator (x, y).multiplication ())
                continue
            elif sign == '^' or '**':
                print (Calculator (x, y).exponentiation ())
            else:
                print (f"Probably '{sign}' isn't an action sign")
                continue
        else:
            break


