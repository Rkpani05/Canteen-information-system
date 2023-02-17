# simple Canteen Information System using tkinter and sqlite3

import tkinter as tk
import sqlite3


class CantenInfoSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("500x300")

        #design the window make it attractive
        self.root.configure(background="light blue")
        self.root.resizable(False, False)

        # Create the GUI elements
        self.lbl_title = tk.Label(self.root, text="Canteen Information System", font=("Helvetica", 24), bg="light blue")
        self.lbl_title.pack(pady=20)

        self.btn_client = tk.Button(self.root, text="Customer", font=("Arial", 16), command=self.open_client)
        self.btn_client.pack(pady=20)

        self.btn_server = tk.Button(self.root, text="Owner", font=("Arial", 16), command=self.open_server)
        self.btn_server.pack(pady=20)

    def open_client(self):
        self.root.withdraw()
        client_window = tk.Toplevel()
        client_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(client_window))
        client_app = Client(client_window)

        # Set the window size and position
        client_window.geometry("800x600+200+200")

        # Show the window and wait for it to close
        client_window.deiconify()
        client_window.wait_window()

        # Update the items list
        self.display_items()

    def open_server(self):
        self.root.withdraw()
        server_window = tk.Toplevel()
        server_window.protocol("WM_DELETE_WINDOW", lambda: self.on_close(server_window))
        server_app = Server(server_window)

    def on_close(self, window):
        window.destroy()
        self.root.deiconify()

