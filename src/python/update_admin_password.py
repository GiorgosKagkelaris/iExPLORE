import sqlite3

conn = sqlite3.connect("iexplore.db")
cursor = conn.cursor()

new_hash = b"$2b$12$OZwj4ipdi5nKdB2aHavODe9krv8sAj8/vu3Z13.d/mkRir3RpzeMK"

cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash.decode('utf-8'), 'admin1'))

conn.commit()
conn.close()

print(" Το password του admin1 ενημερώθηκε με επιτυχία.")
