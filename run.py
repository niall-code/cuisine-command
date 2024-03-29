import gspread
from google.oauth2.service_account import Credentials
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from menu import menu_items

# Connect APIs to enable interaction with spreadsheet
CREDS = Credentials.from_service_account_file('creds.json')
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('food_orders')

class Order:
    '''
    Create an instance of Order,
    which shall be assigned to new_order.
    '''
    def __init__(self):
        self.name = ''
        self.items = []

    def calculate_cost(self):
        total_cost = 0
        for item in self.items:
            total_cost += menu_items[item]
        return f'£{total_cost:.2f}'

# Takes user input and gives autocomplete suggestions from the menu
menu = WordCompleter(menu_items)
item = prompt('Enter menu item: ', completer=menu)

new_order = Order()
new_order.items.append(item)
