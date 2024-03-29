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
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def confirm(self):
        '''
        For each MenuItem instance found in the list assigned to new_order's items attribute,
        append all list values from that MenuItem's foods attribute to the order variable's
        initially empty list. Return the new list.
        '''
        order = []
        for item in self.items:
            order.extend(menu_items[item]['foods'])
        return order

# Takes user input and gives autocomplete suggestions from the menu
menu = WordCompleter(menu_items)
text = prompt('Enter menu item: ', completer=menu)
print(text)

# new_order = Order(name, items)
