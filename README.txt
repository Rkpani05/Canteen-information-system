Canteen Information System
This is a simple program built using Python and the Tkinter library, which allows users to manage a canteen's menu of food items. It provides two interfaces, one for customers to view the menu and order items, and another for the owner to add, update, and delete items from the menu.

The program uses an SQLite database to store the menu items and their prices.

Requirements
The program requires Python 3.x and the Tkinter library to be installed. It also uses the SQLite library for Python, which should be included with most Python installations.

Usage
To start the program, run the canteen.py file in Python. This will open the main menu, where you can choose to either open the customer interface or the owner interface.

Customer Interface
The customer interface displays the list of available menu items and their prices. To order an item, select it from the list and enter the quantity in the input field next to it. Then click the "Add to Order" button to add the item to your order.

Once you have added all the items you want to order, click the "Place Order" button to view your total cost and submit the order.

Owner Interface
The owner interface allows you to add, update, and delete items from the menu. To add a new item, enter its name and price in the input fields at the top of the screen and click the "Add Item" button.

To update an existing item, select it from the list and click the "Update Item" button. This will populate the input fields with the item's current name and price. Edit the fields as desired and click the "Save Changes" button to update the item in the database.

To delete an item, select it from the list and click the "Delete Item" button.

License
This program is licensed under the MIT License. See the LICENSE file for details.

Credits
This program was created by Rk.pani