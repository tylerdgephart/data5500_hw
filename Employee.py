#Problem 2

class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def raise_salary(self, percentage):
        self.salary += self.salary * (percentage / 100)

employee = Employee("John", 5000)

employee.raise_salary(10)
print(f"{employee.name}'s updated salary is:", employee.salary)