import csv  #Loads pythons CVS tools
import os   #Loads operating system helpers
import re   #Loads regular expression tools. (Used here to validate my EMAIL format)
import tkinter as tk   #Loads Tkinter GUI and renames it tk. 
from tkinter import messagebox, filedialog   #Imports popup dialogs. Messagebox give feedback. Filedialog exports to chosen file.

DATA_FILE = "artisan_portal_data.csv"   #Stores the main data file in one place


# STORAGE (CSV)
#This module loads vendor records from the CSV file and stores them in a dictionary so the application can access and use the vendor data.

def load_data():   
    if not os.path.exists(DATA_FILE):   #Checks that an CSV file exists
        return {}

    data = {}  #If not, an empty dictionary is created to store new vendor data.

    try:   #Opens CSV file, reads, and coverts it to into the dictionary
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:   #Loops through CSV rows, gets Vendor ID and skips those that do not have a Vendor ID.
                VENDOR_ID = row.get("VENDOR_ID", "").strip()
                if not VENDOR_ID:
                    continue

                data[VENDOR_ID] = {   #Uses Vendor ID to store this information in the CSV file
                    "VENDOR_NAME": row.get("VENDOR_NAME", "").strip(),
                    "EMAIL": row.get("EMAIL", "").strip(),
                    "CRAFT_TYPE": row.get("CRAFT_TYPE", "").strip(),
                    "STATUS": row.get("STATUS", "Pending").strip(),
                    "BOOTH_NUMBER": row.get("BOOTH_NUMBER", "").strip(),
                    "NOTES": row.get("NOTES", "").strip()
                }

        return data   #Returns the loaded data or an empty dictionary if an error occurs
    except:
        return {}


def save_data(data):  #Defines column names in my CSV file
    fieldnames = [
        "VENDOR_ID",
        "VENDOR_NAME",
        "EMAIL",
        "CRAFT_TYPE",
        "STATUS",
        "BOOTH_NUMBER",
        "NOTES"
    ]

    with open(DATA_FILE, "w", encoding="utf-8", newline="") as file:   #Opens, and writes the header row
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for VENDOR_ID, record in data.items():   #Writes each Vendor record into the CSV file
            writer.writerow({
                "VENDOR_ID": VENDOR_ID,
                "VENDOR_NAME": record.get("VENDOR_NAME", ""),
                "EMAIL": record.get("EMAIL", ""),
                "CRAFT_TYPE": record.get("CRAFT_TYPE", ""),
                "STATUS": record.get("STATUS", "Pending"),
                "BOOTH_NUMBER": record.get("BOOTH_NUMBER", ""),
                "NOTES": record.get("NOTES", "")
            })


def generate_VENDOR_ID(data):   #Generates vendor IDs. If none exist it starts at 1001. If one does it adds 1. 
    if not data:
        return "1001"

    existing_ids = [int(v) for v in data.keys() if str(v).isdigit()]
    if not existing_ids:
        return "1001"

    return str(max(existing_ids) + 1)


# VALIDATION
#Checks to insure my EMAIL contains the @ symbol and matches an EMAIL format of text@text.text
def is_valid_EMAIL(EMAIL):
    if "@" not in EMAIL:
        return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", EMAIL) is not None


# MAIN APPLICATION

