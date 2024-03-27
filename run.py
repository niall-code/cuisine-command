import gspread
from google.oauth2.service_account import Credentials

# APIs connected to enable interaction with spreadsheet
CREDS = Credentials.from_service_account_file('creds.json')
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('food_orders')

class MenuItem:
    '''
    Create an instance of MenuItem.
    '''
    def __init__(self, foods, price):
        self.foods = foods
        self.price = price

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
            order.extend(item.foods)
        return order

test = MenuItem(['item1', 'item2', 'item3'], 12)
test2 = MenuItem(['item4', 'item5', 'item6'], 12)

new_order = Order('Geoffrey', [test, test2])
print(new_order.confirm())
