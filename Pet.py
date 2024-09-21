#Problem 3

class Pets:
    species_lifespans = {
        'dog': 13,
        'cat': 15,
        'rabbit': 9
    }

    def __init__(self, name, age, species):
        self.name = name
        self.age = age
        self.species = species

    def age_in_human_years(self):
        if self.species == 'dog':
            return self.age * 7
        elif self.species == 'cat':
            return self.age * 6
        elif self.species == 'rabbit':
            return self.age * 8
        else:
            return self.age

    @classmethod
    def average_lifespan(cls, species):
        return cls.species_lifespans.get(species, "Unknown species")

Pets1 = Pets("Buddy", 3, "dog")
Pets2 = Pets("Whiskers", 4, "cat")
Pets3 = Pets("Thumper", 2, "rabbit")

print(f"{Pets1.name}'s age in human years is:", Pets1.age_in_human_years())
print(f"{Pets2.name}'s age in human years is:", Pets2.age_in_human_years())
print(f"{Pets3.name}'s age in human years is:", Pets3.age_in_human_years())

print(f"The average lifespan of a {Pets1.species} is:", Pets.average_lifespan(Pets1.species))
print(f"The average lifespan of a {Pets2.species} is:", Pets.average_lifespan(Pets2.species))
print(f"The average lifespan of a {Pets3.species} is:", Pets.average_lifespan(Pets3.species))