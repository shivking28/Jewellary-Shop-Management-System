import csv
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime   

class Customer:
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

class Jewellery:
    def __init__(self, name, price, description):
        self.name = name
        self.price = price
        self.description = description

class JewelleryShop:
    def __init__(self):
        self.jewellery_list = []

    def add_jewellery(self, jewellery):
        self.jewellery_list.append(jewellery)
        print()
        print()

    def add_new_jewellery(self):
        name = input("Enter jewellery name: ")
        price = float(input("Enter jewellery price: "))
        description = input("Enter jewellery description: ")
        new_jewellery = Jewellery(name, price, description)
        self.add_jewellery(new_jewellery)

    def delete_jewellery(self, jewellery_name):
        for jewellery in self.jewellery_list:
            if jewellery.name == jewellery_name:
                self.jewellery_list.remove(jewellery)
                break

    def update_jewellery_price(self, jewellery_name, new_price):
        for jewellery in self.jewellery_list:
            if jewellery.name == jewellery_name:
                jewellery.price = new_price
                break

    def display_product_names(self):
        print("Available Products:")
        for jewellery in self.jewellery_list:
            print(jewellery.name)

    def find_jewellery_by_serial(self, serial_number):
        if 0 <= serial_number < len(self.jewellery_list):
            return self.jewellery_list[serial_number]
        else:
            return None

            

    def save_jewellery_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Price"])

            for jewellery in self.jewellery_list:
                writer.writerow([jewellery.name, jewellery.price])

    def load_jewellery_from_csv(self, filename):
        self.jewellery_list = []
    
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
    
            for row in reader:
                if len(row) >= 2:  # Ensure at least two values are present (name and price)
                    name, price = row[:2]
                    description = "" if len(row) < 3 else row[2]
                    jewellery = Jewellery(name, float(price), description)
                    self.jewellery_list.append(jewellery)

def customer_purchase(shop, sales_management, customers):
    print("\nAvailable Products:")
    for index, jewellery in enumerate(shop.jewellery_list):
        print(f"{index + 1}. {jewellery.name} - {jewellery.description} (${jewellery.price:.2f})")

    try:
        serial_number = int(input("Enter the serial number of the product you want to purchase: ")) - 1
        selected_jewellery = shop.find_jewellery_by_serial(serial_number)
        if selected_jewellery:
            quantity = int(input("Enter the quantity: "))
            total_price = selected_jewellery.price * quantity
            print(f"Total Price: ${total_price:.2f}")

            # Get customer information
            customer_name = input("Enter customer name: ")
            customer_address = input("Enter customer address: ")
            customer_phone = input("Enter customer phone: ")
            customer = Customer(customer_name, customer_address, customer_phone)
            

            # Add sale logic here
            current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            sale = Sale(selected_jewellery, quantity, customer, current_date)
            sales_management.add_sale(sale)
            purchase_amount = selected_jewellery.price * quantity
            generate_bill(purchase_amount)
        else:
            print("Invalid serial number.")
    except ValueError:
        print("Invalid input. Please enter a valid serial number.")

def save_customers_to_csv(customers):
    with open("customers.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Address", "Phone"])

        for customer in customers:
            writer.writerow([customer.name, customer.address, customer.phone])

class Sale:
    def __init__(self, jewellery, quantity, customer, date):  # Include 'date' parameter
        self.jewellery = jewellery
        self.quantity = quantity
        self.customer = customer
        self.date = date


