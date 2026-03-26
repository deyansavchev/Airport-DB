import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2


# --- ФУНКЦИИ ---
def get_db_connection():
    try:
        return psycopg2.connect(
            user="postgres", password="11062004",
            host="127.0.0.1", port="5432", database="Airport_DB_master"
        )
    except Exception as e:
        messagebox.showerror("Грешка", f"Връзката се провали: {e}")
        return None


def search_flights():
    # Изчистване на резултатите
    for row in tree.get_children():
        tree.delete(row)

    origin = entry_from.get()
    dest = entry_to.get()

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            # Търсене по дестинация (симулираме търсене "От-До")
            query = """
                SELECT flight_id, flight_number, destination, flight_date, flight_time, 
                       get_available_seats(flight_id) 
                FROM flight 
                WHERE destination ILIKE %s
            """
            cursor.execute(query, (f'%{dest}%',))

            results = cursor.fetchall()
            if not results:
                messagebox.showinfo("Търсене", "Няма намерени полети за тези критерии.")

            for i, row in enumerate(results):
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                tree.insert("", tk.END, values=row, tags=(tag,))
        finally:
            cursor.close()
            conn.close()


# --- Графичен интерфейс ---
root = tk.Tk()
root.title("Софтуер за запазване на самолетни билети")
root.geometry("1000x700")
root.configure(bg="#f4f7f9")

# Главен контейнер за търсене (Header)
header_frame = tk.Frame(root, bg="#0052ff", pady=20)
header_frame.pack(fill=tk.X)

search_box = tk.LabelFrame(header_frame, text=" Търсене на полети ", bg="white", padx=20, pady=15)
search_box.pack(padx=50, fill=tk.X)

# Тип полет
type_frame = tk.Frame(search_box, bg="white")
type_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)
flight_type = tk.StringVar(value="one-way")
tk.Radiobutton(type_frame, text="Двупосочен", variable=flight_type, value="round-trip", bg="white").pack(side=tk.LEFT)
tk.Radiobutton(type_frame, text="Еднопосочен", variable=flight_type, value="one-way", bg="white").pack(side=tk.LEFT,
                                                                                                       padx=20)

# От - До
tk.Label(search_box, text="Откъде:", bg="white").grid(row=1, column=0, sticky="w")
entry_from = tk.Entry(search_box, width=20);
entry_from.insert(0, "София");
entry_from.grid(row=2, column=0, padx=5)

tk.Label(search_box, text="Докъде:", bg="white").grid(row=1, column=1, sticky="w")
entry_to = tk.Entry(search_box, width=20);
entry_to.grid(row=2, column=1, padx=5)

# Дати и Пътници
tk.Label(search_box, text="Дата заминаване:", bg="white").grid(row=1, column=2, sticky="w")
entry_date = tk.Entry(search_box, width=15);
entry_date.insert(0, "2024-03-15");
entry_date.grid(row=2, column=2, padx=5)

tk.Label(search_box, text="Пътници и класа:", bg="white").grid(row=1, column=3, sticky="w")
class_combo = ttk.Combobox(search_box, values=["1 Пътник, Икономична", "2 Пътници, Бизнес"], width=22)
class_combo.current(0);
class_combo.grid(row=2, column=3, padx=5)

# Бутон "търси"
btn_search = tk.Button(search_box, text="ТЪРСИ", bg="#ff6b00", fg="white", font=("Arial", 12, "bold"),
                       width=15, command=search_flights)
btn_search.grid(row=2, column=4, padx=10)

# Резултати (Долна част)
results_frame = tk.Frame(root, bg="#f4f7f9", pady=20)
results_frame.pack(fill=tk.BOTH, expand=True, padx=50)

tk.Label(results_frame, text="Намерени оферти:", font=("Arial", 12, "bold"), bg="#f4f7f9").pack(anchor="w")

columns = ("ID", "Полет №", "Дестинация", "Дата", "Час", "Свободни места")
tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=10)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor=tk.CENTER)
tree.pack(fill=tk.X, pady=10)

# Тагове за цветове
tree.tag_configure('oddrow', background="white")
tree.tag_configure('evenrow', background="#f1faff")

root.mainloop()
