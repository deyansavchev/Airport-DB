import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

def get_db_connection():
    try:
        return psycopg2.connect(
            user="postgres",
            password="11062004", # Твоята парола
            host="127.0.0.1",
            port="5432",
            database="Airport_DB"
        )
    except Exception as e:
        messagebox.showerror("Грешка при свързване", f"Проверете дали базата 'Airport_DB' съществува.\nДетайли: {e}")
        return None

def load_flights():
    for row in tree.get_children():
        tree.delete(row)
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Синхронизирано с твоя файл 01: flight_number, destination, flight_date, flight_time
            cursor.execute("SELECT flight_id, flight_number, destination, flight_date, flight_time FROM flight")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Грешка при четене на полети: {e}")
        finally:
            cursor.close()
            conn.close()

def make_reservation():
    p_id = entry_pass.get()
    f_id = entry_flight.get()
    seat = entry_seat.get()
    price = entry_price.get()

    if not (p_id and f_id and seat and price):
        messagebox.showwarning("Внимание", "Моля, попълнете всички полета!")
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            # Синхронизирано с твоята процедура 04: book_ticket(passenger_id, flight_id, seat_number, ticket_price)
            cursor.execute("CALL book_ticket(%s, %s, %s, %s)", (p_id, f_id, seat, price))
            conn.commit()
            messagebox.showinfo("Успех", f"Билетът е резервиран! Място: {seat}")
            load_flights()
        except Exception as e:
            # Тук Python ще улови твоите RAISE EXCEPTION от SQL процедурата
            messagebox.showerror("Грешка от базата данни", str(e))
        finally:
            cursor.close()
            conn.close()

# --- ГРАФИЧЕН ИНТЕРФЕЙС ---
root = tk.Tk()
root.title("Авиодиспечерска система - Резервации")
root.geometry("800x600")

tk.Label(root, text="Налични полети в системата", font=("Arial", 14, "bold")).pack(pady=10)

# Таблица (Treeview)
columns = ("ID", "Полет №", "Дестинация", "Дата", "Час")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100, anchor=tk.CENTER)
tree.pack(pady=10, fill=tk.X, padx=20)

# Полета за резервация
frame = tk.Frame(root)
frame.pack(pady=20)

# Ред 1
tk.Label(frame, text="Пътник ID:").grid(row=0, column=0, padx=5, pady=5)
entry_pass = tk.Entry(frame, width=10); entry_pass.grid(row=0, column=1)

tk.Label(frame, text="Полет ID:").grid(row=0, column=2, padx=5, pady=5)
entry_flight = tk.Entry(frame, width=10); entry_flight.grid(row=0, column=3)

# Ред 2
tk.Label(frame, text="Място (напр. 15A):").grid(row=1, column=0, padx=5, pady=5)
entry_seat = tk.Entry(frame, width=10); entry_seat.grid(row=1, column=1)

tk.Label(frame, text="Цена:").grid(row=1, column=2, padx=5, pady=5)
entry_price = tk.Entry(frame, width=10); entry_price.grid(row=1, column=3)

# Бутони
tk.Button(root, text="РЕЗЕРВИРАЙ БИЛЕТ", command=make_reservation,
          bg="#2ecc71", fg="white", font=("Arial", 11, "bold"), width=25).pack(pady=10)

tk.Button(root, text="ОБНОВИ СПИСЪКА", command=load_flights, width=20).pack()

# Зареждане на данни при стартиране
load_flights()

root.mainloop()
