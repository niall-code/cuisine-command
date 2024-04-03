# Import necessary libraries and modules:
# To enable API use.
import gspread
from google.oauth2.service_account import Credentials
# For autocompletion of user input.
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

# Connect APIs to enable interaction with spreadsheet.
# As demonstrated in Code Institute's Python Essentials walkthrough project.
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
        # Values initially empty string and list, to be replaced/appended to by user inputs.
        self.name = ''
        self.items = []

    def take_order(self, menu_items):
        '''
        Take user input, with autocomplete suggestions from the menu.
        Repeat for each item customer orders. User enters x to end loop.
        '''

        # prompt_toolkit was created primarily by Jonathan Slenders (https://github.com/jonathanslenders).
        # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html#autocompletion

        menu = WordCompleter(menu_items)

        while True:

            # Take user input of the first/next ordered menu item.
            # User should type menu item's dish number, press down arrow to highlight correct suggestion, then press Enter.
            item = prompt('Enter menu item:\n', completer=menu)

            # If user enters x, exit loop to resume progression through the script.
            if item == 'x':
                break
            else:
                try:
                    # Check whether input is a valid menu item.
                    menu_items[item]
                except:
                    print('Sorry, that is not a menu item.')
                else:
                    # If input was valid, append to list value of items attribute.
                    self.items.append(item)

        return self.items

    def calculate_cost(self, menu_items):
        '''
        Get prices of ordered items from dictionary in menu module.
        Sum the prices to give a total cost.
        '''
        total_cost = 0

        for item in self.items:
            total_cost += menu_items[item]

        # Total cost given with 2 decimal places.
        return f'£{total_cost:.2f}'

    def take_name(self):
        '''
        Take user input of surname to collect order under.
        '''
        while True:

            # User enters surname given by customer for collection purposes.
            # User should not include hyphens, accents, numbers, or other non-letters.
            name = input('Enter surname:\n')

            try:
                # Check input field is letters only and was not left blank.
                name.isalpha()
            except:
                print('A collection name is required. It must be letters only.')
            else:
                # Once a valid (not empty) string is given, assign to name attribute.
                self.name = name
                # Resume script progression.
                break

    def make_record(self, cost):
        '''
        Add customer's collection name, ordered dishes, and total cost to spreadsheet,
        to assist with record keeping regarding product sales and income.
        '''
        target_worksheet = SHEET.worksheet('record')
        target_worksheet.append_row([self.name, '\n'.join(self.items), cost])

def to_prepare(items):
    '''
    Remind user what dishes now need to be prepared for the customer.
    '''
    for item in items:
        print(item)

def get_menu():
    print('Menu is loading.')

    dishes = SHEET.worksheet('menu').col_values(1)
    prices = SHEET.worksheet('menu').col_values(2)

    menu_items = {}
    
    for dish, price in zip(dishes, prices):
        menu_items[dish] = price

    print('Menu has loaded.')

    return menu_items

def main():
    '''
    Run all program functions.
    '''
    new_order = Order()
    menu_items = get_menu()
    items = new_order.take_order(menu_items)
    cost = new_order.calculate_cost(menu_items)
    new_order.take_name()
    new_order.make_record(cost)
    to_prepare(items)

main()
