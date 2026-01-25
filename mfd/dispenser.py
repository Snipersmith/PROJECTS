

from typing import Dict, Optional

from mfd.fuel import Fuel


class Dispenser:


    def __init__(self):
        self._fuels: Dict[str, Fuel] = {}

    def add_fuel(self, fuel: Fuel):

        fuel_name_lower = fuel.fuel_name.lower()
        if fuel_name_lower in self._fuels:
            raise ValueError(f"Fuel '{fuel.fuel_name}' already exists in the dispenser")
        self._fuels[fuel_name_lower] = fuel

    def get_fuel(self, fuel_name: str) -> Optional[Fuel]:

        return self._fuels.get(fuel_name.lower())

    def get_all_fuels(self) -> Dict[str, Fuel]:

        return self._fuels.copy()

    def get_available_fuels(self) -> Dict[str, Fuel]:

        return {
            name: fuel for name, fuel in self._fuels.items() if fuel.is_available()
        }

    def update_fuel_price(self, fuel_name: str, new_price: float):

        fuel = self.get_fuel(fuel_name)
        if fuel is None:
            raise ValueError(f"Fuel '{fuel_name}' not found in the dispenser")
        fuel.price_per_liter = new_price

    def restock_fuel(self, fuel_name: str, liters: float):

        fuel = self.get_fuel(fuel_name)
        if fuel is None:
            raise ValueError(f"Fuel '{fuel_name}' not found in the dispenser")
        fuel.add_quantity(liters)

    def remove_fuel(self, fuel_name: str) -> bool:

        fuel_name_lower = fuel_name.lower()
        if fuel_name_lower in self._fuels:
            del self._fuels[fuel_name_lower]
            return True
        return False

    def has_fuel(self, fuel_name: str) -> bool:

        return fuel_name.lower() in self._fuels

    def __str__(self) -> str:
        if not self._fuels:
            return "Dispenser is empty"
        fuels_list = "\n".join([str(fuel) for fuel in self._fuels.values()])
        return f"Dispenser contains:\n{fuels_list}"

    def __repr__(self) -> str:
        return f"Dispenser(fuels={list(self._fuels.keys())})"
