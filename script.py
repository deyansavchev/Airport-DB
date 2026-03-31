import tkinter as tk #Библиотека за създаване на GUI
from tkinter import messagebox, ttk #Инструменти за изскачащи съобщения
import psycopg2 #Драйвер за връзка с PostgreSQL
from tkcalendar import DateEntry #Визуален календар
import datetime #Библиотека за работа с дати и час


#Установяване на връзка с базата
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


#Функции за търсене
def search_flights():
    #Изчистваме старите резултати от таблицата
    for row in tree.get_children():
        tree.delete(row)

    #Взимаме данните от интерфейса
    dest = entry_to.get().strip()
    selected_date = entry_date.get_date()
    ignore_date = var_ignore_date.get()

    #Преобразуваме избора от Радио бутоните в Boolean за базата
    #Двупосочен (True), 2 = Еднопосочен (False)
    is_rt_value = True if var_flight_type.get() == 1 else False

    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        try:
            #Дефинираме SQL заявката
            query = """
                SELECT flight_id, flight_number, destination, flight_date, flight_time, 
                       get_available_seats(flight_id), base_price, is_round_trip 
                FROM flight 
                WHERE destination ILIKE %s AND is_round_trip = %s
            """
            params = [f'%{dest}%', is_rt_value]

            #Добавяме филтър за дата само ако потребителят НЕ е избрал "Всички дати"
            if not ignore_date:
                query += " AND flight_date = %s"
                params.append(selected_date)

            query += " ORDER BY flight_date ASC"
            cursor.execute(query, tuple(params))

            results = cursor.fetchall()

            #Обработка на резултатите за визуализация
            for i, row in enumerate(results):
                #Превръщаме кортежа в списък, за да променим True/False на текст
                display_row = list(row)

                if display_row[7] == True:
                    display_row[7] = "Двупосочен"
                else:
                    display_row[7] = "Еднопосочен"

                # Редуване на цветове на редовете за по-добра четимост
                tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                tree.insert("", tk.END, values=display_row, tags=(tag,))

            if not results:
                messagebox.showinfo("Търсене", "Няма намерени полети за тези критерии.")

        except Exception as e:
            messagebox.showerror("Грешка при търсене", f"SQL грешка: {e}")
        finally:
            cursor.close()
            conn.close()

#Функция за изчистване
def clear_all():
    entry_to.delete(0, tk.END)
    entry_from.delete(0, tk.END)
    entry_from.insert(0, "Sofia")
    entry_date.set_date(datetime.date.today())
    var_ignore_date.set(False)
    #Изчистване на резервацията
    entry_pass.delete(0, tk.END)
    entry_flight.delete(0, tk.END)
    entry_seat.delete(0, tk.END)
    entry_price.delete(0, tk.END)
    for row in tree.get_children():
        tree.delete(row)


#Автоматично попълване при клик
def on_tree_select(event):
    selected_item = tree.selection()
    if not selected_item:
        return

    flight_data = tree.item(selected_item[0])['values']

    #Попълваме автоматично Полет ID и Цена
    entry_flight.delete(0, tk.END)
    entry_flight.insert(0, flight_data[0]) 

    entry_price.delete(0, tk.END)
    entry_price.insert(0, flight_data[6]) 


#Функция за резервация
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
root.geometry("1150x850")
root.configure(bg="#f4f7f9")

header_frame = tk.Frame(root, bg="#0052ff", pady=20)
header_frame.pack(fill=tk.X)

search_box = tk.LabelFrame(header_frame, text=" Търсене на полети ", bg="white", padx=20, pady=15)
search_box.pack(padx=50, fill=tk.X)
#Дефинираме променливата за типа полет
var_flight_type = tk.IntVar(value=2) #2 е за 'Еднопосочен' по подразбиране

#Полета за търсене
tk.Label(search_box, text="Откъде:", bg="white").grid(row=0, column=0, sticky="w")
entry_from = tk.Entry(search_box, width=18);
entry_from.insert(0, "Sofia");
entry_from.grid(row=1, column=0, padx=5)

#Контейнер за радио бутоните
type_frame = tk.Frame(search_box, bg="white")
type_frame.grid(row=0, column=0, columnspan=4, sticky="w", pady=5)

#Самите бутони - ЗАДЪЛЖИТЕЛНО с .pack() или .grid()
tk.Radiobutton(type_frame, text="Двупосочен", variable=var_flight_type,
               value=1, bg="white").pack(side=tk.LEFT)
tk.Radiobutton(type_frame, text="Еднопосочен", variable=var_flight_type,
               value=2, bg="white").pack(side=tk.LEFT, padx=30)

tk.Label(search_box, text="", bg="white").grid(row=0, column=1, sticky="w")
entry_to = tk.Entry(search_box, width=18);
entry_to.grid(row=1, column=1, padx=5)

entry_date = DateEntry(search_box, width=15, background='darkblue', foreground='white', date_pattern='yyyy-mm-dd')
entry_date.grid(row=1, column=2, padx=5)

var_ignore_date = tk.BooleanVar()
tk.Checkbutton(search_box, text="Всички дати", variable=var_ignore_date, bg="white").grid(row=2, column=2, sticky="w")

btn_search = tk.Button(search_box, text="ТЪРСИ", bg="#ff6b00", fg="white", font=("Arial", 11, "bold"), width=12,
                       command=search_flights)
btn_search.grid(row=1, column=3, padx=10)

btn_clear = tk.Button(search_box, text="ИЗЧИСТИ", command=clear_all, width=10).grid(row=1, column=4)

#Таблица
results_frame = tk.Frame(root, bg="#f4f7f9", pady=10)
results_frame.pack(fill=tk.BOTH, expand=True, padx=50)

columns = ("ID", "Полет №", "Дестинация", "Дата", "Час", "Свободни места", "Цена", "Тип")
tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=130, anchor=tk.CENTER)
tree.bind('<<TreeviewSelect>>', on_tree_select)
tree.pack(fill=tk.X)

#Резервация
res_box = tk.LabelFrame(root, text=" Детайли за резервация ", bg="white", padx=20, pady=15)
res_box.pack(padx=50, pady=20, fill=tk.X)

tk.Label(res_box, text="Пътник ID:").grid(row=0, column=0);
entry_pass = tk.Entry(res_box, width=8);
entry_pass.grid(row=0, column=1, padx=5)
tk.Label(res_box, text="Полет ID:").grid(row=0, column=2);
entry_flight = tk.Entry(res_box, width=8);
entry_flight.grid(row=0, column=3, padx=5)
tk.Label(res_box, text="Място:").grid(row=0, column=4);
entry_seat = tk.Entry(res_box, width=8);
entry_seat.grid(row=0, column=5, padx=5)
tk.Label(res_box, text="Цена:").grid(row=0, column=6);
entry_price = tk.Entry(res_box, width=8);
entry_price.grid(row=0, column=7, padx=5)

btn_book = tk.Button(res_box, text="ПОТВЪРДИ", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                     command=make_reservation)
btn_book.grid(row=0, column=8, padx=20)

root.mainloop()