class SalesManagement:
    def __init__(self):
        self.sales_list = []

    def add_sale(self, sale):
        self.sales_list.append(sale)

    def get_sales_count_by_product(self):
        sales_count = {}
        for sale in self.sales_list:
            if sale.jewellery.name in sales_count:
                sales_count[sale.jewellery.name] += sale.quantity
            else:
                sales_count[sale.jewellery.name] = sale.quantity
        return sales_count

    def plot_sales_over_time(self):
        sales_dates = [sale.date.split()[0] for sale in self.sales_list]
        sales_quantities = {}

        for sale in self.sales_list:
            date = sale.date.split()[0]
            if date in sales_quantities:
                sales_quantities[date] += sale.quantity
            else:
                sales_quantities[date] = sale.quantity

        dates = list(sales_quantities.keys())
        quantities = list(sales_quantities.values())

        plt.figure(figsize=(10, 6))
        plt.bar(dates, quantities, color='green')
        plt.xlabel('Date')
        plt.ylabel('Total Quantity Sold')
        plt.title('Total Quantity Sold Over Time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def plot_most_sold_products(self):
        sales_count = self.get_sales_count_by_product()
        products = list(sales_count.keys())
        quantities = list(sales_count.values())

        plt.bar(products, quantities, color='blue')
        plt.xlabel('Jewellery Products')
        plt.ylabel('Quantity Sold')
        plt.title('Most Sold Jewellery Products')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def save_sales_to_csv(self, filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Jewellery Name", "Quantity", "Date", "Customer Name", "Customer Address", "Customer Phone"])
    
            for sale in self.sales_list:
                writer.writerow([sale.jewellery.name, sale.quantity, sale.date, sale.customer.name, sale.customer.address, sale.customer.phone])

    def load_sales_from_csv(self, filename, shop, customers):
        self.sales_list = []
    
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row
    
            for row in reader:
                if len(row) >= 6:  # Ensure all six values are present
                    jewellery_name, quantity, date, customer_name, customer_address, customer_phone = row
                    jewellery = self.find_jewellery_by_name(jewellery_name, shop)
                    customer = self.find_customer_by_info(customers, customer_name, customer_address, customer_phone)
                    if jewellery and customer:
                        sale = Sale(jewellery, int(quantity), date, customer)
                        self.sales_list.append(sale)

    def find_jewellery_by_name(self, jewellery_name, shop):
        for item in shop.jewellery_list:
            if item.name == jewellery_name:
                return item
        return None
                   

    def find_customer_by_info(self, customers, name, address, phone):
        for customer in customers:
            if customer.name == name and customer.address == address and customer.phone == phone:
                return customer
        return None 
        

class Admin:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def login(self, entered_username, entered_password):
        if entered_username == self.username and entered_password == self.password:
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    def change_password(self, new_password):
        self.password = new_password
        print("Password changed successfully")

    def logout(self):
        print("Logged out")

# Set the login credentials for the admin
admin = Admin("shiv","pass") 

def generate_bill(purchase_amount):
    gst_percentage = 18
    other_tax_percentage = 5
    gst_amount = (gst_percentage / 100) * purchase_amount
    other_tax_amount = (other_tax_percentage / 100) * purchase_amount
    total_amount = purchase_amount + gst_amount + other_tax_amount

    print("\n\n*** Bill ***")
    print(f"Purchase Amount: {purchase_amount:.2f}")
    print(f"GST ({gst_percentage}%): {gst_amount:.2f}")
    print(f"Other Tax ({other_tax_percentage}%): {other_tax_amount:.2f}")
    print(f"Total Amount: {total_amount:.2f}")
    print("*** Thank you for your purchase! ***\n\n")

def main():
    shop = JewelleryShop()
    sales_management = SalesManagement()
    customers = []

    shop.load_jewellery_from_csv("jewellery_data.csv")
    sales_management.load_sales_from_csv("sales_data.csv", shop, customers)
    load_customers_from_csv(customers)

    while True:
        print("\nMain Menu")
        print("1. Customer Purchase")
        print("2. Admin Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Customer Purchase
            customer_purchase(shop, sales_management, customers)  # Call customer_purchase function
        elif choice == '2':
            # Admin Login
            entered_username = input("Username: ")
            entered_password = input("Password: ")
            if admin.login(entered_username, entered_password):
                admin_menu(shop, sales_management)
        elif choice == '3':
            print("Exiting the program.")
            shop.save_jewellery_to_csv("jewellery_data.csv")
            sales_management.save_sales_to_csv("sales_data.csv")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def load_customers_from_csv(customers):
    try:
        with open("customers.csv", mode='r') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header row

            for row in readersssssssssssssssssssssssssssssssssssssssssss:
                if len(row) >= 3:  # Ensure all three values are present (name, address, phone)
                    name, address, phone = row
                    customer = Customer(name, address, phone)
                    customers.append(customer)
    except FileNotFoundError:
        pass  # Customers CSV file might not exist initially

def admin_menu(shop, sales_management):
    while True:
        print("1. Add Jewellery")
        print("2. Delete Jewellery")
        print("3. Update Jewellery Price")
        print("4. View Most Sold Products Graph")
        print("5. View Sales Over Time Graph")
        print("6. Show All Products List")
        print("7. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            # Add Jewellery
            shop.add_new_jewellery()
            print("Jewellery added successfully")
        elif choice == '2':
            # Delete Jewellery
            jewellery_name = input("Enter the name of the jewellery to delete: ")
            shop.delete_jewellery(jewellery_name)
            print("Jewellery deleted successfully")
        elif choice == '3':
            # Update Jewellery Price
            jewellery_name = input("Enter the name of the jewellery to update: ")
            new_price = float(input("Enter the new price: "))
            shop.update_jewellery_price(jewellery_name, new_price)
            print("Jewellery price updated successfully")
        elif choice == '4':
            # View Most Sold Products Graph
            sales_management.plot_most_sold_products()

        elif choice == '5':
            # View Sales Over Time Graph
            sales_management.plot_sales_over_time()

        elif choice == '6':
            # Show All Products List with Prices
            for jewellery in shop.jewellery_list:
                print(f"{jewellery.name} - {jewellery.description} (${jewellery.price:.2f})")

        elif choice == '7':
            print("Logging out from admin mode.")
            shop.save_jewellery_to_csv("jewellery_data.csv")
            sales_management.save_sales_to_csv("sales_data.csv")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    admin = Admin("shiv", "pass")
    main()
