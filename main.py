import os
from datetime import datetime

# Folder setup
os.makedirs("data", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# FILE PATHS
FILES = {
    "activities": "data/activities.txt",
    "contacts": "data/contacts.txt",
    "events": "data/events.txt",
    "media": "media/files.txt"
}

def save_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")

def read_file(filename):
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def write_file(filename, lines):
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(line + "\n" for line in lines)

def add_record(file_key, record):
    save_to_file(FILES[file_key], record)

def list_records(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records found.")
        return
    for idx, rec in enumerate(records, 1):
        print(f"{idx}. {rec}")

def search_records(file_key, keyword):
    records = read_file(FILES[file_key])
    results = [rec for rec in records if keyword.lower() in rec.lower()]
    if not results:
        print("No matching records found.")
        return
    for idx, rec in enumerate(results, 1):
        print(f"{idx}. {rec}")

def edit_record(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records to edit.")
        return
    list_records(file_key)
    try:
        choice = int(input("Enter record number to edit: "))
        if choice < 1 or choice > len(records):
            print("Invalid number.")
            return
    except:
        print("Invalid input.")
        return
    print(f"Current record: {records[choice-1]}")
    new_text = input("Enter new record text:\n")
    if new_text.strip() == "":
        print("Empty input. Cancelled.")
        return
    records[choice-1] = new_text.strip()
    write_file(FILES[file_key], records)
    print("Record updated.")

def delete_record(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records to delete.")
        return
    list_records(file_key)
    try:
        choice = int(input("Enter record number to delete: "))
        if choice < 1 or choice > len(records):
            print("Invalid number.")
            return
    except:
        print("Invalid input.")
        return
    print(f"Deleting record: {records[choice-1]}")
    confirm = input("Confirm delete? (y/n): ").lower()
    if confirm == "y":
        records.pop(choice-1)
        write_file(FILES[file_key], records)
        print("Record deleted.")
    else:
        print("Delete cancelled.")

def add_activity():
    title = input("Activity Title: ")
    date = input("Date (YYYY-MM-DD): ")
    summary = input("Summary: ")
    record = f"{date} | {title} | {summary}"
    add_record("activities", record)
    print("✅ Activity saved.\n")

def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    role = input("Role (e.g. media, parent): ")
    record = f"{name} | {phone} | {email} | {role}"
    add_record("contacts", record)