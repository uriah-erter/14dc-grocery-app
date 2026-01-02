import constants

class GroceryItem:
    def __init__(self):
        self._name = constants.NAME_DEFAULT
        self._store = constants.STORE_DEFAULT
        self._cost = constants.COST_DEFAULT
        self._amount = constants.AMOUNT_DEFAULT
        self._priority = constants.PRIORITY_DEFAULT
        self._buy = constants.BUY_DEFAULT
        self._id = constants.ID_DEFAULT

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string value")
        self._name = value

    @property
    def store(self):
        return self._store

    @store.setter
    def store(self, value):
        if not isinstance(value, str):
            raise ValueError("Store must be a string value")
        self._store = value

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Cost must be an int or a float value")
        self._cost = int(value)

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        if not isinstance(value, int):
            raise ValueError("Amount must be an int value")
        self._amount = value

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, value):
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        if not value:
            pass

        if not isinstance(value, int):
            raise ValueError(f"Priority must be an int value, {value}")
            
        if p_min <= value <= p_max:
            pass

        else:
            raise ValueError(f"Priority must be an int value between {p_min} and {p_max}")

        self._priority = value
        
    @property
    def buy(self):
        return self._buy

    @buy.setter
    def buy(self, value):
        if not isinstance(value, bool):
            raise ValueError("Name must be a boolean value")
        self._buy = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be a UUID")
        self._id = value
