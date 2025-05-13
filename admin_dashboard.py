import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

# Πάρε το username από τα arguments (αν υπάρχει)
admin_username = sys.argv[1] if len(sys.argv) > 1 else "Χρήστης"

def open_add_content():
    try:
        subprocess.run(["python", "add_content.py"])
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία ανοίγματος του module: {e}")

def open_manage_offers():
    try:
        subprocess.run(["python", "manage_offers.py"])
    except Exception as e:
        messagebox.showerror("Σφάλμα", f"Αποτυχία ανοίγματος του module: {e}")

def logout():
    confirm = messagebox.askyesno("Αποσύνδεση", "Είσαι σίγουρος/η ότι θέλεις να αποσυνδεθείς;")
    if confirm:
        root.destroy()
        # Αν θες να επιστρέφει στο login, ξεκίνα το login script:
     #subprocess.Popen([sys.executable, "Login-Register_v.0.1.py"])

# Δημιουργία παραθύρου
root = tk.Tk()
root.title("Πίνακας Διαχειριστή")
root.geometry("420x300")

# Εμφάνιση username στο πάνω μέρος
tk.Label(root, text=f"Καλώς ήρθες, {admin_username} (Διαχειριστής)", font=("Arial", 14)).pack(pady=20)

# Κουμπιά για τα use cases
tk.Button(root, text="➕ Προσθήκη Νέου Περιεχομένου", width=35, height=2, command=open_add_content).pack(pady=10)
tk.Button(root, text="💸 Διαχείριση Προσφορών & Εκπτώσεων", width=40, height=3, command=open_manage_offers).pack(pady=10)

# Κουμπί Αποσύνδεσης
tk.Button(root, text="🚪 Αποσύνδεση", width=20, command=logout, bg="red", fg="white").pack(pady=20)

root.mainloop()
