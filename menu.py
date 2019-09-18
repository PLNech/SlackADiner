class Menu(object):
    def __init__(self, meals=None, desserts=None):
        if meals is None:
            meals = []
        self.meals = meals

        if desserts is None:
            desserts = []
        self.desserts = desserts

    def __getitem__(self, item):
        if item is "meals":
            return self.meals
        elif item is "desserts":
            return self.desserts

    def __str__(self):
        return "Meals: %s, desserts: %s." % (self.meals, self.desserts)

    @property
    def has_food(self):
        return len(self.meals) or len(self.desserts)
