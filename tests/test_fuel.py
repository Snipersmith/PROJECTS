

import pytest

from mfd import Fuel


class TestFuel:
    def test_fuel_initialization(self):
        fuel = Fuel("Petrol", 650.0, 1000.0)
        assert fuel.fuel_name == "Petrol"
        assert fuel.price_per_liter == 650.0
        assert fuel.quantity == 1000.0

    def test_fuel_initialization_with_whitespace(self):
        fuel = Fuel("  Diesel  ", 700.0, 800.0)
        assert fuel.fuel_name == "Diesel"

    def test_fuel_initialization_negative_price(self):
        """Test that negative price raises ValueError."""
        with pytest.raises(ValueError, match="Price per liter cannot be negative"):
            Fuel("Petrol", -100.0, 1000.0)

    def test_fuel_initialization_negative_quantity(self):
        """Test that negative quantity raises ValueError."""
        with pytest.raises(ValueError, match="Quantity cannot be negative"):
            Fuel("Petrol", 650.0, -100.0)

    def test_fuel_initialization_empty_name(self):
        """Test that empty fuel name raises ValueError."""
        with pytest.raises(ValueError, match="Fuel name cannot be empty"):
            Fuel("", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Fuel name cannot be empty"):
            Fuel("   ", 650.0, 1000.0)

    def test_price_setter(self):
        """Test setting price per liter."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        fuel.price_per_liter = 700.0
        assert fuel.price_per_liter == 700.0

    def test_price_setter_negative(self):
        """Test that setting negative price raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Price per liter cannot be negative"):
            fuel.price_per_liter = -100.0

    def test_add_quantity(self):
        """Test adding quantity to fuel."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        fuel.add_quantity(500.0)
        assert fuel.quantity == 1500.0

    def test_add_quantity_negative(self):
        """Test that adding negative quantity raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Cannot add negative quantity"):
            fuel.add_quantity(-100.0)

    def test_reduce_quantity(self):
        """Test reducing quantity from fuel."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        fuel.reduce_quantity(200.0)
        assert fuel.quantity == 800.0

    def test_reduce_quantity_negative(self):
        """Test that reducing negative quantity raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Cannot reduce negative quantity"):
            fuel.reduce_quantity(-100.0)

    def test_reduce_quantity_insufficient(self):
        """Test that reducing more than available raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Insufficient fuel"):
            fuel.reduce_quantity(1500.0)

    def test_calculate_cost(self):
        """Test calculating cost for liters."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        cost = fuel.calculate_cost(10.0)
        assert cost == 6500.0

    def test_calculate_cost_negative(self):
        """Test that calculating cost with negative liters raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Liters cannot be negative"):
            fuel.calculate_cost(-10.0)

    def test_calculate_liters(self):
        """Test calculating liters for amount."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        liters = fuel.calculate_liters(6500.0)
        assert liters == 10.0

    def test_calculate_liters_negative(self):
        """Test that calculating liters with negative amount raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            fuel.calculate_liters(-100.0)

    def test_calculate_liters_below_minimum(self):
        """Test that amount below price per liter raises ValueError."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        with pytest.raises(ValueError, match="Amount must be at least"):
            fuel.calculate_liters(500.0)

    def test_is_available(self):
        """Test checking fuel availability."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        assert fuel.is_available() is True

        fuel_empty = Fuel("Diesel", 700.0, 0.0)
        assert fuel_empty.is_available() is False

    def test_string_representation(self):
        """Test string representation of Fuel."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        str_repr = str(fuel)
        assert "Petrol" in str_repr
        assert "650.00" in str_repr
        assert "1000.00" in str_repr

    def test_repr_representation(self):
        """Test developer representation of Fuel."""
        fuel = Fuel("Petrol", 650.0, 1000.0)
        repr_str = repr(fuel)
        assert "Fuel" in repr_str
        assert "Petrol" in repr_str
        assert "650" in repr_str
        assert "1000" in repr_str
