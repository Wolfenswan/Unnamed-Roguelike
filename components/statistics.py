from functools import wraps


def statistics_updater(entry, value_idx=1, substract=False):
    """
    This decorator allows to track statistic changes on functions manipulating a single value (e.g. Fighter.take_damage())
    """
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            ent = args[0].owner
            value = args[value_idx] if not substract else -args[value_idx]
            ent.statistics.update_all(entry, value)
            return result
        return wrapper
    return decorator


class Statistics:
    """
    Statistics contains three dictionaries: turn, level, game.
    All dictionaries contain various key:value pairs referencing in-game attributes.
    The values of these pairs are updated as the game progresses.
    """
    def __init__(self):
        # These lists dictate the empty state for each value
        self.int_values = ['hp_change', 'sta_change', 'dmg_done']
        self.list_values = ['killed']
        self.turn, self.level, self.game = {}, {}, {}  # Initializes empty dictionaries
        for dic in [self.turn, self.level, self.game]: # Then set each key:value pair to the respective empty-state
            self.reset(dic) # Reset

    # All @properties are just convenient ways to directly get and set the current turn statistics
    @property
    def hp_change(self):
        return self.turn['hp_change']

    @hp_change.setter
    def hp_change(self, value):
        self.update_all('hp_change', value)

    @property
    def sta_change(self):
        return self.turn['sta_change']

    @sta_change.setter
    def sta_change(self, value):
        self.update_all('sta_change', value)

    @property
    def dmg_done(self):
        return self.turn['dmg_done']

    @dmg_done.setter
    def dmg_done(self, value):
        self.update_all('dmg_done', value)

    @property
    def killed(self):
        if isinstance(self.turn['killed'], int):
            self.turn['killed'] = []
        return self.turn['killed']

    @killed.setter
    def killed(self, value):
        self.update_all('killed', value)

    def update_all(self, key, value):
        """ Statistics.update_all() updates the respective key:value pair in each dictionary """
        for dic in [self.turn, self.level, self.game]:
            if isinstance(value, float):
                value = round(value)
            dic[key] += value

    def reset(self, dic):
        """ Statistics.reset() sets all values of the corresponding dict to their respective empty-state. """
        for key in self.int_values:
            dic[key] = 0
        for key in self.list_values:
            dic[key] = []

    def reset_turn(self):
        self.reset(self.turn)