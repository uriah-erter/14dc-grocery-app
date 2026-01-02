"""
grocery_item.py

Defines the GroceryItem model used by the Grocery List application.

A GroceryItem stores one entry in the grocery list and validates each field
through property setters.
"""

import constants


class GroceryItem:
    """
    Data model for a single grocery list item.

    Attributes are stored internally using private variables (e.g. _name) and
    exposed/validated using @property getters/setters.
    """

    def __init__(self) -> None:
        """
        Initialize a new GroceryItem with default values from constants.

        Defaults allow the app to create a valid item even when users leave
        optional fields blank during the add workflow.
        """
        self._name: str = constants.NAME_DEFAULT
        self._store: str = constants.STORE_DEFAULT
        self._cost: float = float(constants.COST_DEFAULT)
        self._amount: int = constants.AMOUNT_DEFAULT
        self._priority: int = constants.PRIORITY_DEFAULT
        self._buy: bool = constants.BUY_DEFAULT
        self._id: int = constants.ID_DEFAULT

    # -----------------
    # Name
    # -----------------

    @property
    def name(self) -> str:
        """Return the item name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the item name (must be a string)."""
        if not isinstance(value, str):
            raise ValueError("Name must be a string value.")
        self._name = value

    # -----------------
    # Store
    # -----------------

    @property
    def store(self) -> str:
        """Return the store name."""
        return self._store

    @store.setter
    def store(self, value: str) -> None:
        """Set the store name (must be a string)."""
        if not isinstance(value, str):
            raise ValueError("Store must be a string value.")
        self._store = value

    # -----------------
    # Cost
    # -----------------

    @property
    def cost(self) -> float:
        """Return the item cost."""
        return self._cost

    @cost.setter
    def cost(self, value: int | float) -> None:
        """
        Set the item cost.

        Cost is stored as a float to preserve decimal values.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Cost must be an int or a float value.")
        self._cost = float(value)

    # -----------------
    # Amount
    # -----------------

    @property
    def amount(self) -> int:
        """Return the quantity (amount) to buy."""
        return self._amount

    @amount.setter
    def amount(self, value: int) -> None:
        """Set the quantity (must be a positive integer)."""
        if not isinstance(value, int):
            raise ValueError("Amount must be an int value.")
        if value <= 0:
            raise ValueError("Amount must be a positive integer.")
        self._amount = value

    # -----------------
    # Priority
    # -----------------

    @property
    def priority(self) -> int:
        """Return the priority value."""
        return self._priority

    @priority.setter
    def priority(self, value: int) -> None:
        """
        Set the priority value.

        Priority must be an integer between PRIORITY_MIN and PRIORITY_MAX.
        """
        p_min = constants.PRIORITY_MIN
        p_max = constants.PRIORITY_MAX

        if not isinstance(value, int):
            raise ValueError(f"Priority must be an int value (got {value!r}).")

        if not (p_min <= value <= p_max):
            raise ValueError(
                f"Priority must be an int value between {p_min} and {p_max}."
            )

        self._priority = value

    # -----------------
    # Buy flag
    # -----------------

    @property
    def buy(self) -> bool:
        """Return whether the item should be purchased now."""
        return self._buy

    @buy.setter
    def buy(self, value: bool) -> None:
        """Set the buy flag (must be a boolean)."""
        if not isinstance(value, bool):
            raise ValueError("Buy must be a boolean value.")
        self._buy = value

    # -----------------
    # ID
    # -----------------

    @property
    def id(self) -> int:
        """Return the unique ID for this item."""
        return self._id

    @id.setter
    def id(self, value: int) -> None:
        """
        Set the item ID.

        IDs are generated from uuid.uuid4() and converted to int.
        """
        if not isinstance(value, int):
            raise ValueError("ID must be an int.")
        self._id = value