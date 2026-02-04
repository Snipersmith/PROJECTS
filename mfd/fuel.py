
class Fuel:
    def __init__(self, fuel_name: str, price_per_liter: float, quantity: float):
        if price_per_liter < 0:
            raise ValueError("Price per liter cannot be negative")
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if not fuel_name or not fuel_name.strip():
            raise ValueError("Fuel name cannot be empty")

        self._fuel_name = fuel_name.strip()
        self._price_per_liter = price_per_liter
        self._quantity = quantity

    @property
    def fuel_name(self) -> str:
        return self._fuel_name

    @property
    def price_per_liter(self) -> float:
        return self._price_per_liter

    @price_per_liter.setter
    def price_per_liter(self, new_price: float):
        if new_price < 0:
            raise ValueError("Price per liter cannot be negative")
        self._price_per_liter = new_price

    @property
    def quantity(self) -> float:
        return self._quantity

    def add_quantity(self, liters: float):
        if liters < 0:
            raise ValueError("Cannot add negative quantity")
        self._quantity += liters

    def reduce_quantity(self, liters: float):
        if liters < 0:
            raise ValueError("Cannot reduce negative quantity")
        if liters > self._quantity:
            raise ValueError(f"Insufficient fuel. Available: {self._quantity}L, Requested: {liters}L")
        self._quantity -= liters

    def calculate_cost(self, liters: float) -> float:
        if liters < 0:
            raise ValueError("Liters cannot be negative")
        return liters * self._price_per_liter

    def calculate_liters(self, amount: float) -> float:
        if amount < 0:
            raise ValueError("Amount cannot be negative")
        if amount < self._price_per_liter:
            raise ValueError(f"Amount must be at least ₦{self._price_per_liter} (price per liter)")
        return amount / self._price_per_liter

    def is_available(self) -> bool:
        return self._quantity > 0

    def __str__(self) -> str:
        return f"{self._fuel_name}: ₦{self._price_per_liter:.2f}/L, Available: {self._quantity:.2f}L"

    def __repr__(self) -> str:
        return f"Fuel(name='{self._fuel_name}', price={self._price_per_liter}, quantity={self._quantity})"
