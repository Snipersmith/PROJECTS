
from mfd import Dispenser, FuelAttendant


def display_menu():
    print("\n" + "=" * 60)
    print("     MULTI-FUEL DISPENSER SYSTEM (MFDS)")
    print("=" * 60)
    print("1. Display available fuels and prices")
    print("2. Add a new fuel")
    print("3. Update fuel price")
    print("4. Restock fuel")
    print("5. Dispense fuel by liters")
    print("6. Dispense fuel by amount")
    print("7. Show all transactions")
    print("8. Show transaction summary")
    print("9. Exit")
    print("=" * 60)


def display_available_fuels(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("AVAILABLE FUELS")
    print("-" * 60)
    available_fuels = attendant.get_available_fuels()
    if not available_fuels:
        print("No fuels available at the moment.")
    else:
        for fuel_name, fuel in available_fuels.items():
            print(f"  • {fuel}")
    print("-" * 60)


def add_new_fuel(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("ADD NEW FUEL")
    print("-" * 60)
    try:
        fuel_name = input("Enter fuel name: ").strip()
        if not fuel_name:
            print("Error: Fuel name cannot be empty.")
            return

        price = float(input("Enter price per liter (₦): "))
        if price <= 0:
            print("Error: Price must be greater than 0.")
            return

        quantity = float(input("Enter initial quantity (liters): "))
        if quantity < 0:
            print("Error: Quantity cannot be negative.")
            return

        attendant.add_fuel(fuel_name, price, quantity)
        print(f"\n✓ Successfully added {fuel_name} to the dispenser.")
    except ValueError as e:
        if "already exists" in str(e):
            print(f"Error: {e}")
        else:
            print(f"Error: Invalid input. {e}")
    except Exception as e:
        print(f"Error: {e}")


def update_fuel_price(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("UPDATE FUEL PRICE")
    print("-" * 60)
    try:
        fuel_name = input("Enter fuel name: ").strip()
        new_price = float(input("Enter new price per liter (₦): "))
        if new_price <= 0:
            print("Error: Price must be greater than 0.")
            return

        attendant.update_fuel_price(fuel_name, new_price)
        print(f"\n✓ Successfully updated {fuel_name} price to ₦{new_price:.2f}/L")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def restock_fuel(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("RESTOCK FUEL")
    print("-" * 60)
    try:
        fuel_name = input("Enter fuel name: ").strip()
        liters = float(input("Enter liters to add: "))
        if liters <= 0:
            print("Error: Liters must be greater than 0.")
            return

        attendant.restock_fuel(fuel_name, liters)
        fuel = attendant.dispenser.get_fuel(fuel_name)
        print(f"\n✓ Successfully restocked {fuel_name}. New quantity: {fuel.quantity:.2f}L")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def dispense_by_liters(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("DISPENSE FUEL BY LITERS")
    print("-" * 60)
    display_available_fuels(attendant)
    try:
        fuel_name = input("\nEnter fuel name: ").strip()
        liters = float(input("Enter liters to dispense (1-50): "))

        transaction = attendant.dispense_by_liters(fuel_name, liters)
        if transaction:
            print(transaction.generate_receipt())
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def dispense_by_amount(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("DISPENSE FUEL BY AMOUNT")
    print("-" * 60)
    display_available_fuels(attendant)
    try:
        fuel_name = input("\nEnter fuel name: ").strip()
        amount = float(input("Enter amount to spend (₦): "))

        transaction = attendant.dispense_by_amount(fuel_name, amount)
        if transaction:
            print(transaction.generate_receipt())
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def show_all_transactions(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("ALL TRANSACTIONS")
    print("-" * 60)
    transactions = attendant.show_all_transactions()
    if not transactions:
        print("No transactions recorded yet.")
    else:
        for i, txn in enumerate(transactions, 1):
            print(f"\n{i}. {txn}")
            print(f"   Date: {txn.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   Type: {txn.transaction_type.replace('_', ' ').title()}")
    print("-" * 60)


def show_transaction_summary(attendant: FuelAttendant):
    print("\n" + "-" * 60)
    print("TRANSACTION SUMMARY")
    print("-" * 60)
    summary = attendant.get_transaction_summary()
    print(f"Total Transactions: {summary['total_transactions']}")
    print(f"Total Liters Dispensed: {summary['total_liters']:.2f}L")
    print(f"Total Amount: ₦{summary['total_amount']:.2f}")
    print("\nBy Fuel Type:")
    if summary['by_fuel_type']:
        for fuel_name, stats in summary['by_fuel_type'].items():
            print(f"  • {fuel_name}:")
            print(f"    - Transactions: {stats['count']}")
            print(f"    - Liters: {stats['liters']:.2f}L")
            print(f"    - Amount: ₦{stats['amount']:.2f}")
    else:
        print("  No transactions yet.")
    print("-" * 60)


def main():
    dispenser = Dispenser()
    attendant_name = input("Enter attendant name: ").strip()
    if not attendant_name:
        attendant_name = "Default Attendant"

    attendant = FuelAttendant(attendant_name, dispenser)

    try:
        attendant.add_fuel("Petrol", 650.0, 1000.0)
        attendant.add_fuel("Diesel", 700.0, 800.0)
        print("\n✓ System initialized with sample fuels.")
    except Exception:
        pass

    while True:
        display_menu()
        try:
            choice = input("\nEnter your choice (1-9): ").strip()

            if choice == "1":
                display_available_fuels(attendant)
            elif choice == "2":
                add_new_fuel(attendant)
            elif choice == "3":
                update_fuel_price(attendant)
            elif choice == "4":
                restock_fuel(attendant)
            elif choice == "5":
                dispense_by_liters(attendant)
            elif choice == "6":
                dispense_by_amount(attendant)
            elif choice == "7":
                show_all_transactions(attendant)
            elif choice == "8":
                show_transaction_summary(attendant)
            elif choice == "9":
                print("\nThank you for using MFDS. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please enter a number between 1 and 9.")
        except KeyboardInterrupt:
            print("\n\nProgram interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
