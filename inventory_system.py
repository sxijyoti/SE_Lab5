"""Inventory management utilities.

Provides simple in-memory stock tracking with functions to add/remove items,
load/save data to JSON, and report low-stock items.
"""
import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
    """Add qty of item to stock_data and record the action in logs if provided."""
    if not item:
        return
    if logs is None:
        logs = []
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(item, qty):
    """Decrease qty for item; remove the item entirely if quantity falls to zero or below."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Attempted to remove non-existent item: %s", item)

def getQty(item):
    """Return the current quantity for item (raises KeyError if item missing)."""
    return stock_data[item]

def loadData(file="inventory.json"):
    """Load stock data from a JSON file; on error, initialize an empty inventory."""
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except FileNotFoundError:
        logging.warning("Data file not found: %s", file)
        stock_data = {}
    except json.JSONDecodeError:
        logging.warning("Invalid JSON in data file: %s", file)
        stock_data = {}

def saveData(file="inventory.json"):
    """Persist current stock_data to a JSON file using UTF-8 encoding."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)

def printData():
    """Print a simple report of all items and their quantities to stdout."""
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    """Return a list of item names whose quantity is below the given threshold."""
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    """Demonstrate basic usage of the inventory functions (example entry point)."""
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()
    print("eval used")

main()
