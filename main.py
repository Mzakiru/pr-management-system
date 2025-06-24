import datetime

activities = []

def add_activity():
    title = input("Enter activity title: ")
    date = input("Enter date (YYYY-MM-DD): ")
    summary = input("Enter a short summary: ")
    activities.append({"title": title, "date": date, "summary": summary})
    print("✅ Activity added successfully!")

def view_activities():
    if not activities:
        print("No activities recorded yet.")
    for i, act in enumerate(activities):
        print(f"{i+1}. {act['date']} - {act['title']}:\n   {act['summary']}\n")

def generate_report():
    filename = f"pr_report_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
    with open(filename, 'w') as file:
        file.write("Green Acres PR Report\n")
        file.write(f"Date: {datetime.datetime.now().date()}\n\n")
        for act in activities:
            file.write(f"- {act['date']} | {act['title']}\n  {act['summary']}\n\n")
    print(f"✅ Report saved as {filename}")

def menu():
    while True:
        print("\n=== PR Management Menu ===")
        print("1. Add Activity")
        print("2. View Activities")
        print("3. Generate Report")
        print("4. Exit")
        choice = input("Choose an option: ")
        
        if choice == '1':
            add_activity()
        elif choice == '2':
            view_activities()
        elif choice == '3':
            generate_report()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Try again.")

menu()
