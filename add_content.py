import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

class Content:
    def __init__(self, title, description, location, price, content_type, status="published"):
        self.title = title
        self.description = description
        self.location = location
        self.price = price
        self.content_type = content_type
        self.status = status

class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Προσθήκη Περιεχομένου")
        self.root.geometry("600x500")
        self.root.config(bg="#f0f8ff")

        self.admin_id = 1  # Προσωρινά σταθερό. Συνδέστε με login σύστημα αργότερα.
        self.create_content_form()

    def create_content_form(self):
        tk.Label(self.root, text="➕ Προσθήκη Νέου Περιεχομένου", 
                 font=("Helvetica", 16, "bold"), bg="#f0f8ff").pack(pady=10)

        form_frame = tk.Frame(self.root, bg="#f0f8ff")
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Τύπος Περιεχομένου:", bg="#f0f8ff").grid(row=0, column=0, sticky="w")
        self.content_type = ttk.Combobox(form_frame, values=["destination", "activity", "offer", "guide"])
        self.content_type.grid(row=0, column=1)

        tk.Label(form_frame, text="Όνομα:", bg="#f0f8ff").grid(row=1, column=0, sticky="w")
        self.title_entry = tk.Entry(form_frame, width=40)
        self.title_entry.grid(row=1, column=1)

        tk.Label(form_frame, text="Περιγραφή:", bg="#f0f8ff").grid(row=2, column=0, sticky="w")
        self.description_entry = tk.Entry(form_frame, width=40)
        self.description_entry.grid(row=2, column=1)

        tk.Label(form_frame, text="Τοποθεσία:", bg="#f0f8ff").grid(row=3, column=0, sticky="w")
        self.location_entry = tk.Entry(form_frame, width=40)
        self.location_entry.grid(row=3, column=1)

        tk.Label(form_frame, text="Τιμή (€):", bg="#f0f8ff").grid(row=4, column=0, sticky="w")
        self.price_entry = tk.Entry(form_frame, width=40)
        self.price_entry.grid(row=4, column=1)

        btn_frame = tk.Frame(self.root, bg="#f0f8ff")
        btn_frame.pack(pady=20)

        button_style = {
            "width": 30,
            "height": 2,
            "bg": "#e6f2ff",
            "fg": "#333",
            "font": ("Arial", 10)
        }

        publish_btn = tk.Button(btn_frame, text="Δημοσίευση", command=self.publish_content, **button_style)
        publish_btn.grid(row=0, column=0, padx=10)

        draft_btn = tk.Button(btn_frame, text="Αποθήκευση ως Πρόχειρο", command=self.save_as_draft, **button_style)
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
        if not self.content_type.get():
            messagebox.showerror("Σφάλμα", "Επιλέξτε τύπο περιεχομένου.")
            return False
        return True

    def save_content(self, status):
        if not self.validate_fields():
            return
        content = Content(
            title=self.title_entry.get(),
            description=f"{self.description_entry.get()} | Τοποθεσία: {self.location_entry.get()} | Τιμή: {self.price_entry.get()} €",
            location=self.location_entry.get(),
            price=self.price_entry.get(),
            content_type=self.content_type.get(),
            status=status
        )
        self.insert_to_db(content)
        messagebox.showinfo("Επιτυχία", f"Το περιεχόμενο αποθηκεύτηκε ως '{status}'.")
        self.clear_form()

    def publish_content(self):
        self.save_content("published")

    def save_as_draft(self):
        self.save_content("draft")

    def insert_to_db(self, content):
        conn = sqlite3.connect("iexplore.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO admin_content (admin_id, type, title, description)
            VALUES (?, ?, ?, ?)
        """, (
            self.admin_id,
            content.content_type,
            content.title,
            content.description
        ))

        conn.commit()
        conn.close()

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