class ArtisanPortal:   #Starts the application window, loads vendor data, and builds main window

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Artisan Portal")
        self.vendor_db = load_data()
        self.build_main_window()


    # MAIN WINDOW
    # Builds the main menu labels and buttons

    def build_main_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Welcome to Artisan Portal",
                 font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(self.root, text="Vendor Application Management System",
                 font=("Arial", 12)).pack(pady=5)

        tk.Label(self.root, text="Choose an option below",
                 font=("Arial", 11)).pack(pady=10)

        tk.Button(self.root, text="Submit Application",
                  width=25, command=self.open_submission_window).pack(pady=5)

        tk.Button(self.root, text="Check Application STATUS",
                  width=25, command=self.open_STATUS_window).pack(pady=5)

        tk.Button(self.root, text="Coordinator Review",
                  width=25, command=self.open_coordinator_window).pack(pady=5)

        tk.Button(self.root, text="Export Vendor Data",
                  width=25, command=self.export_csv).pack(pady=5)

        tk.Button(self.root, text="Exit",
                  width=25, command=self.root.destroy).pack(pady=15)


    # EXPORT
    # Opens a save window to let the user decide where to save the file. 
    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Vendor Data"
        )

        if not file_path:
            return

        fieldnames = [   #Defines the name of the columns to be placed in the CSV file
            "VENDOR_ID",
            "VENDOR_NAME",
            "EMAIL",
            "CRAFT_TYPE",
            "STATUS",
            "BOOTH_NUMBER",
            "NOTES"
        ]

        #Writes all vendor records to the CSV file and shows a confirmation message when export is complete
        with open(file_path, "w", newline="", encoding="utf-8") as file:  
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for v_id, record in self.vendor_db.items():
                writer.writerow({
                    "VENDOR_ID": v_id,
                    "VENDOR_NAME": record.get("VENDOR_NAME", ""),
                    "EMAIL": record.get("EMAIL", ""),
                    "CRAFT_TYPE": record.get("CRAFT_TYPE", ""),
                    "STATUS": record.get("STATUS", ""),
                    "BOOTH_NUMBER": record.get("BOOTH_NUMBER", ""),
                    "NOTES": record.get("NOTES", "")
                })

        messagebox.showinfo("Export Complete", "CSV exported successfully.")


    # SUBMISSION WINDOW

    def open_submission_window(self):   #Opens new window for vendor application, and creates the input fields
        win = tk.Toplevel(self.root)
        win.title("Vendor Application Form")

        tk.Label(win, text="Vendor Name").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(win, width=30)
        entry_name.grid(row=0, column=1)

        tk.Label(win, text="EMAIL").grid(row=1, column=0, padx=5, pady=5)
        entry_EMAIL = tk.Entry(win, width=30)
        entry_EMAIL.grid(row=1, column=1)

        tk.Label(win, text="Type of Craft").grid(row=2, column=0, padx=5, pady=5)
        entry_craft = tk.Entry(win, width=30)
        entry_craft.grid(row=2, column=1)

        def submit():   #Gets the entered information and checks that everything is filled and the EMAIL is valid.
            name = entry_name.get().strip()
            EMAIL = entry_EMAIL.get().strip()
            craft = entry_craft.get().strip()

            if not name or not EMAIL or not craft:
                messagebox.showerror("Error", "All fields must be completed.")
                return

            if not is_valid_EMAIL(EMAIL):
                messagebox.showerror("Error", "Enter a valid EMAIL address.")
                return

            VENDOR_ID = generate_VENDOR_ID(self.vendor_db)   #Adds new vendor information into the database dictionary with the vendor ID as the primary key

            self.vendor_db[VENDOR_ID] = {
                "VENDOR_NAME": name,
                "EMAIL": EMAIL,
                "CRAFT_TYPE": craft,
                "STATUS": "Pending",
                "BOOTH_NUMBER": "",
                "NOTES": ""
            }

            save_data(self.vendor_db)

            messagebox.showinfo(  #Shows a success message for the application submission, and closes the window. 
                "Success",
                f"Application submitted successfully.\nVendor ID: {VENDOR_ID}"
            )

            win.destroy()

        tk.Button(win, text="Submit Application",
                  command=submit).grid(row=3, column=0, pady=10)

        tk.Button(win, text="Return to Main Menu",
                  command=win.destroy).grid(row=3, column=1, pady=10)


    # STATUS CHECK WINDOW
    # Opens STATUS check window, creates labels, entry fields for vendor ID, and EMAIL. Then displays a text box for the application STATUS. 
    def open_STATUS_window(self):
        win = tk.Toplevel(self.root)
        win.title("Check Application STATUS")

        tk.Label(win, text="Vendor ID").grid(row=0, column=0, padx=5, pady=5)
        entry_id = tk.Entry(win)
        entry_id.grid(row=0, column=1)

        tk.Label(win, text="EMAIL").grid(row=1, column=0, padx=5, pady=5)
        entry_EMAIL = tk.Entry(win)
        entry_EMAIL.grid(row=1, column=1)

        result_box = tk.Text(win, width=45, height=8, state="disabled")
        result_box.grid(row=2, column=0, columnspan=2, pady=10)

        def check_STATUS():   #Gets Vendor ID and EMAIL, checks at least one was entered and prepares to search the record
            v_id = entry_id.get().strip()
            EMAIL = entry_EMAIL.get().strip()

            if not v_id and not EMAIL:
                messagebox.showerror("Error", "Enter Vendor ID or EMAIL.")
                return

            record = None

            if v_id and EMAIL:  #searches database for EMAIL and vendor ID or shows error
                if v_id in self.vendor_db and self.vendor_db[v_id].get("EMAIL", "") == EMAIL:
                    record = self.vendor_db[v_id]
                else:
                    messagebox.showerror("Error", "Vendor ID and EMAIL do not match.")
                    return

            elif v_id:   #searches database for vendor ID or shows error
                if v_id in self.vendor_db:
                    record = self.vendor_db[v_id]
                else:
                    messagebox.showerror("Error", "Vendor record not found.")
                    return

            elif EMAIL:  #searches database for EMAIL or shows error
                for r in self.vendor_db.values():
                    if r.get("EMAIL", "") == EMAIL:
                        record = r
                        break
                if not record:
                    messagebox.showerror("Error", "Vendor record not found.")
                    return

            result_box.config(state="normal")   #Displays the vendor information in a result box
            result_box.delete("1.0", tk.END)

            result_box.insert(tk.END, f"Vendor Name: {record.get('VENDOR_NAME','')}\n")
            result_box.insert(tk.END, f"Craft Type: {record.get('CRAFT_TYPE','')}\n")
            result_box.insert(tk.END, f"STATUS: {record.get('STATUS','')}\n")
            result_box.insert(tk.END, f"Booth Number: {record.get('BOOTH_NUMBER','')}\n")

            result_box.config(state="disabled")

        tk.Button(win, text="Check STATUS",    #Creates buttons to check STATUS or return to main menu
                  command=check_STATUS).grid(row=3, column=0, pady=10)

        tk.Button(win, text="Return to Main Menu",
                  command=win.destroy).grid(row=3, column=1, pady=10)


    # COORDINATOR WINDOW
    #Opens coordinator window and creates a list box to display vendors and entry field to assign booth
    def open_coordinator_window(self):
        win = tk.Toplevel(self.root)
        win.title("Coordinator Review Panel")

        listbox = tk.Listbox(win, width=80)
        listbox.pack(pady=10)

        tk.Label(win, text="Booth Number").pack()
        entry_booth = tk.Entry(win, width=20)
        entry_booth.pack(pady=5)

        def refresh():   #Refreshes list box by clearing it and repopulating it with current vendor records
            listbox.delete(0, tk.END)
            for v_id, record in self.vendor_db.items():
                name = record.get("VENDOR_NAME", "")
                STATUS = record.get("STATUS", "")
                booth = record.get("BOOTH_NUMBER", "")
                if not name:
                    continue
                listbox.insert(tk.END, f"{v_id} | {name} | {STATUS} | Booth: {booth}")

        def get_selected_VENDOR_ID():   #Collects vendor ID from selected item in the list or returns none if nothing is selected
            selection = listbox.curselection()
            if not selection:
                return None
            return listbox.get(selection[0]).split("|")[0].strip()

        def approve_vendor():   #Approves the selected vendor, saves the update, and refreshes list
            v_id = get_selected_VENDOR_ID()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return
            self.vendor_db[v_id]["STATUS"] = "Approved"
            save_data(self.vendor_db)
            refresh()

        def decline_vendor():   #Declines selected vendor, saves to the database, and refreshes list
            v_id = get_selected_VENDOR_ID()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return
            self.vendor_db[v_id]["STATUS"] = "Declined"
            save_data(self.vendor_db)
            refresh()

        def assign_booth():   #Collects the selected vendor and checks that one is selected before assigning booths
            v_id = get_selected_VENDOR_ID()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return

            if self.vendor_db[v_id].get("STATUS") != "Approved":   #Checks the vendor is approved before allowing a booth to be assigned
                messagebox.showerror("Error", "Vendor must be approved first.")
                return

            booth = entry_booth.get().strip()   #Grabs the booth number and checks that it is not empty
            if not booth:
                messagebox.showerror("Error", "Booth number cannot be empty.")
                return

            self.vendor_db[v_id]["BOOTH_NUMBER"] = booth   #Assigns booth number to the vendor, saves, and refreshes list
            save_data(self.vendor_db)
            refresh()

        def open_NOTES_editor():   #Opens the NOTES editor for selected vendor and checks that a vendor is selected.
            v_id = get_selected_VENDOR_ID()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return

            NOTES_win = tk.Toplevel(win)   #Opens a NOTES window and loads the vendor's exisiting NOTES into the text box
            NOTES_win.title(f"NOTES for Vendor {v_id}")

            tk.Label(NOTES_win, text="Coordinator NOTES").pack(pady=5)

            text_NOTES = tk.Text(NOTES_win, width=60, height=12)
            text_NOTES.pack(padx=10, pady=5)

            existing = self.vendor_db[v_id].get("NOTES", "")
            text_NOTES.insert("1.0", existing)

            def save_NOTES():   #Saves the coordinators NOTES, creates action button, and refreshes vendor list
                self.vendor_db[v_id]["NOTES"] = text_NOTES.get("1.0", tk.END).strip()
                save_data(self.vendor_db)
                messagebox.showinfo("Saved", "NOTES saved successfully.")
                NOTES_win.destroy()

            tk.Button(NOTES_win, text="Save NOTES", command=save_NOTES).pack(pady=5)
            tk.Button(NOTES_win, text="Close", command=NOTES_win.destroy).pack(pady=5)

        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Approve Vendor", command=approve_vendor).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Decline Vendor", command=decline_vendor).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="NOTES", command=open_NOTES_editor).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(button_frame, text="Assign Booth", command=assign_booth).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Return to Main Menu", command=win.destroy).grid(row=1, column=1, padx=5, pady=5)

        refresh()

    def run(self):   #Starts the tkinter event loop so that the window stays open and responds to user actions
        self.root.mainloop()


# PROGRAM START
# Starts the program by creating the application and running the main window
if __name__ == "__main__":
    app = ArtisanPortal()
    app.run()