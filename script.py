import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2


def get_db_connection():
    try:
        return psycopg2.connect(
            user="postgres",
            password="11062004",  # Паролата от твоя скрипт
            host="127.0.0.1",
            port="5432",
            database="Airport_DB"
        )
    except Exception as e:
        messagebox.showerror("Грешка", f"Неуспешна връзка с базата: {e}")
        return None


def load_flights():
    for row in tree.get_children():
        tree.delete(row)

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Използваме малки букви за таблицата, както е в pgAdmin
            cursor.execute("SELECT flight_id, flight_no, departure_time FROM flight")
            for row in cursor.fetchall():
                # Оправено отместване (Indentation)
                tree.insert("", tk.END, values=row)
        except Exception as e:
            print(f"Грешка при четене: {e}")
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
            # Извикваме процедурата book_ticket
            cursor.execute("CALL book_ticket(%s, %s, %s, %s)", (p_id, f_id, seat, price))
            conn.commit()
            messagebox.showinfo("Успех", "Резервацията е успешна!")
            load_flights()
        except Exception as e:
            messagebox.showerror("Грешка от базата", str(e))
        finally:
            cursor.close()
            conn.close()


# GUI Настройки
root = tk.Tk()
root.title("Летищна система - Резервации")
root.geometry("650x500")

tk.Label(root, text="Налични полети", font=("Arial", 12, "bold")).pack(pady=10)

tree = ttk.Treeview(root, columns=("ID", "Полет №", "Време"), show="headings")
tree.heading("ID", text="ID");
tree.heading("Полет №", text="Полет №");
tree.heading("Време", text="Време")
tree.pack(pady=10, fill=tk.X, padx=20)

frame = tk.Frame(root)
frame.pack(pady=20)

tk.Label(frame, text="Пътник ID:").grid(row=0, column=0)
entry_pass = tk.Entry(frame, width=10);
entry_pass.grid(row=0, column=1, padx=5)

tk.Label(frame, text="Полет ID:").grid(row=0, column=2)
entry_flight = tk.Entry(frame, width=10);
entry_flight.grid(row=0, column=3, padx=5)

tk.Label(frame, text="Място:").grid(row=1, column=0, pady=10)
entry_seat = tk.Entry(frame, width=10);
entry_seat.grid(row=1, column=1)

tk.Label(frame, text="Цена:").grid(row=1, column=2)
entry_price = tk.Entry(frame, width=10);
entry_price.grid(row=1, column=3)

tk.Button(root, text="РЕЗЕРВИРАЙ БИЛЕТ", command=make_reservation, bg="green", fg="white").pack(pady=10)

load_flights()
root.mainloop()
