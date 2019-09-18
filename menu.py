class Menu(object):
    def __init__(self, meals=None, deserts=None):
        if meals is None:
            meals = []
        self.meals = meals

        if deserts is None:
            deserts = []
        self.deserts = deserts

    def __getitem__(self, item):
        if item is "meals":
            return self.meals
        elif item is "deserts":
            return self.deserts

    def __str__(self):
        return "Meals: %s, Deserts: %s." % (self.meals, self.deserts)

    @property
    def has_food(self):
        return len(self.meals) or len(self.deserts)
