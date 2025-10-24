"""Inventory management utilities.

Provides simple in-memory stock tracking with functions to add/remove items,
load/save data to JSON, and report low-stock items.
"""
import json
import logging
from datetime import datetime

# Global variable
stock_data = {}

def add_item(item="default", qty=0, logs=None):
    """Add qty of item to stock_data and record the action in logs if provided."""
    if not item:
        return
    if logs is None:
        logs = []
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append(f"{datetime.now()}: Added {qty} of {item}")

def remove_item(item, qty):
    """Decrease qty for item; remove the item entirely if quantity falls to zero or below."""
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        logging.warning("Attempted to remove non-existent item: %s", item)

def get_qty(item):
    """Return the current quantity for item (raises KeyError if item missing)."""
    return stock_data[item]

def load_data(file="inventory.json"):
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

def save_data(file="inventory.json"):
    """Persist current stock_data to a JSON file using UTF-8 encoding."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(stock_data, f)

def print_data():
    """Print a simple report of all items and their quantities to stdout."""
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def check_low_items(threshold=5):
    """Return a list of item names whose quantity is below the given threshold."""
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    """Demonstrate basic usage of the inventory functions (example entry point)."""
    add_item("apple", 10)
    add_item("banana", -2)
    add_item(123, "ten")  # invalid types, no check
    remove_item("apple", 3)
    remove_item("orange", 1)
    print("Apple stock:", get_qty("apple"))
    print("Low items:", check_low_items())
    save_data()
    load_data()
    print_data()
    print("eval used")

main()
