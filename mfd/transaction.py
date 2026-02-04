
from datetime import datetime
from typing import Optional


class Transaction:
    def __init__(
        self,
        fuel_name: str,
        liters: float,
        amount: float,
        transaction_type: str,
        attendant_name: str,
        transaction_id: Optional[str] = None,
    ):
        self._transaction_id = transaction_id or self._generate_transaction_id()
        self._fuel_name = fuel_name
        self._liters = liters
        self._amount = amount
        self._transaction_type = transaction_type
        self._attendant_name = attendant_name
        self._timestamp = datetime.now()

    @staticmethod
    def _generate_transaction_id() -> str:
        return f"TXN{datetime.now().strftime('%Y%m%d%H%M%S%f')}"

    @property
    def transaction_id(self) -> str:
        return self._transaction_id

    @property
    def fuel_name(self) -> str:
        return self._fuel_name

    @property
    def liters(self) -> float:
        return self._liters

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def transaction_type(self) -> str:
        return self._transaction_type

    @property
    def attendant_name(self) -> str:
        return self._attendant_name

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> dict:
        return {
            "transaction_id": self._transaction_id,
            "fuel_name": self._fuel_name,
            "liters": self._liters,
            "amount": self._amount,
            "transaction_type": self._transaction_type,
            "attendant_name": self._attendant_name,
            "timestamp": self._timestamp.isoformat(),
        }

    def generate_receipt(self) -> str:
        receipt = "\n" + "=" * 50 + "\n"
        receipt += "         FUEL DISPENSER RECEIPT\n"
        receipt += "=" * 50 + "\n"
        receipt += f"Transaction ID: {self._transaction_id}\n"
        receipt += f"Date/Time: {self._timestamp.strftime('%Y-%m-%d %H:%M:%S')}\n"
        receipt += f"Attendant: {self._attendant_name}\n"
        receipt += "-" * 50 + "\n"
        receipt += f"Fuel Type: {self._fuel_name}\n"
        receipt += f"Liters: {self._liters:.2f} L\n"
        receipt += f"Amount: ₦{self._amount:.2f}\n"
        receipt += f"Transaction Type: {self._transaction_type.replace('_', ' ').title()}\n"
        receipt += "-" * 50 + "\n"
        receipt += "         Thank you for your purchase!\n"
        receipt += "=" * 50 + "\n"
        return receipt

    def __str__(self) -> str:
        """String representation of the Transaction object."""
        return (
            f"Transaction({self._transaction_id}, {self._fuel_name}, "
            f"{self._liters}L, ₦{self._amount:.2f})"
        )

    def __repr__(self) -> str:
        """Developer representation of the Transaction object."""
        return (
            f"Transaction(id='{self._transaction_id}', fuel='{self._fuel_name}', "
            f"liters={self._liters}, amount={self._amount})"
        )
