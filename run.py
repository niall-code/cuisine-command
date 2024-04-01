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

    def take_order(self):
        # Takes user input and gives autocomplete suggestions from the menu
        menu = WordCompleter(menu_items)
        while True:
            item = prompt('Enter menu item: ', completer=menu)
            if item == 'x':
                break
            else:
                try:
                    menu_items[item]
                except:
                    print('Sorry, that is not a menu item.')
                else:
                    self.items.append(item)
        return self.items

    def calculate_cost(self):
        total_cost = 0
        for item in self.items:
            total_cost += menu_items[item]
        return f'£{total_cost:.2f}'
    
    def take_name(self):
        while True:
            name = input('Enter name: ')
            try:
                len(name) >= 1
            except:
                print('A collection name is required.')
            else:
                self.name = name
                break
    
    def make_record(self, cost):
        target_worksheet = SHEET.worksheet('record')
        target_worksheet.append_row([self.name, ', '.join(self.items), cost])

def to_prepare(items):
    for item in items:
        print(item)

def main():
    new_order = Order()
    items = new_order.take_order()
    cost = new_order.calculate_cost()
    new_order.take_name()
    new_order.make_record(cost)
    to_prepare(items)

main()
