# shopping_cart.py

import datetime # Used https://stackabuse.com/how-to-format-dates-in-python/ for datetime
from dotenv import load_dotenv # Used https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/dotenv.md for .env variables
import os
load_dotenv()

products = [
    {"id":1, "name": "Chocolate Sandwich Cookies", "department": "snacks", "aisle": "cookies cakes", "price": 3.50},
    {"id":2, "name": "All-Seasons Salt", "department": "pantry", "aisle": "spices seasonings", "price": 4.99},
    {"id":3, "name": "Robust Golden Unsweetened Oolong Tea", "department": "beverages", "aisle": "tea", "price": 2.49},
    {"id":4, "name": "Smart Ones Classic Favorites Mini Rigatoni With Vodka Cream Sauce", "department": "frozen", "aisle": "frozen meals", "price": 6.99},
    {"id":5, "name": "Green Chile Anytime Sauce", "department": "pantry", "aisle": "marinades meat preparation", "price": 7.99},
    {"id":6, "name": "Dry Nose Oil", "department": "personal care", "aisle": "cold flu allergy", "price": 21.99},
    {"id":7, "name": "Pure Coconut Water With Orange", "department": "beverages", "aisle": "juice nectars", "price": 3.50},
    {"id":8, "name": "Cut Russet Potatoes Steam N' Mash", "department": "frozen", "aisle": "frozen produce", "price": 4.25},
    {"id":9, "name": "Light Strawberry Blueberry Yogurt", "department": "dairy eggs", "aisle": "yogurt", "price": 6.50},
    {"id":10, "name": "Sparkling Orange Juice & Prickly Pear Beverage", "department": "beverages", "aisle": "water seltzer sparkling water", "price": 2.99},
    {"id":11, "name": "Peach Mango Juice", "department": "beverages", "aisle": "refrigerated", "price": 1.99},
    {"id":12, "name": "Chocolate Fudge Layer Cake", "department": "frozen", "aisle": "frozen dessert", "price": 18.50},
    {"id":13, "name": "Saline Nasal Mist", "department": "personal care", "aisle": "cold flu allergy", "price": 16.00},
    {"id":14, "name": "Fresh Scent Dishwasher Cleaner", "department": "household", "aisle": "dish detergents", "price": 4.99},
    {"id":15, "name": "Overnight Diapers Size 6", "department": "babies", "aisle": "diapers wipes", "price": 25.50},
    {"id":16, "name": "Mint Chocolate Flavored Syrup", "department": "snacks", "aisle": "ice cream toppings", "price": 4.50},
    {"id":17, "name": "Rendered Duck Fat", "department": "meat seafood", "aisle": "poultry counter", "price": 9.99},
    {"id":18, "name": "Pizza for One Suprema Frozen Pizza", "department": "frozen", "aisle": "frozen pizza", "price": 12.50},
    {"id":19, "name": "Gluten Free Quinoa Three Cheese & Mushroom Blend", "department": "dry goods pasta", "aisle": "grains rice dried goods", "price": 3.99},
    {"id":20, "name": "Pomegranate Cranberry & Aloe Vera Enrich Drink", "department": "beverages", "aisle": "juice nectars", "price": 4.25}
] # based on data from Instacart: https://www.instacart.com/datasets/grocery-shopping-2017

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Source: https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/datatypes/numbers.md#formatting-as-currency
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

# GSPREAD

import gspread # Used https://github.com/prof-rossetti/intro-to-python/blob/master/notes/python/packages/gspread.md for help with Google Sheets
from oauth2client.service_account import ServiceAccountCredentials

DOCUMENT_ID = os.environ.get("GOOGLE_SHEET_ID", "OOPS")
SHEET_NAME = os.environ.get("SHEET_NAME", "Products")

# AUTHORIZATION

CREDENTIALS_FILEPATH = os.path.join(os.path.dirname(__file__), "auth", "spreadsheet_credentials.json")

AUTH_SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets", #> Allows read/write access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/drive.file" #> Per-file access to files created or opened by the app.
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILEPATH, AUTH_SCOPE)

# READ SHEET VALUES

client = gspread.authorize(credentials)

doc = client.open_by_key(DOCUMENT_ID)

print("-----------------")
print("SPREADSHEET:", doc.title)
print("-----------------")

sheet = doc.worksheet(SHEET_NAME)

products = sheet.get_all_records()

# PROCESS USER INPUTED IDS

print("Please input a product identifier.  Enter 'DONE' when finished.")
condition = True
SelectedIDs = []
while condition == True:
    try:
        UserID = input("Product ID:  ")
        if UserID.lower() == "done":
            condition = False
        else:
            MatchedID = [p for p in products if str(p["id"]) == str(UserID)]
            MatchedID = MatchedID[0]
            SelectedIDs.append(MatchedID)
    except:
        Error = "Invalid Product ID - Enter Valid"
        print(Error, end = " ")

# OUTPUT RECEIPT

print("---------------------------------")
print("FOSTER QUICKMART")
print("WWW.FOSTER-QUICKMART.COM")
print("---------------------------------")
date = datetime.date.today()
time = datetime.datetime.now()
print("CHECKOUT AT: ", date, time.strftime("%I:%M %p"))
print("---------------------------------")
print("SELECTED PRODUCTS:")
Prices = []
for MatchedID in SelectedIDs:
    print(" ... " + MatchedID["name"], " (" + to_usd(MatchedID["price"]) + ")")
    Prices.append(MatchedID["price"])
print("---------------------------------")
Subtotal = sum(Prices)
Tax = float(os.getenv("Tax", default = ".0875"))
print("SUBTOTAL: ", to_usd(Subtotal))
print("TAX: ", to_usd(Subtotal * Tax))
print("TOTAL: ", to_usd(Subtotal * (1 + Tax)))
print("---------------------------------")
print("THANKS, SEE YOU AGAIN SOON!")
print("---------------------------------")