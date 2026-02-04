

from datetime import datetime

from mfd import Transaction


class TestTransaction:
    def test_transaction_initialization(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="John Doe",
        )
        assert txn.fuel_name == "Petrol"
        assert txn.liters == 10.0
        assert txn.amount == 6500.0
        assert txn.transaction_type == "by_liters"
        assert txn.attendant_name == "John Doe"
        assert txn.transaction_id is not None
        assert isinstance(txn.timestamp, datetime)

    def test_transaction_with_custom_id(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="Sniper Smith",
            transaction_id="CUSTOM123",
        )
        assert txn.transaction_id == "CUSTOM123"

    def test_transaction_id_generation(self):
        txn1 = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="Sniper Smith",
        )
        txn2 = Transaction(
            fuel_name="Diesel",
            liters=5.0,
            amount=3500.0,
            transaction_type="by_amount",
            attendant_name="Jane Doe",
        )
        assert txn1.transaction_id != txn2.transaction_id
        assert txn1.transaction_id.startswith("TXN")
        assert txn2.transaction_id.startswith("TXN")

    def test_to_dictionary(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="John Doe",
        )
        txn_dict = txn.to_dict()
        assert isinstance(txn_dict, dict)
        assert txn_dict["fuel_name"] == "Petrol"
        assert txn_dict["liters"] == 10.0
        assert txn_dict["amount"] == 6500.0
        assert txn_dict["transaction_type"] == "by_liters"
        assert txn_dict["attendant_name"] == "John Doe"
        assert "transaction_id" in txn_dict
        assert "timestamp" in txn_dict

    def test_generate_receipt(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="John Doe",
        )
        receipt = txn.generate_receipt()
        assert isinstance(receipt, str)
        assert "FUEL DISPENSER RECEIPT" in receipt
        assert "Petrol" in receipt
        assert "10.00" in receipt
        assert "6500.00" in receipt
        assert "John Doe" in receipt
        assert txn.transaction_id in receipt

    def test_generate_receipt_by_amount(self):
        txn = Transaction(
            fuel_name="Diesel",
            liters=5.0,
            amount=3500.0,
            transaction_type="by_amount",
            attendant_name="Jane Doe",
        )
        receipt = txn.generate_receipt()
        assert "Diesel" in receipt
        assert "By Amount" in receipt

    def test_string_representation(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="John Doe",
            transaction_id="TEST123",
        )
        str_repr = str(txn)
        assert "Transaction" in str_repr
        assert "TEST123" in str_repr
        assert "Petrol" in str_repr

    def test_repr_representation(self):
        txn = Transaction(
            fuel_name="Petrol",
            liters=10.0,
            amount=6500.0,
            transaction_type="by_liters",
            attendant_name="John Doe",
            transaction_id="TEST123",
        )
        repr_str = repr(txn)
        assert "Transaction" in repr_str
        assert "TEST123" in repr_str
        assert "Petrol" in repr_str
