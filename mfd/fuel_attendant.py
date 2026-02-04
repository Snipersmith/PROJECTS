
from typing import List, Optional

from mfd.dispenser import Dispenser
from mfd.fuel import Fuel
from mfd.transaction import Transaction


class FuelAttendant:
    def __init__(self, full_name: str, dispenser: Dispenser):
        if not full_name or not full_name.strip():
            raise ValueError("Attendant name cannot be empty")

        self._full_name = full_name.strip()
        self._dispenser = dispenser
        self._transactions: List[Transaction] = []

    @property
    def full_name(self) -> str:
        return self._full_name

    @property
    def dispenser(self) -> Dispenser:
        return self._dispenser

    def add_fuel(self, fuel_name: str, price_per_liter: float, quantity: float):
        fuel = Fuel(fuel_name, price_per_liter, quantity)
        self._dispenser.add_fuel(fuel)

    def get_available_fuels(self) -> dict:
        return self._dispenser.get_available_fuels()

    def update_fuel_price(self, fuel_name: str, new_price: float):
        self._dispenser.update_fuel_price(fuel_name, new_price)

    def restock_fuel(self, fuel_name: str, liters: float):
        self._dispenser.restock_fuel(fuel_name, liters)

    def dispense_by_liters(
        self, fuel_name: str, liters: float
    ) -> Optional[Transaction]:
        if liters < 1 or liters > 50:
            raise ValueError("Liters must be between 1 and 50")

        fuel = self._dispenser.get_fuel(fuel_name)
        if fuel is None:
            raise ValueError(f"Fuel '{fuel_name}' not found")

        if not fuel.is_available():
            raise ValueError(f"Fuel '{fuel_name}' is out of stock")

        if liters > fuel.quantity:
            raise ValueError(
                f"Insufficient fuel. Available: {fuel.quantity:.2f}L, Requested: {liters}L"
            )

        amount = fuel.calculate_cost(liters)
        fuel.reduce_quantity(liters)

        transaction = Transaction(
            fuel_name=fuel.fuel_name,
            liters=liters,
            amount=amount,
            transaction_type="by_liters",
            attendant_name=self._full_name,
        )
        self._transactions.append(transaction)
        return transaction

    def dispense_by_amount(
        self, fuel_name: str, amount: float
    ) -> Optional[Transaction]:
        fuel = self._dispenser.get_fuel(fuel_name)
        if fuel is None:
            raise ValueError(f"Fuel '{fuel_name}' not found")

        if not fuel.is_available():
            raise ValueError(f"Fuel '{fuel_name}' is out of stock")

        if amount < fuel.price_per_liter:
            raise ValueError(
                f"Amount must be at least ₦{fuel.price_per_liter:.2f} (price per liter)"
            )

        liters = fuel.calculate_liters(amount)
        if liters > fuel.quantity:
            raise ValueError(
                f"Insufficient fuel. Available: {fuel.quantity:.2f}L, "
                f"Requested: {liters:.2f}L (for ₦{amount:.2f})"
            )
        actual_amount = fuel.calculate_cost(liters)
        fuel.reduce_quantity(liters)

        transaction = Transaction(
            fuel_name=fuel.fuel_name,
            liters=liters,
            amount=actual_amount,
            transaction_type="by_amount",
            attendant_name=self._full_name,
        )
        self._transactions.append(transaction)
        return transaction

    def show_all_transactions(self) -> List[Transaction]:
        return self._transactions.copy()

    def get_transaction_summary(self) -> dict:

        if not self._transactions:
            return {
                "total_transactions": 0,
                "total_liters": 0.0,
                "total_amount": 0.0,
                "by_fuel_type": {},
            }

        total_liters = sum(txn.liters for txn in self._transactions)
        total_amount = sum(txn.amount for txn in self._transactions)

        by_fuel_type = {}
        for txn in self._transactions:
            fuel_name = txn.fuel_name
            if fuel_name not in by_fuel_type:
                by_fuel_type[fuel_name] = {"liters": 0.0, "amount": 0.0, "count": 0}
            by_fuel_type[fuel_name]["liters"] += txn.liters
            by_fuel_type[fuel_name]["amount"] += txn.amount
            by_fuel_type[fuel_name]["count"] += 1

        return {
            "total_transactions": len(self._transactions),
            "total_liters": total_liters,
            "total_amount": total_amount,
            "by_fuel_type": by_fuel_type,
        }

    def __str__(self) -> str:
        """String representation of the FuelAttendant."""
        return f"FuelAttendant(name='{self._full_name}', transactions={len(self._transactions)})"

    def __repr__(self) -> str:
        """Developer representation of the FuelAttendant."""
        return f"FuelAttendant(name='{self._full_name}', transactions={len(self._transactions)})"
