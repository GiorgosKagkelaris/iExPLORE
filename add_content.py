import tkinter as tk
from tkinter import messagebox, ttk
import json
import os

class Content:
    def __init__(self, title, description, location, price, content_type, status="published"):
        self.title = title
        self.description = description
        self.location = location
        self.price = price
        self.content_type = content_type
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "price": self.price,
            "type": self.content_type,
            "status": self.status
        }

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Προσθήκη Περιεχομένου")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f8ff")

        self.create_content_form()

    def create_content_form(self):
        tk.Label(self.root, text="➕ Προσθήκη Νέου Περιεχομένου", 
                 font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#f0f8ff")
        form_frame.pack(pady=10)

        # Επιλογή τύπου περιεχομένου
        tk.Label(form_frame, text="Τύπος Περιεχομένου:", bg="#f0f8ff").grid(row=0, column=0, sticky="w")
        self.content_type = ttk.Combobox(form_frame, values=["Προορισμός", "Δραστηριότητα", "Προσφορά", "Οδηγός"])
        self.content_type.grid(row=0, column=1)

        # Τίτλος
        tk.Label(form_frame, text="Όνομα:", bg="#f0f8ff").grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=1, column=1)

        # Περιγραφή
        tk.Label(form_frame, text="Περιγραφή:", bg="#f0f8ff").grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Entry(form_frame, width=40)
        self.description_entry.grid(row=2, column=1)

        
        tk.Label(form_frame, text="Τοποθεσία:", bg="#f0f8ff").grid(row=3, column=0, sticky="w")
        self.location_entry = tk.Entry(form_frame, width=40)
        self.location_entry.grid(row=3, column=1)

        # Τιμή
        tk.Label(form_frame, text="Τιμή (€):", bg="#f0f8ff").grid(row=4, column=0, sticky="w")
        self.price_entry = tk.Entry(form_frame, width=40)
        self.price_entry.grid(row=4, column=1)

        # Κουμπιά δράσης
        btn_frame = tk.Frame(self.root, bg="#f0f8ff")
        btn_frame.pack(pady=20)

        publish_btn = tk.Button(btn_frame, text="Δημοσίευση", command=self.publish_content, bg="#4caf50", fg="white", width=15)
        publish_btn.grid(row=0, column=0, padx=10)

        draft_btn = tk.Button(btn_frame, text="Αποθήκευση ως Πρόχειρο", command=self.save_as_draft, bg="#2196f3", fg="white", width=20)
        draft_btn.grid(row=0, column=1, padx=10)

    def validate_fields(self):
        if not self.title_entry.get() or not self.description_entry.get() or not self.location_entry.get() or not self.price_entry.get():
            messagebox.showerror("Σφάλμα", "Όλα τα πεδία πρέπει να συμπληρωθούν.")
            return False
        try:
            float(self.price_entry.get())
        except ValueError:
            messagebox.showerror("Σφάλμα", "Η τιμή πρέπει να είναι αριθμός.")
            return False
        return True

    def save_content(self, status):
        if not self.validate_fields():
            return
        content = Content(
            title=self.title_entry.get(),
            description=self.description_entry.get(),
            location=self.location_entry.get(),
            price=self.price_entry.get(),
            content_type=self.content_type.get(),
            status=status
        )
        self.save_to_file(content)
        messagebox.showinfo("Επιτυχία", f"Το περιεχόμενο αποθηκεύτηκε ως {status}.")
        self.clear_form()

    def publish_content(self):
        self.save_content("published")

    def save_as_draft(self):
        self.save_content("draft")

    def save_to_file(self, content):
        file_path = "content_data.json"
        data = []
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
        data.append(content.to_dict())
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.location_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.content_type.set("")


if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()

