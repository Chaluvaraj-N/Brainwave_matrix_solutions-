import tkinter as tk
from tkinter import messagebox
import json

# Authentication
USERS = {"admin": "password"}

# File to store inventory data
data_file = "inventory.json"

# Load inventory data from file
def load_inventory():
    try:
        with open(data_file, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

# Save inventory data to file
def save_inventory(data):
    with open(data_file, "w") as file:
        json.dump(data, file, indent=4)

inventory = load_inventory()

# Login window
def login():
    def authenticate():
        username = username_entry.get()
        password = password_entry.get()
        if username in USERS and USERS[username] == password:
            login_window.destroy()
            main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_window = tk.Tk()
    login_window.title("Login")

    tk.Label(login_window, text="Username:").grid(row=0, column=0)
    username_entry = tk.Entry(login_window)
    username_entry.grid(row=0, column=1)

    tk.Label(login_window, text="Password:").grid(row=1, column=0)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.grid(row=1, column=1)

    tk.Button(login_window, text="Login", command=authenticate).grid(row=2, column=1)

    login_window.mainloop()

# Main application window
def main_window():
    def add_product():
        product_id = product_id_entry.get()
        name = name_entry.get()
        quantity = quantity_entry.get()

        if not product_id or not name or not quantity.isdigit():
            messagebox.showerror("Error", "Invalid input")
            return

        quantity = int(quantity)
        inventory[product_id] = {"name": name, "quantity": quantity}
        save_inventory(inventory)
        messagebox.showinfo("Success", "Product added successfully")
        update_inventory_list()

    def edit_product():
        product_id = product_id_entry.get()
        if product_id not in inventory:
            messagebox.showerror("Error", "Product ID not found")
            return

        name = name_entry.get()
        quantity = quantity_entry.get()

        if not name or not quantity.isdigit():
            messagebox.showerror("Error", "Invalid input")
            return

        inventory[product_id]["name"] = name
        inventory[product_id]["quantity"] = int(quantity)
        save_inventory(inventory)
        messagebox.showinfo("Success", "Product edited successfully")
        update_inventory_list()

    def delete_product():
        product_id = product_id_entry.get()
        if product_id not in inventory:
            messagebox.showerror("Error", "Product ID not found")
            return

        del inventory[product_id]
        save_inventory(inventory)
        messagebox.showinfo("Success", "Product deleted successfully")
        update_inventory_list()

    def update_inventory_list():
        inventory_list.delete(0, tk.END)
        for pid, details in inventory.items():
            inventory_list.insert(tk.END, f"{pid}: {details['name']} (Qty: {details['quantity']})")

    def generate_low_stock_report():
        low_stock_items = [f"{pid}: {details['name']} (Qty: {details['quantity']})" \
                           for pid, details in inventory.items() if details['quantity'] < 5]
        if low_stock_items:
            messagebox.showinfo("Low Stock Report", "\n".join(low_stock_items))
        else:
            messagebox.showinfo("Low Stock Report", "No items with low stock")

    root = tk.Tk()
    root.title("Inventory Management System")

    tk.Label(root, text="Product ID:").grid(row=0, column=0)
    product_id_entry = tk.Entry(root)
    product_id_entry.grid(row=0, column=1)

    tk.Label(root, text="Name:").grid(row=1, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=1, column=1)

    tk.Label(root, text="Quantity:").grid(row=2, column=0)
    quantity_entry = tk.Entry(root)
    quantity_entry.grid(row=2, column=1)

    tk.Button(root, text="Add Product", command=add_product).grid(row=3, column=0)
    tk.Button(root, text="Edit Product", command=edit_product).grid(row=3, column=1)
    tk.Button(root, text="Delete Product", command=delete_product).grid(row=3, column=2)

    inventory_list = tk.Listbox(root, width=50)
    inventory_list.grid(row=4, column=0, columnspan=3)

    tk.Button(root, text="Low Stock Report", command=generate_low_stock_report).grid(row=5, column=1)

    update_inventory_list()
    root.mainloop()

if __name__ == "__main__":
    login()
