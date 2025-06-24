import os
from datetime import datetime
import re
from fpdf import FPDF

# === Login Function ===
def login():
    USERNAME = "admin"
    PASSWORD = "admin123"

    print("==== PR SYSTEM LOGIN ====")
    for attempt in range(3):
        user = input("Username: ").strip()
        pwd = input("Password: ").strip()
        if user == USERNAME and pwd == PASSWORD:
            print("✅ Login successful!\n")
            return True
        else:
            print("❌ Incorrect credentials. Try again.")
    print("Too many failed attempts. Exiting.")
    return False

# === Setup ===
os.makedirs("data", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("reports", exist_ok=True)

FILES = {
    "activities": "data/activities.txt",
    "contacts": "data/contacts.txt",
    "events": "data/events.txt",
    "media": "media/files.txt"
}

# === Utilities ===
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

def valid_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except:
        return False

def valid_phone(phone):
    return re.fullmatch(r"\+?\d{7,15}", phone) is not None

def input_nonempty(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("This field cannot be empty.")

# === Add Records ===
def add_activity():
    title = input_nonempty("Activity Title: ")
    while True:
        date = input_nonempty("Date (YYYY-MM-DD): ")
        if valid_date(date):
            break
        print("Invalid date format.")
    summary = input_nonempty("Summary: ")
    save_to_file(FILES["activities"], f"{date} | {title} | {summary}")
    print("✅ Activity saved.\n")

def add_contact():
    name = input_nonempty("Name: ")
    while True:
        phone = input_nonempty("Phone (+countrycode and digits): ")
        if valid_phone(phone):
            break
        print("Invalid phone number.")
    email = input("Email: ").strip()
    role = input("Role (e.g. media, parent): ").strip()
    save_to_file(FILES["contacts"], f"{name} | {phone} | {email} | {role}")
    print("✅ Contact saved.\n")

def add_event():
    name = input_nonempty("Event Name: ")
    while True:
        date = input_nonempty("Event Date (YYYY-MM-DD): ")
        if valid_date(date):
            break
        print("Invalid date format.")
    notes = input("Notes: ").strip()
    save_to_file(FILES["events"], f"{date} | {name} | {notes}")
    print("✅ Event saved.\n")

def add_media():
    filename = input_nonempty("Enter media filename or path: ")
    save_to_file(FILES["media"], filename)
    print("✅ Media info saved.\n")

# === Generate Reports ===
def generate_text_report():
    now = datetime.now().strftime("%Y-%m-%d")
    report_name = f"reports/pr_report_{now}.txt"

    with open(report_name, "w", encoding="utf-8") as f:
        f.write("***** PR REPORT - Green Acres School *****\n")
        f.write(f"Date: {now}\n\n")

        for key, title in [("activities", "ACTIVITIES"), ("contacts", "CONTACTS"), ("events", "EVENTS"), ("media", "MEDIA FILES")]:
            f.write(f"--- {title} ---\n")
            records = read_file(FILES[key])
            if records:
                for rec in records:
                    f.write(f"* {rec}\n")
            else:
                f.write("No records found.\n")
            f.write("\n")
    print(f"✅ Text report saved: {report_name}")

def generate_pdf_report():
    now = datetime.now().strftime("%Y-%m-%d")
    pdf_name = f"reports/pr_report_{now}.pdf"

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "PR REPORT - Green Acres School", ln=True, align="C")
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 10, f"Date: {now}", ln=True, align="C")
    pdf.ln(10)

    for key, title in [("activities", "ACTIVITIES"), ("contacts", "CONTACTS"), ("events", "EVENTS"), ("media", "MEDIA FILES")]:
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, title, ln=True)
        records = read_file(FILES[key])
        pdf.set_font("Arial", "", 12)
        if records:
            for rec in records:
                pdf.multi_cell(0, 8, f"- {rec}")
        else:
            pdf.cell(0, 8, "No records found.", ln=True)
        pdf.ln(5)

    pdf.output(pdf_name)
    print(f"✅ PDF report saved: {pdf_name}")

# === Manage Records ===
def list_records(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records found.")
        return
    for idx, rec in enumerate(records, 1):
        print(f"{idx}. {rec}")

def search_records(file_key, keyword):
    results = [rec for rec in read_file(FILES[file_key]) if keyword.lower() in rec.lower()]
    if not results:
        print("No matching records.")
        return
    for i, r in enumerate(results, 1):
        print(f"{i}. {r}")

def edit_record(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records to edit.")
        return
    list_records(file_key)
    try:
        num = int(input("Enter record number to edit: "))
        if not (1 <= num <= len(records)):
            print("Invalid number.")
            return
    except:
        print("Invalid input.")
        return
    print(f"Old record: {records[num-1]}")
    new_text = input("Enter new record:\n").strip()
    if new_text:
        records[num-1] = new_text
        write_file(FILES[file_key], records)
        print("✅ Updated.")
    else:
        print("Cancelled.")

def delete_record(file_key):
    records = read_file(FILES[file_key])
    if not records:
        print("No records to delete.")
        return
    list_records(file_key)
    try:
        num = int(input("Enter record number to delete: "))
        if not (1 <= num <= len(records)):
            print("Invalid number.")
            return
    except:
        print("Invalid input.")
        return
    confirm = input(f"Delete '{records[num-1]}'? (y/n): ").lower()
    if confirm == "y":
        records.pop(num-1)
        write_file(FILES[file_key], records)
        print("✅ Deleted.")
    else:
        print("Cancelled.")

def manage_records(file_key):
    while True:
        print(f"\nManage {file_key.capitalize()}:")
        print("1. List all")
        print("2. Search")
        print("3. Edit")
        print("4. Delete")
        print("5. Back")
        choice = input("Choose: ")
        if choice == "1":
            list_records(file_key)
        elif choice == "2":
            keyword = input("Enter keyword: ")
            search_records(file_key, keyword)
        elif choice == "3":
            edit_record(file_key)
        elif choice == "4":
            delete_record(file_key)
        elif choice == "5":
            break
        else:
            print("Invalid choice.")

# === Main Menu ===
def main_menu():
    while True:
        print("\n==== PR MANAGEMENT MENU ====")
        print("1. Add Activity")
        print("2. Manage Activities")
        print("3. Add Contact")
        print("4. Manage Contacts")
        print("5. Add Event")
        print("6. Manage Events")
        print("7. Add Media File")
        print("8. Manage Media Files")
        print("9. Generate Text Report")
        print("10. Generate PDF Report")
        print("11. Exit")
        choice = input("Choose (1-11): ")

        if choice == "1":
            add_activity()
        elif choice == "2":
            manage_records("activities")
        elif choice == "3":
            add_contact()
        elif choice == "4":
            manage_records("contacts")
        elif choice == "5":
            add_event()
        elif choice == "6":
            manage_records("events")
        elif choice == "7":
            add_media()
        elif choice == "8":
            manage_records("media")
        elif choice == "9":
            generate_text_report()
        elif choice == "10":
            generate_pdf_report()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid option.")

# === Start the App ===
if __name__ == "__main__":
    if login():
        main_menu()
