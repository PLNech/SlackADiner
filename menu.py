import unidecode as unidecode


class Menu(object):
    def __init__(self, entrees=None, plats=None, garnitures=None, desserts=None, dessertbar=None):
        if entrees is None:
            entrees = []
        self.entrees = entrees

        if plats is None:
            plats = []
        self.plats = plats

        if garnitures is None:
            garnitures = []
        self.garnitures = garnitures

        if desserts is None:
            desserts = []
        self.desserts = desserts

        if dessertbar is None:
            dessertbar = []
        self.dessertbar = dessertbar

    def __getitem__(self, key):
        key = unidecode.unidecode(key).lower().replace("'", "")
        if key == "entrees":
            return self.entrees
        elif key == "plats":
            return self.plats
        elif key == "garnitures":
            return self.garnitures
        elif key == "desserts":
            return self.desserts
        elif key == "dessertbar":
            return self.dessertbar
        else:
            print("a Menu has no %s." % key)
            exit("-1")

    def __str__(self):
        sep = ", "
        return "Starters: %s\nMeals: %s\n Garnitures: %s\n Desserts: %s\n Dessert'Bar: %s." % \
               (sep.join(self.entrees), sep.join(self.plats), sep.join(self.garnitures), sep.join(self.desserts),
                sep.join(self.dessertbar))

    @property
    def has_food(self):
        return len(self.plats) or len(self.desserts)


class Diner(Menu):
    def __init__(self, plats=None, desserts=None):
        super().__init__(plats=plats, desserts=desserts)

    def __str__(self):
        return "Meals: %s, desserts: %s." % (self.plats, self.desserts)

    @property
    def has_food(self):
        return len(self.plats) or len(self.desserts)
