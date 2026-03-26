import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2
from tkcalendar import DateEntry
import datetime

#Усановяване на връзка със сървъра
def get_db_connection():
    try:
        return psycopg2.connect(
            user="postgres",
            password="11062004",
            host="127.0.0.1",
            port="5432",
            database="Airport_DB_master"
        )
    except Exception as e:
        messagebox.showerror("Грешка", f"Връзката се провали: {e}")
        return None

def search_flights():
    for row in tree.get_children():
        tree.delete(row)

    dest = entry_to.get().strip()
    selected_date = entry_date.get_date()
    # Взимаме избраната класа - не знам това дали ще го оставя или просто ще го махна, защото трябва и в базата да добавям към полетите това. Понеже в момента просто си стои.
    selected_class = class_combo.get()

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            query = """
                SELECT flight_id, flight_number, destination, flight_date, flight_time, 
                       get_available_seats(flight_id) 
                FROM flight 
                WHERE destination ILIKE %s AND flight_date = %s
            """
            cursor.execute(query, (f'%{dest}%', selected_date))
            results = cursor.fetchall()

            if not results:
                messagebox.showinfo("Търсене", f"Няма полети за {dest} на {selected_date}.")

            for i, row in enumerate(results):
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                # Показваме резултатите
                tree.insert("", tk.END, values=row, tags=(tag,))
        finally:
            cursor.close()
            conn.close()

def make_reservation():
    data = (entry_pass.get(), entry_flight.get(), entry_seat.get(), entry_price.get())
    if not all(data):
        messagebox.showwarning("Внимание", "Попълнете всички полета!")
        return

    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            #Извикване на процедурата от базата
            cursor.execute("CALL book_ticket(%s, %s, %s, %s)", data)
            conn.commit()
            messagebox.showinfo("Успех", "Резервацията е потвърдена!")
            search_flights()
        except Exception as e:
            error_msg = str(e).split('\n')[0].replace("P0001:", "").strip()
            messagebox.showerror("Грешка", error_msg)
        finally:
            cursor.close()
            conn.close()

#Графичен интерфейс
root = tk.Tk()
root.title("eSky - Търсене и Резервация 2026")
root.geometry("1150x800")
root.configure(bg="#f4f7f9")

#Header
header_frame = tk.Frame(root, bg="#0052ff", pady=20)
header_frame.pack(fill=tk.X)

search_box = tk.LabelFrame(header_frame, text=" Търсене на полети ", bg="white", padx=20, pady=15)
search_box.pack(padx=50, fill=tk.X)

#Тип полет - отново нещо, което трябва да преценя дали ще оставя. Най-вероятно ще го оставя, но просто трябва да се напише в базата.
type_frame = tk.Frame(search_box, bg="white")
type_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)
tk.Radiobutton(type_frame, text="Двупосочен", value=1, bg="white").pack(side=tk.LEFT)
tk.Radiobutton(type_frame, text="Еднопосочен", value=2, bg="white").pack(side=tk.LEFT, padx=20)

#Основни полета
tk.Label(search_box, text="Откъде:", bg="white").grid(row=1, column=0, sticky="w")
entry_from = tk.Entry(search_box, width=18); entry_from.insert(0, "Sofia"); entry_from.grid(row=2, column=0, padx=5)

tk.Label(search_box, text="Докъде:", bg="white").grid(row=1, column=1, sticky="w")
entry_to = tk.Entry(search_box, width=18); entry_to.grid(row=2, column=1, padx=5)

tk.Label(search_box, text="Дата:", bg="white").grid(row=1, column=2, sticky="w")
entry_date = DateEntry(search_box, width=15, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
entry_date.grid(row=2, column=2, padx=5)

#Брой пътници и избор на класа
tk.Label(search_box, text="Пътници и класа:", bg="white").grid(row=1, column=3, sticky="w")
class_combo = ttk.Combobox(search_box, values=[
    "1 Пътник, Икономична",
    "1 Пътник, Бизнес",
    "2 Пътници, Икономична",
    "2 Пътници, Бизнес"
], width=25)
class_combo.current(0)
class_combo.grid(row=2, column=3, padx=5)

btn_search = tk.Button(search_box, text="ТЪРСИ", bg="#ff6b00", fg="white", font=("Arial", 11, "bold"), width=12, command=search_flights)
btn_search.grid(row=2, column=4, padx=10)

#Таблица с резултати - Тук не знам дали ще оставя колоните по този начин. По-скоро потребителя трябва да си въведе имената, а не ID и трябва да въведе номер на мястото може би?
results_frame = tk.Frame(root, bg="#f4f7f9", pady=10)
results_frame.pack(fill=tk.BOTH, expand=True, padx=50)

columns = ("ID", "Полет №", "Дестинация", "Дата", "Час", "Свободни места")
tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=140, anchor=tk.CENTER)
tree.tag_configure('oddrow', background="white")
tree.tag_configure('evenrow', background="#f1faff")
tree.pack(fill=tk.X)

#Резервация
res_box = tk.LabelFrame(root, text=" Детайли за резервация ", bg="white", padx=20, pady=15)
res_box.pack(padx=50, pady=20, fill=tk.X)

fields = [("Пътник ID:", "e_p"), ("Полет ID:", "e_f"), ("Място:", "e_s"), ("Цена:", "e_pr")]
res_entries = {}

for i, (label, var) in enumerate(fields):
    tk.Label(res_box, text=label, bg="white").grid(row=0, column=i*2, padx=5)
    entry = tk.Entry(res_box, width=10)
    entry.grid(row=0, column=i*2+1, padx=5)
    res_entries[var] = entry

entry_pass, entry_flight, entry_seat, entry_price = res_entries.values()

btn_book = tk.Button(res_box, text="ПОТВЪРДИ РЕЗЕРВАЦИЯ", bg="#27ae60", fg="white", font=("Arial", 10, "bold"), command=make_reservation)
btn_book.grid(row=0, column=8, padx=20)

root.mainloop()
