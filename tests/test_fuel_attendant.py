
import pytest

from mfd import Dispenser, FuelAttendant


class TestFuelAttendant:
    def test_attendant_initialization(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        assert attendant.full_name == "Sniper Smith"
        assert attendant.dispenser == dispenser
        assert len(attendant.show_all_transactions()) == 0

    def test_attendant_initialization_empty_name(self):
        dispenser = Dispenser()
        with pytest.raises(ValueError, match="Attendant name cannot be empty"):
            FuelAttendant("", dispenser)
        with pytest.raises(ValueError, match="Attendant name cannot be empty"):
            FuelAttendant("   ", dispenser)

    def test_attendant_name_is_stripped_of_whitespace(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("  Sniper Smith  ", dispenser)
        assert attendant.full_name == "Sniper Smith"

    def test_add_fuel_through_attendant(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        assert dispenser.has_fuel("Petrol") is True

    def test_add_duplicate_fuel(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="already exists"):
            attendant.add_fuel("Petrol", 700.0, 800.0)

    def test_get_available_fuels(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        attendant.add_fuel("Diesel", 700.0, 0.0)  # Out of stock
        available = attendant.get_available_fuels()
        assert len(available) == 1
        assert "petrol" in available

    def test_update_fuel_price(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        attendant.update_fuel_price("Petrol", 700.0)
        fuel = dispenser.get_fuel("Petrol")
        assert fuel.price_per_liter == 700.0

    def test_update_fuel_price_not_found(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("Sniper Smith", dispenser)
        with pytest.raises(ValueError, match="not found"):
            attendant.update_fuel_price("NonExistent", 700.0)

    def test_restock_fuel(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        attendant.restock_fuel("Petrol", 500.0)
        fuel = dispenser.get_fuel("Petrol")
        assert fuel.quantity == 1500.0

    def test_restock_fuel_not_found(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        with pytest.raises(ValueError, match="not found"):
            attendant.restock_fuel("NonExistent", 500.0)

    def test_dispense_by_liters(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        transaction = attendant.dispense_by_liters("Petrol", 10.0)
        assert transaction is not None
        assert transaction.liters == 10.0
        assert transaction.amount == 6500.0
        assert transaction.fuel_name == "Petrol"
        assert transaction.transaction_type == "by_liters"
        assert transaction.attendant_name == "John Doe"
        fuel = dispenser.get_fuel("Petrol")
        assert fuel.quantity == 990.0

    def test_dispense_by_liters_out_of_range_low(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="between 1 and 50"):
            attendant.dispense_by_liters("Petrol", 0.5)

    def test_dispense_by_liters_out_of_range_high(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="between 1 and 50"):
            attendant.dispense_by_liters("Petrol", 51.0)

    def test_dispense_by_liters_insufficient_fuel(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 10.0)
        with pytest.raises(ValueError, match="Insufficient fuel"):
            attendant.dispense_by_liters("Petrol", 20.0)

    def test_dispense_by_liters_fuel_not_found(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        with pytest.raises(ValueError, match="not found"):
            attendant.dispense_by_liters("NonExistent", 10.0)

    def test_dispense_by_liters_out_of_stock(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 0.0)
        with pytest.raises(ValueError, match="out of stock"):
            attendant.dispense_by_liters("Petrol", 10.0)

    def test_dispense_by_amount(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        transaction = attendant.dispense_by_amount("Petrol", 6500.0)
        assert transaction is not None
        assert transaction.liters == 10.0
        assert transaction.amount == 6500.0
        assert transaction.fuel_name == "Petrol"
        assert transaction.transaction_type == "by_amount"
        fuel = dispenser.get_fuel("Petrol")
        assert fuel.quantity == 990.0

    def test_dispense_by_amount_below_minimum(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Amount must be at least"):
            attendant.dispense_by_amount("Petrol", 500.0)

    def test_dispense_by_amount_insufficient_fuel(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 5.0)  # Only 5 liters available
        with pytest.raises(ValueError, match="Insufficient fuel"):
            attendant.dispense_by_amount("Petrol", 6500.0)  # Needs 10 liters

    def test_dispense_by_amount_fuel_not_found(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        with pytest.raises(ValueError, match="not found"):
            attendant.dispense_by_amount("NonExistent", 6500.0)

    def test_dispense_by_amount_out_of_stock(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 0.0)
        with pytest.raises(ValueError, match="out of stock"):
            attendant.dispense_by_amount("Petrol", 6500.0)

    def test_show_all_transactions(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        transaction1 = attendant.dispense_by_liters("Petrol", 10.0)
        transaction2 = attendant.dispense_by_amount("Petrol", 3250.0)
        transactions = attendant.show_all_transactions()
        assert len(transactions) == 2
        assert transaction1 in transactions
        assert transaction2 in transactions

    def test_get_transaction_summary_empty(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        summary = attendant.get_transaction_summary()
        assert summary["total_transactions"] == 0
        assert summary["total_liters"] == 0.0
        assert summary["total_amount"] == 0.0
        assert summary["by_fuel_type"] == {}

    def test_get_transaction_summary(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        attendant.add_fuel("Diesel", 700.0, 1000.0)
        attendant.dispense_by_liters("Petrol", 10.0)
        attendant.dispense_by_liters("Petrol", 5.0)
        attendant.dispense_by_liters("Diesel", 10.0)
        summary = attendant.get_transaction_summary()
        assert summary["total_transactions"] == 3
        assert summary["total_liters"] == 25.0
        assert "Petrol" in summary["by_fuel_type"]
        assert "Diesel" in summary["by_fuel_type"]
        assert summary["by_fuel_type"]["Petrol"]["count"] == 2
        assert summary["by_fuel_type"]["Diesel"]["count"] == 1

    def test_string_representation(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        str_repr = str(attendant)
        assert "FuelAttendant" in str_repr
        assert "John Doe" in str_repr

    def test_repr_representation(self):
        dispenser = Dispenser()
        attendant = FuelAttendant("John Doe", dispenser)
        repr_str = repr(attendant)
        assert "FuelAttendant" in repr_str
        assert "John Doe" in repr_str
