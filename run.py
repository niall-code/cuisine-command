# Import necessary libraries and modules:
# To enable API use.
import gspread
from google.oauth2.service_account import Credentials
# System, for clearing terminal.
import os
# For coloring of certain terminal text. https://pypi.org/project/colorama/
from colorama import Fore, init
# For autocompletion of user input. https://pypi.org/project/prompt-toolkit/
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
# For order summary in table format. https://pypi.org/project/tabulate/
from tabulate import tabulate

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

# Auto-reset to default color after each colorama use.
init(autoreset=True)


class Order:
    '''
    Create an instance of Order,
    which shall be assigned to new_order.
    '''
    def __init__(self):
        # Values initially empty string and list, to be replaced/appended to by
        # user inputs.
        self.name = ''
        self.items = []

    def take_order(self, menu_items):
        '''
        Take user input, with autocomplete suggestions from the menu.
        Repeat for each item customer orders. User enters x to end loop.
        '''

        # https://python-prompt-toolkit.readthedocs.io/en/stable/pages/asking_for_input.html#autocompletion

        menu = WordCompleter(menu_items)

        quit = False
        if not quit:

            # Take user input of the first/next ordered menu item.
            # User should type menu item's dish number, press down arrow to
            # highlight correct suggestion, then press Enter.
            item = prompt('\nEnter menu item:\n', completer=menu)

            # If user enters x, exit loop to resume progression through the
            # script. At least one menu item must have been entered first.
            if item == 'x':
                if len(self.items) >= 1:
                    quit = True
                else:
                    # Red text for invalidity message.
                    print(Fore.RED + 'An order must have at least one item.')
            else:
                try:
                    # Check whether input is a valid menu item.
                    menu_items[item]
                except Exception:
                    # Red text for invalidity message.
                    print(Fore.RED + 'Sorry, that is not a valid menu item.')
                else:
                    # If input was valid, append to list value of items
                    # attribute.
                    self.items.append(item)

        return self.items

    def calculate_cost(self, menu_items):
        '''
        Get prices of ordered items from menu_items dictionary.
        Sum the prices to give a total cost.
        '''
        total_cost = 0

        for item in self.items:
            total_cost += menu_items[item]

        # Total cost given with 2 decimal places.
        return f'£{total_cost:.2f}'

    def take_name(self):
        '''
        Take user input of surname for customer to collect order with.
        '''
        given = False
        if not given:

            # User enters surname given by customer for collection purposes.
            # User should not include hyphens, accents, numbers, or other
            # non-letters.
            name = input('\nEnter surname:\n')

            try:
                # Check input field is letters only and was not left blank.
                name.isalpha()
            except Exception:
                # Red text for invalidity message.
                print(Fore.RED + 'A letters-only collection name is required.')
            else:
                # Once a valid (not empty) string is given, assign to name
                # attribute.
                self.name = name
                # Resume script progression.
                given = True

        return self.name

    def make_record(self, cost):
        '''
        Add customer's surname, ordered dishes, and total cost to worksheet,
        to assist with record keeping regarding product sales and income.
        '''
        target_worksheet = SHEET.worksheet('record')
        target_worksheet.append_row([self.name, '\n'.join(self.items), cost])


def clear_terminal():
    '''
    Clear the terminal.
    '''

    # Learnt from https://www.geeksforgeeks.org/clear-screen-python/

    if os.name == 'nt':
        # Windows
        os.system('cls')
    else:
        # Mac or Linux
        os.system('clear')


def title_banner():
    '''
    Print the ASCII art title banner, colored green.
    '''

    # Made with https://www.ascii-art-generator.org/

    print(Fore.GREEN + r'''
 _     ___  __ ___       _    _  _                       _
/  | |  |  (_   |  |\ | |_   /  / \ |\/| |\/|  /\  |\ | | \
\_ |_| _|_ __) _|_ | \| |_   \_ \_/ |  | |  | /--\ | \| |_/ ''')


def get_menu():
    '''
    Retrieve menu from worksheet. Convert into dictionary.
    '''
    print('\nMenu is loading.')

    dishes = SHEET.worksheet('menu').col_values(1)
    prices = SHEET.worksheet('menu').col_values(2)

    menu_items = {}

    for dish, price in zip(dishes, prices):
        menu_items[dish] = float(price)

    print('Menu has loaded.')

    return menu_items


def to_prepare(name, items, cost):
    '''
    Remind user what dishes now need to be prepared for the customer.
    '''
    table = [['NAME', 'ITEMS ORDERED', 'COST'],
             [name, '\n'.join(items), cost]]
    print('\n' + tabulate(table, tablefmt='pretty'))


def main():
    '''
    Run all program functions.
    '''
    # Clear terminal in case not the first time program run.
    clear_terminal()
    title_banner()
    new_order = Order()
    menu_items = get_menu()
    items = new_order.take_order(menu_items)
    cost = new_order.calculate_cost(menu_items)
    clear_terminal()

    # Reprint banner after terminal cleared.
    title_banner()
    name = new_order.take_name()
    new_order.make_record(cost)
    clear_terminal()

    title_banner()
    to_prepare(name, items, cost)


main()
