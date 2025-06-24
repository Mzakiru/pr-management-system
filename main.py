import os
from datetime import datetime

# Folder structure
os.makedirs("data", exist_ok=True)
os.makedirs("media", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Save data to file
def save_to_file(filename, text):
    with open(filename, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# Add PR activity
def add_activity():
    title = input("Activity Title: ")
    date = input("Date (YYYY-MM-DD): ")
    summary = input("Summary: ")
    record = f"{date} | {title} | {summary}"
    save_to_file("data/activities.txt", record)
    print("✅ Activity saved.\n")

# Add contact
def add_contact():
    name = input("Name: ")
    phone = input("Phone: ")
    email = input("Email: ")
    role = input("Role (e.g. media, parent): ")
    record = f"{name} | {phone} | {email} | {role}"
    save_to_file("data/contacts.txt", record)
    print("✅ Contact saved.\n")

# Add event
def add_event():
    name = input("Event Name: ")
    date = input("Event Date: ")
    notes = input("Notes: ")
    record = f"{date} | {name} | {notes}"
    save_to_file("data/events.txt", record)
    print("✅ Event saved.\n")

# Save media filename
def add_media():
    filename = input("Enter media filename or path (e.g. photo.jpg): ")
    save_to_file("media/files.txt", filename)
    print("✅ Media info saved.\n")

# Generate report
def generate_report():
    now = datetime.now().strftime("%Y-%m-%d")
    report_name = f"reports/pr_report_{now}.txt"
    
    with open(report_name, "w", encoding="utf-8") as f:
        f.write("PR REPORT - Green Acres School\n")
        f.write(f"Date: {now}\n\n")

        f.write("== ACTIVITIES ==\n")
        if os.path.exists("data/activities.txt"):
            with open("data/activities.txt", "r", encoding="utf-8") as a:
                f.writelines(a.readlines())
        else:
            f.write("No activities found.\n")

        f.write("\n== CONTACTS ==\n")
        if os.path.exists("data/contacts.txt"):
            with open("data/contacts.txt", "r", encoding="utf-8") as c:
                f.writelines(c.readlines())
        else:
            f.write("No contacts found.\n")

        f.write("\n== EVENTS ==\n")
        if os.path.exists("data/events.txt"):
            with open("data/events.txt", "r", encoding="utf-8") as e:
                f.writelines(e.readlines())
        else:
            f.write("No events found.\n")

        f.write("\n== MEDIA FILES ==\n")
        if os.path.exists("media/files.txt"):
            with open("media/files.txt", "r", encoding="utf-8") as m:
                f.writelines(m.readlines())
        else:
            f.write("No media recorded.\n")

    print(f"✅ Report saved: {report_name}\n")

# Main menu
def menu():
    while True:
        print("\n==== PR MANAGEMENT MENU ====")
        print("1. Add Activity")
        print("2. Add Contact")
        print("3. Add Event")
        print("4. Add Media File")
        print("5. Generate Report")
        print("6. Exit")
        choice = input("Choose an option (1-6): ")

        if choice == "1":
            add_activity()
        elif choice == "2":
            add_contact()
        elif choice == "3":
            add_event()
        elif choice == "4":
            add_media()
        elif choice == "5":
            generate_report()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("❌ Invalid option, try again.")

menu()
