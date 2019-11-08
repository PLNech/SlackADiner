import unidecode as unidecode


class Menu(object):
    def __init__(self, entrees=None, plats=None, garnitures=None, desserts=None):
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
        elif key == "dessertbar":  # DISCUSS: should we separate desserts?
            return self.desserts
        else:
            print("a Menu has no %s." % key)
            exit("-1")

    def __str__(self):
        return "Starters: %s\nMeals: %s\n Garnitures: %s\n Desserts: %s\n" % \
               tuple(["; ".join(it) for it, _, _ in self.composantes])

    @property
    def has_food(self):
        return any(len(it) for it in self.composantes)

    @property
    def composantes(self):
        return [self.entrees, self.plats, self.garnitures, self.desserts]


class Diner(Menu):
    def __init__(self, plats=None, desserts=None):
        super().__init__(plats=plats, desserts=desserts)

    @property
    def composantes(self):
        return [self.plats, self.desserts]

    def __str__(self):
        return "Meals: %s, desserts: %s." % (self.plats, self.desserts)