class Server:
    def __init__(self, root):
        self.root = root
        self.root.title("Server")
        self.root.geometry("800x600")
        self.root.configure(background="light green")
        self.root.resizable(False, False)

        # Connect to the database
        self.conn = sqlite3.connect("CIS.db")
        self.cursor = self.conn.cursor()

        # Create the table if it doesn't exist
        self.cursor.execute("CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name TEXT, price INTEGER)")

        # Create the GUI elements
        self.lbl_title = tk.Label(self.root, text="Add Delicious Food Items", font=("Arial", 24),bg="light blue")
        self.lbl_title.pack(pady=20)

        # Add a frame to contain the input fields and buttons
        self.frm_input = tk.Frame(self.root,background="light green")
        self.frm_input.pack()

        self.lbl_name = tk.Label(self.frm_input, text="Item Name", font=("Arial", 16),background="light green")
        self.lbl_name.grid(row=0, column=0, pady=10, padx=20, sticky=tk.W)

        self.ent_name = tk.Entry(self.frm_input, font=("Arial", 16), width=20)
        self.ent_name.grid(row=0, column=1, pady=10, padx=20, sticky=tk.W)

        self.lbl_price = tk.Label(self.frm_input, text="Item Price", font=("Arial", 16),background="light green")
        self.lbl_price.grid(row=1, column=0, pady=10, padx=20, sticky=tk.W)

        self.ent_price = tk.Entry(self.frm_input, font=("Arial", 16), width=10)
        self.ent_price.grid(row=1, column=1, pady=10, padx=20, sticky=tk.W)

        self.btn_add = tk.Button(self.frm_input, text="Add Item", font=("Arial", 16), command=self.add_item)
        self.btn_add.grid(row=2, column=0, pady=20, padx=20, sticky=tk.W)

        self.btn_clear = tk.Button(self.frm_input, text="Clear Fields", font=("Arial", 16), command=self.clear_fields)
        self.btn_clear.grid(row=2, column=1, pady=20, padx=20, sticky=tk.W)

        self.btn_delete = tk.Button(self.frm_input, text="Delete Items", font=("Arial", 16), command=self.deleteitems)
        self.btn_delete.grid(row=2, column=2, pady=20, padx=20, sticky=tk.W)

        self.btn_clearall = tk.Button(self.frm_input, text="Clear All", font=("Arial", 16), command=self.Clearall)
        self.btn_clearall.grid(row=2, column=3, pady=20, padx=20, sticky=tk.W)
        # Add a frame to contain the list of items
        self.frm_items = tk.Frame(self.root)
        self.frm_items.pack(pady=20)

        self.lbl_items_title = tk.Label(self.frm_items, text="Menu Items", font=("Arial", 24))
        self.lbl_items_title.pack()

        self.scrollbar = tk.Scrollbar(self.frm_items)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lst_items = tk.Listbox(self.frm_items, font=("Arial", 16), width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.lst_items.pack()

        self.scrollbar.config(command=self.lst_items.yview)

        self.display_items()

    def add_item(self):
        # Get the name and price from the entries
        name = self.ent_name.get()
        price = int(self.ent_price.get())

        # Insert the item into the database
        self.cursor.execute("INSERT INTO items (name,  price) VALUES (?,   ?)", (name, price))
        self.conn.commit()

        # Clear the entries
        self.ent_name.delete(0, tk.END)
        self.ent_price.delete(0, tk.END)

        # Display the items
        self.display_items()

    def clear_fields(self):
        self.ent_name.delete(0, tk.END)
        self.ent_price.delete(0, tk.END)

    def display_items(self):

        # Clear the listbox
        self.lst_items.delete(0, tk.END)

        # Get the items from the database
        self.cursor.execute("SELECT * FROM items")
        items = self.cursor.fetchall()

        

        #headings for the listbox rest items should be inserted below this line
        self.lst_items.insert(tk.END, "ID            Item Name                        Item Price (INR)")
        self.lst_items.insert(tk.END,"**************************************************************************")

        # Insert the items into the listbox
        for item in items:
            self.lst_items.insert(tk.END, "{:<15}{:<35}{:>9}".format(item[0], item[1], item[2]))

    def deleteitems(self):
        # delete selected item from the database
        self.cursor.execute("DELETE FROM items WHERE id = ?", (self.lst_items.curselection()[0],))
        self.conn.commit()

        # Display the items
        self.display_items()

    def Clearall(self):
        # delete all items from the database
        self.cursor.execute("DELETE FROM items")
        self.conn.commit()

        # Display the items
        self.display_items()

class Client:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu")
        self.root.geometry("300x300")

        #background color something wood colour
        self.root.configure(background="light green")


        # Connect to the database
        self.conn = sqlite3.connect("CIS.db")
        self.cursor = self.conn.cursor()

        # Add a frame to contain the list of items
        self.frm_items = tk.Frame(self.root)
        self.frm_items.pack(pady=20)
        #allign it to the middle 

        self.lbl_items_title = tk.Label(self.frm_items, text="Menu Items", font=("Arial", 24))
        self.lbl_items_title.pack()

        self.scrollbar = tk.Scrollbar(self.frm_items)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lst_items = tk.Listbox(self.frm_items, font=("Arial", 16), width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.lst_items.pack()

        self.scrollbar.config(command=self.lst_items.yview)

        self.btn_order = tk.Button(self.root, text="Order", font=("Arial", 16), command=self.order_items)
        self.btn_order.pack(pady=20)

        self.items_selected = {}

        self.display_items()

    def display_items(self):
        # Clear the listbox
        self.lst_items.delete(0, tk.END)

        # Get the items from the database
        self.cursor.execute("SELECT * FROM items")

        # Add the items to the listbox
        for item in self.cursor.fetchall():
            self.lst_items.insert(tk.END, f"{item[1]} - Rs. {item[2]}")
    
    def order_items(self):
        # Create a new window to display the selected items and their prices
        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Ordered Items")
        self.order_window.geometry("500x400")

        # Add a frame to contain the list of ordered items
        self.frm_ordered_items = tk.Frame(self.order_window)
        self.frm_ordered_items.pack(pady=20)

        self.lbl_ordered_items_title = tk.Label(self.frm_ordered_items, text="Ordered Items", font=("Arial", 24))
        self.lbl_ordered_items_title.pack()

        self.scrollbar = tk.Scrollbar(self.frm_ordered_items)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.lst_ordered_items = tk.Listbox(self.frm_ordered_items, font=("Arial", 16), width=50, height=10, yscrollcommand=self.scrollbar.set)
        self.lst_ordered_items.pack()

        self.scrollbar.config(command=self.lst_ordered_items.yview)

        # Add a frame to contain the total price and delete button
        self.frm_total = tk.Frame(self.order_window)
        self.frm_total.pack(pady=20)

        self.lbl_total = tk.Label(self.frm_total, text="Total Price:", font=("Arial", 16))
        self.lbl_total.pack(side=tk.LEFT)

        self.lbl_total_price = tk.Label(self.frm_total, text="Rs. 0", font=("Arial", 16))
        self.lbl_total_price.pack(side=tk.LEFT, padx=10)

        self.btn_delete = tk.Button(self.frm_total, text="Delete Item", font=("Arial", 16), command=self.delete_item)
        self.btn_delete.pack(side=tk.RIGHT)

        # Get the selected items from the listbox
        selected_items = self.lst_items.curselection()

        # Add the selected items to the ordered items listbox
        for index in selected_items:
            item = self.lst_items.get(index)

            # Add the item to the ordered items listbox
            self.lst_ordered_items.insert(tk.END, item)

            # Add the item to the dictionary
            self.items_selected[item] = item

        # Calculate the total price
        self.calculate_total()

        # Disable the order button
        self.btn_order.config(state=tk.DISABLED)


    def delete_item(self):
        # Delete the selected item from the ordered items listbox
        self.lst_ordered_items.delete(tk.ACTIVE)

        # Delete the item from the dictionary
        del self.items_selected[self.lst_ordered_items.get(tk.ACTIVE)]

        # Calculate the total price
        self.calculate_total()

    def calculate_total(self):
        # Calculate the total price
        total_price = 0

        for item in self.items_selected:
            # Get the price of the item
            price = item.split("Rs. ")[1]

            # Add the price to the total price
            total_price += float(price)

        # Display the total price
        self.lbl_total_price.config(text=f"Rs. {total_price}")

# Create the main window

if __name__ == "__main__":
    root = tk.Tk()
    main_menu = CantenInfoSystem(root)
    root.mainloop()