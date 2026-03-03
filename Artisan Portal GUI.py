import csv
import os
import re
import tkinter as tk
from tkinter import messagebox, filedialog

DATA_FILE = "artisan_portal_data.csv"


# STORAGE (CSV)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}

    data = {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                vendor_id = row.get("vendor_id", "").strip()
                if not vendor_id:
                    continue

                data[vendor_id] = {
                    "vendor_name": row.get("vendor_name", "").strip(),
                    "email": row.get("email", "").strip(),
                    "craft_type": row.get("craft_type", "").strip(),
                    "status": row.get("status", "Pending").strip(),
                    "booth_number": row.get("booth_number", "").strip(),
                    "notes": row.get("notes", "").strip()
                }

        return data
    except:
        return {}


def save_data(data):
    fieldnames = [
        "vendor_id",
        "vendor_name",
        "email",
        "craft_type",
        "status",
        "booth_number",
        "notes"
    ]

    with open(DATA_FILE, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for vendor_id, record in data.items():
            writer.writerow({
                "vendor_id": vendor_id,
                "vendor_name": record.get("vendor_name", ""),
                "email": record.get("email", ""),
                "craft_type": record.get("craft_type", ""),
                "status": record.get("status", "Pending"),
                "booth_number": record.get("booth_number", ""),
                "notes": record.get("notes", "")
            })


def generate_vendor_id(data):
    if not data:
        return "1001"

    existing_ids = [int(v) for v in data.keys() if str(v).isdigit()]
    if not existing_ids:
        return "1001"

    return str(max(existing_ids) + 1)


# VALIDATION

def is_valid_email(email):
    if "@" not in email:
        return False
    return re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email) is not None


# MAIN APPLICATION

class ArtisanPortal:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Artisan Portal")
        self.vendor_db = load_data()
        self.build_main_window()


    # MAIN WINDOW

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

        tk.Button(self.root, text="Check Application Status",
                  width=25, command=self.open_status_window).pack(pady=5)

        tk.Button(self.root, text="Coordinator Review",
                  width=25, command=self.open_coordinator_window).pack(pady=5)

        tk.Button(self.root, text="Export Vendor Data",
                  width=25, command=self.export_csv).pack(pady=5)

        tk.Button(self.root, text="Exit",
                  width=25, command=self.root.destroy).pack(pady=15)


    # EXPORT

    def export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Vendor Data"
        )

        if not file_path:
            return

        fieldnames = [
            "vendor_id",
            "vendor_name",
            "email",
            "craft_type",
            "status",
            "booth_number",
            "notes"
        ]

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for v_id, record in self.vendor_db.items():
                writer.writerow({
                    "vendor_id": v_id,
                    "vendor_name": record.get("vendor_name", ""),
                    "email": record.get("email", ""),
                    "craft_type": record.get("craft_type", ""),
                    "status": record.get("status", ""),
                    "booth_number": record.get("booth_number", ""),
                    "notes": record.get("notes", "")
                })

        messagebox.showinfo("Export Complete", "CSV exported successfully.")


    # SUBMISSION WINDOW

    def open_submission_window(self):
        win = tk.Toplevel(self.root)
        win.title("Vendor Application Form")

        tk.Label(win, text="Vendor Name").grid(row=0, column=0, padx=5, pady=5)
        entry_name = tk.Entry(win, width=30)
        entry_name.grid(row=0, column=1)

        tk.Label(win, text="Email").grid(row=1, column=0, padx=5, pady=5)
        entry_email = tk.Entry(win, width=30)
        entry_email.grid(row=1, column=1)

        tk.Label(win, text="Type of Craft").grid(row=2, column=0, padx=5, pady=5)
        entry_craft = tk.Entry(win, width=30)
        entry_craft.grid(row=2, column=1)

        def submit():
            name = entry_name.get().strip()
            email = entry_email.get().strip()
            craft = entry_craft.get().strip()

            if not name or not email or not craft:
                messagebox.showerror("Error", "All fields must be completed.")
                return

            if not is_valid_email(email):
                messagebox.showerror("Error", "Enter a valid email address.")
                return

            vendor_id = generate_vendor_id(self.vendor_db)

            self.vendor_db[vendor_id] = {
                "vendor_name": name,
                "email": email,
                "craft_type": craft,
                "status": "Pending",
                "booth_number": "",
                "notes": ""
            }

            save_data(self.vendor_db)

            messagebox.showinfo(
                "Success",
                f"Application submitted successfully.\nVendor ID: {vendor_id}"
            )

            win.destroy()

        tk.Button(win, text="Submit Application",
                  command=submit).grid(row=3, column=0, pady=10)

        tk.Button(win, text="Return to Main Menu",
                  command=win.destroy).grid(row=3, column=1, pady=10)


    # STATUS CHECK WINDOW

    def open_status_window(self):
        win = tk.Toplevel(self.root)
        win.title("Check Application Status")

        tk.Label(win, text="Vendor ID").grid(row=0, column=0, padx=5, pady=5)
        entry_id = tk.Entry(win)
        entry_id.grid(row=0, column=1)

        tk.Label(win, text="Email").grid(row=1, column=0, padx=5, pady=5)
        entry_email = tk.Entry(win)
        entry_email.grid(row=1, column=1)

        result_box = tk.Text(win, width=45, height=8, state="disabled")
        result_box.grid(row=2, column=0, columnspan=2, pady=10)

        def check_status():
            v_id = entry_id.get().strip()
            email = entry_email.get().strip()

            if not v_id and not email:
                messagebox.showerror("Error", "Enter Vendor ID or Email.")
                return

            record = None

            if v_id and email:
                if v_id in self.vendor_db and self.vendor_db[v_id].get("email", "") == email:
                    record = self.vendor_db[v_id]
                else:
                    messagebox.showerror("Error", "Vendor ID and Email do not match.")
                    return

            elif v_id:
                if v_id in self.vendor_db:
                    record = self.vendor_db[v_id]
                else:
                    messagebox.showerror("Error", "Vendor record not found.")
                    return

            elif email:
                for r in self.vendor_db.values():
                    if r.get("email", "") == email:
                        record = r
                        break
                if not record:
                    messagebox.showerror("Error", "Vendor record not found.")
                    return

            result_box.config(state="normal")
            result_box.delete("1.0", tk.END)

            result_box.insert(tk.END, f"Vendor Name: {record.get('vendor_name','')}\n")
            result_box.insert(tk.END, f"Craft Type: {record.get('craft_type','')}\n")
            result_box.insert(tk.END, f"Status: {record.get('status','')}\n")
            result_box.insert(tk.END, f"Booth Number: {record.get('booth_number','')}\n")

            result_box.config(state="disabled")

        tk.Button(win, text="Check Status",
                  command=check_status).grid(row=3, column=0, pady=10)

        tk.Button(win, text="Return to Main Menu",
                  command=win.destroy).grid(row=3, column=1, pady=10)


    # COORDINATOR WINDOW

    def open_coordinator_window(self):
        win = tk.Toplevel(self.root)
        win.title("Coordinator Review Panel")

        listbox = tk.Listbox(win, width=80)
        listbox.pack(pady=10)

        tk.Label(win, text="Booth Number").pack()
        entry_booth = tk.Entry(win, width=20)
        entry_booth.pack(pady=5)

        def refresh():
            listbox.delete(0, tk.END)
            for v_id, record in self.vendor_db.items():
                name = record.get("vendor_name", "")
                status = record.get("status", "")
                booth = record.get("booth_number", "")
                if not name:
                    continue
                listbox.insert(tk.END, f"{v_id} | {name} | {status} | Booth: {booth}")

        def get_selected_vendor_id():
            selection = listbox.curselection()
            if not selection:
                return None
            return listbox.get(selection[0]).split("|")[0].strip()

        def approve_vendor():
            v_id = get_selected_vendor_id()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return
            self.vendor_db[v_id]["status"] = "Approved"
            save_data(self.vendor_db)
            refresh()

        def decline_vendor():
            v_id = get_selected_vendor_id()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return
            self.vendor_db[v_id]["status"] = "Declined"
            save_data(self.vendor_db)
            refresh()

        def assign_booth():
            v_id = get_selected_vendor_id()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return

            if self.vendor_db[v_id].get("status") != "Approved":
                messagebox.showerror("Error", "Vendor must be approved first.")
                return

            booth = entry_booth.get().strip()
            if not booth:
                messagebox.showerror("Error", "Booth number cannot be empty.")
                return

            self.vendor_db[v_id]["booth_number"] = booth
            save_data(self.vendor_db)
            refresh()

        def open_notes_editor():
            v_id = get_selected_vendor_id()
            if not v_id:
                messagebox.showerror("Error", "Select a vendor first.")
                return

            notes_win = tk.Toplevel(win)
            notes_win.title(f"Notes for Vendor {v_id}")

            tk.Label(notes_win, text="Coordinator Notes").pack(pady=5)

            text_notes = tk.Text(notes_win, width=60, height=12)
            text_notes.pack(padx=10, pady=5)

            existing = self.vendor_db[v_id].get("notes", "")
            text_notes.insert("1.0", existing)

            def save_notes():
                self.vendor_db[v_id]["notes"] = text_notes.get("1.0", tk.END).strip()
                save_data(self.vendor_db)
                messagebox.showinfo("Saved", "Notes saved successfully.")
                notes_win.destroy()

            tk.Button(notes_win, text="Save Notes", command=save_notes).pack(pady=5)
            tk.Button(notes_win, text="Close", command=notes_win.destroy).pack(pady=5)

        button_frame = tk.Frame(win)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Approve Vendor", command=approve_vendor).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Decline Vendor", command=decline_vendor).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Notes", command=open_notes_editor).grid(row=0, column=2, padx=5, pady=5)

        tk.Button(button_frame, text="Assign Booth", command=assign_booth).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Return to Main Menu", command=win.destroy).grid(row=1, column=1, padx=5, pady=5)

        refresh()

    def run(self):
        self.root.mainloop()


# PROGRAM START

if __name__ == "__main__":
    app = ArtisanPortal()
    app.run()