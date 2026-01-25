
import pytest

from mfd import Dispenser, Fuel


class TestDispenser:

    def test_dispenser_initialization(self):
        dispenser = Dispenser()
        assert len(dispenser.get_all_fuels()) == 0

    def test_add_fuel(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        assert dispenser.has_fuel("Petrol") is True
        assert dispenser.has_fuel("petrol") is True  # Case insensitive

    def test_add_duplicate_fuel(self):
        dispenser = Dispenser()
        fuel1 = Fuel("Petrol", 650.0, 1000.0)
        fuel2 = Fuel("Petrol", 700.0, 800.0)
        dispenser.add_fuel(fuel1)
        with pytest.raises(ValueError, match="already exists"):
            dispenser.add_fuel(fuel2)

    def test_get_fuel(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        retrieved_fuel = dispenser.get_fuel("Petrol")
        assert retrieved_fuel is not None
        assert retrieved_fuel.fuel_name == "Petrol"

    def test_get_fuel_case_insensitive(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        assert dispenser.get_fuel("petrol") is not None
        assert dispenser.get_fuel("PETROL") is not None

    def test_get_fuel_not_found(self):
        dispenser = Dispenser()
        assert dispenser.get_fuel("NonExistent") is None

    def test_get_all_fuels(self):
        dispenser = Dispenser()
        fuel1 = Fuel("Petrol", 650.0, 1000.0)
        fuel2 = Fuel("Diesel", 700.0, 800.0)
        dispenser.add_fuel(fuel1)
        dispenser.add_fuel(fuel2)
        all_fuels = dispenser.get_all_fuels()
        assert len(all_fuels) == 2

    def test_get_available_fuels(self):
        dispenser = Dispenser()
        fuel1 = Fuel("Petrol", 650.0, 1000.0)
        fuel2 = Fuel("Diesel", 700.0, 0.0)  # Out of stock
        dispenser.add_fuel(fuel1)
        dispenser.add_fuel(fuel2)
        available = dispenser.get_available_fuels()
        assert len(available) == 1
        assert "petrol" in available

    def test_update_fuel_price(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        dispenser.update_fuel_price("Petrol", 700.0)
        assert dispenser.get_fuel("Petrol").price_per_liter == 700.0

    def test_update_fuel_price_not_found(self):
        dispenser = Dispenser()
        with pytest.raises(ValueError, match="not found"):
            dispenser.update_fuel_price("NonExistent", 700.0)

    def test_restock_fuel(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        dispenser.restock_fuel("Petrol", 500.0)
        assert dispenser.get_fuel("Petrol").quantity == 1500.0

    def test_restock_fuel_not_found(self):
        dispenser = Dispenser()
        with pytest.raises(ValueError, match="not found"):
            dispenser.restock_fuel("NonExistent", 500.0)

    def test_remove_fuel(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        assert dispenser.remove_fuel("Petrol") is True
        assert dispenser.has_fuel("Petrol") is False

    def test_remove_fuel_not_found(self):
        dispenser = Dispenser()
        assert dispenser.remove_fuel("NonExistent") is False

    def test_has_fuel(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        assert dispenser.has_fuel("Petrol") is True
        assert dispenser.has_fuel("petrol") is True
        assert dispenser.has_fuel("NonExistent") is False

    def test_string_representation(self):
        dispenser = Dispenser()
        fuel = Fuel("Petrol", 650.0, 1000.0)
        dispenser.add_fuel(fuel)
        str_repr = str(dispenser)
        assert "Dispenser" in str_repr
        assert "Petrol" in str_repr

    def test_string_representation_empty(self):
        dispenser = Dispenser()
        str_repr = str(dispenser)
        assert "empty" in str_repr.lower()
