from functools import wraps


class Statistics:
    def __init__(self):
        self.int_values = ['hp_change', 'sta_change', 'dmg_done']
        self.list_values = ['killed']
        self.turn, self.level, self.game = {}, {}, {}
        for dic in [self.turn, self.level, self.game]:
            self.reset(dic)

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
        for dic in [self.turn, self.level, self.game]:
            if isinstance(value, int):
                value = round(value)
            dic[key] += value

    def reset(self, dic):
        for key in self.int_values:
            dic[key] = 0
        for key in self.list_values:
            dic[key] = []

    def reset_turn(self):
        self.reset(self.turn)


def statistics_updater(entry, value_idx=1, substract=False):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            ent = args[0].owner
            value = args[value_idx] if not substract else -args[value_idx]
            ent.statistics.update_all(entry,value)
            result = function(*args, **kwargs)
            return result

        return wrapper
    return decorator