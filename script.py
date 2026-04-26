import tkinter as tk  # Библиотека за създаване на GUI
from tkinter import messagebox, ttk  # Инструменти за изскачащи съобщения
import psycopg2  # Драйвер за връзка с PostgreSQL
from psycopg2 import extras
from tkcalendar import DateEntry  # Визуален календар
import datetime  # Библиотека за работа с дати и час

# Конфигурация на базата данни
DB_CONFIG = {
    "user": "postgres",
    "password": "11062004",
    "host": "127.0.0.1",
    "port": "5432",
    "database": "Airport_DB"
}


# Установяване на връзка с базата
def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        messagebox.showerror("Грешка", f"Връзката се провали: {e}")
        return None


class AirportApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Система за авиационен мениджмънт")
        self.root.geometry("1200x850")
        self.root.configure(bg="#f4f7f9")

        # Стилизиране
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", rowheight=30, font=("Arial", 10))
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.setup_tabs()

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Таб 1: Търсене и Резервация
        self.tab_main = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_main, text=" ✈️ Полети и Резервации ")
        self.setup_main_tab()

        # Таб 2: Администрация
        self.tab_admin = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_admin, text=" ⚙️ Администрация (CRUD) ")
        self.setup_admin_tab()

        # Таб 3: Справки
        self.tab_reports = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_reports, text=" 📊 Аналитични Справки ")
        self.setup_reports_tab()

    def setup_main_tab(self):
        # Хедър
        header_frame = tk.Frame(self.tab_main, bg="#0052ff", pady=20)
        header_frame.pack(fill=tk.X)

        # Търсене
        search_box = tk.LabelFrame(header_frame, text=" Търсене на полети ", bg="white", padx=20, pady=15)
        search_box.pack(padx=50, fill=tk.X)

        self.var_flight_type = tk.IntVar(value=2)  # 2 е за 'Еднопосочен' по подразбиране
        self.var_ignore_date = tk.BooleanVar(value=False)

        tk.Label(search_box, text="Дестинация:", bg="white").grid(row=0, column=0, sticky="w")
        self.entry_to = tk.Entry(search_box, width=18)
        self.entry_to.grid(row=1, column=0, padx=5)

        # Тип полет
        type_frame = tk.Frame(search_box, bg="white")
        type_frame.grid(row=0, column=1, columnspan=2, sticky="w")
        tk.Radiobutton(type_frame, text="Двупосочен", variable=self.var_flight_type, value=1, bg="white").pack(
            side=tk.LEFT)
        tk.Radiobutton(type_frame, text="Еднопосочен", variable=self.var_flight_type, value=2, bg="white").pack(
            side=tk.LEFT, padx=20)

        tk.Label(search_box, text="Дата:", bg="white").grid(row=0, column=3, sticky="w")
        self.entry_date = DateEntry(search_box, width=15, background='darkblue', foreground='white',
                                    date_pattern='yyyy-mm-dd')
        self.entry_date.grid(row=1, column=3, padx=5)

        tk.Checkbutton(search_box, text="Всички дати", variable=self.var_ignore_date, bg="white").grid(row=2, column=3,
                                                                                                       sticky="w")

        tk.Button(search_box, text="ТЪРСИ", bg="#ff6b00", fg="white", font=("Arial", 11, "bold"), width=12,
                  command=self.search_flights).grid(row=1, column=4, padx=10)
        tk.Button(search_box, text="ИЗЧИСТИ", command=self.clear_all, width=10).grid(row=1, column=5)

        # Таблица с резултати
        results_frame = tk.Frame(self.tab_main, bg="#f4f7f9", pady=10)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=50)

        columns = ("ID", "Полет №", "Дестинация", "Дата", "Час", "Свободни места", "Цена", "Тип")
        self.tree = ttk.Treeview(results_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_column(c, False))
            self.tree.column(col, width=130, anchor=tk.CENTER)
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

        # Резервация
        res_box = tk.LabelFrame(self.tab_main, text=" Детайли за резервация ", bg="white", padx=20, pady=15)
        res_box.pack(padx=50, pady=20, fill=tk.X)

        self.ent_pass = tk.Entry(res_box, width=8);
        tk.Label(res_box, text="Пътник ID:").grid(row=0, column=0);
        self.ent_pass.grid(row=0, column=1, padx=5)
        self.ent_flight = tk.Entry(res_box, width=8);
        tk.Label(res_box, text="Полет ID:").grid(row=0, column=2);
        self.ent_flight.grid(row=0, column=3, padx=5)
        self.ent_seat = tk.Entry(res_box, width=8);
        tk.Label(res_box, text="Място:").grid(row=0, column=4);
        self.ent_seat.grid(row=0, column=5, padx=5)
        self.ent_price = tk.Entry(res_box, width=8);
        tk.Label(res_box, text="Цена:").grid(row=0, column=6);
        self.ent_price.grid(row=0, column=7, padx=5)

        tk.Button(res_box, text="ПОТВЪРДИ", bg="#27ae60", fg="white", font=("Arial", 10, "bold"),
                  command=self.make_reservation).grid(row=0, column=8, padx=20)

    def setup_admin_tab(self):
        # Администрация
        admin_frame = tk.Frame(self.tab_admin, bg="white", padx=30, pady=30)
        admin_frame.pack(fill="both", expand=True)

        tk.Label(admin_frame, text="Административно управление (CRUD)", font=("Arial", 14, "bold"), bg="white").pack(
            pady=10)

        # Пътници
        p_frame = tk.LabelFrame(admin_frame, text=" Управление на Пътници ", bg="white", padx=10, pady=10)
        p_frame.pack(fill="x", pady=10)
        tk.Button(p_frame, text="➕ Добави / Обнови Пътник (CALL upsert_passenger)",
                  command=self.open_passenger_crud).pack(side="left", padx=10)

        # Самолети
        a_frame = tk.LabelFrame(admin_frame, text=" Управление на Самолети ", bg="white", padx=10, pady=10)
        a_frame.pack(fill="x", pady=10)
        tk.Button(a_frame, text="✏️ Обнови технически данни (CALL update_aircraft_details)",
                  command=self.open_aircraft_crud).pack(side="left", padx=10)

        # Полети (Безопасно изтриване)
        f_frame = tk.LabelFrame(admin_frame, text=" Управление на Полети ", bg="white", padx=10, pady=10)
        f_frame.pack(fill="x", pady=10)
        tk.Button(f_frame, text="🗑️ Безопасно изтриване на полет (CALL delete_flight_safe)", bg="#e74c3c", fg="white",
                  command=self.open_delete_flight).pack(side="left", padx=10)

    def setup_reports_tab(self):
        # Справки
        reports_frame = tk.Frame(self.tab_reports, bg="#f4f7f9", padx=20, pady=20)
        reports_frame.pack(fill="both", expand=True)

        tk.Label(reports_frame, text="Аналитични справки и отчети", font=("Arial", 14, "bold"), bg="#f4f7f9").pack(
            pady=10)

        grid_frame = tk.Frame(reports_frame, bg="#f4f7f9")
        grid_frame.pack()

        reps = [
            ("1. Топ 3 Дестинации (Агрегация)",
             "SELECT destination, COUNT(*) FROM ticket t JOIN flight f ON t.flight_id = f.flight_id GROUP BY destination ORDER BY 2 DESC LIMIT 3"),
            ("2. Пътници в Boeing (Вложена)",
             "SELECT first_name, last_name FROM passenger WHERE passenger_id IN (SELECT passenger_id FROM ticket t JOIN flight f ON t.flight_id = f.flight_id JOIN aircraft a ON f.aircraft_id = a.aircraft_id WHERE a.model LIKE 'Boeing%')"),
            ("3. Полети 100-500лв (Диапазон)", "SELECT * FROM flight WHERE base_price BETWEEN 100 AND 500"),
            ("4. Приходи по Авиолинии (Join/Group)",
             "SELECT airline, SUM(actual_price) FROM aircraft a JOIN flight f ON a.aircraft_id = f.aircraft_id JOIN ticket t ON f.flight_id = t.flight_id GROUP BY airline"),
            ("5. Екипаж на полет FB101 (Join)",
             "SELECT e.first_name, e.last_name, ca.role FROM employee e JOIN crew_assignment ca ON e.employee_id = ca.employee_id JOIN flight f ON ca.flight_id = f.flight_id WHERE f.flight_number = 'FB101'"),
            ("6. Продажби (Последни 30 дни)",
             "SELECT * FROM ticket WHERE purchase_date >= CURRENT_DATE - INTERVAL '30 days'"),
            ("7. Заетост (Курсор)", "SELECT * FROM flight_report_cursor()"),
            ("8. Лоялни клиенти (Функция)", "SELECT * FROM find_frequent_travelers()")
        ]

        for i, (name, sql) in enumerate(reps):
            btn = tk.Button(grid_frame, text=name, width=40, height=2, bg="#34495e", fg="white",
                            font=("Arial", 9, "bold"), command=lambda s=sql: self.run_report(s))
            btn.grid(row=i // 2, column=i % 2, padx=10, pady=10)

    # Логика за търсене
    def search_flights(self):
        for row in self.tree.get_children(): self.tree.delete(row)
        dest = self.entry_to.get().strip()
        selected_date = self.entry_date.get_date()
        ignore_date = self.var_ignore_date.get()
        is_rt_value = True if self.var_flight_type.get() == 1 else False

        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            try:
                query = "SELECT flight_id, flight_number, destination, flight_date, flight_time, get_available_seats(flight_id), base_price, is_round_trip FROM flight WHERE destination ILIKE %s AND is_round_trip = %s"
                params = [f'%{dest}%', is_rt_value]
                if not ignore_date:
                    query += " AND flight_date = %s"
                    params.append(selected_date)
                query += " ORDER BY flight_date ASC"
                cursor.execute(query, tuple(params))
                results = cursor.fetchall()
                for i, row in enumerate(results):
                    display_row = list(row)
                    display_row[7] = "Двупосочен" if display_row[7] else "Еднопосочен"
                    tag = 'oddrow' if i % 2 == 0 else 'evenrow'
                    self.tree.insert("", tk.END, values=display_row, tags=(tag,))
                if not results: messagebox.showinfo("Търсене", "Няма намерени полети.")
            except Exception as e:
                messagebox.showerror("Грешка", str(e))
            finally:
                cursor.close(); conn.close()

    def clear_all(self):
        self.entry_to.delete(0, tk.END)
        self.entry_date.set_date(datetime.date.today())
        self.var_ignore_date.set(False)
        self.ent_pass.delete(0, tk.END);
        self.ent_flight.delete(0, tk.END)
        self.ent_seat.delete(0, tk.END);
        self.ent_price.delete(0, tk.END)
        for row in self.tree.get_children(): self.tree.delete(row)

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel: return
        data = self.tree.item(sel[0])['values']
        self.ent_flight.delete(0, tk.END);
        self.ent_flight.insert(0, data[0])
        self.ent_price.delete(0, tk.END);
        self.ent_price.insert(0, data[6])

    def make_reservation(self):
        data = (self.ent_pass.get(), self.ent_flight.get(), self.ent_seat.get(), self.ent_price.get())
        if not all(data): messagebox.showwarning("Внимание", "Попълнете всички полета!"); return
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("CALL book_ticket(%s, %s, %s, %s)", data)
                conn.commit()
                messagebox.showinfo("Успех", "Резервацията е потвърдена!")
                self.search_flights()
            except Exception as e:
                error_msg = str(e).split('\n')[0].replace("P0001:", "").strip()
                messagebox.showerror("Грешка", error_msg)
            finally:
                cursor.close(); conn.close()

    def sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)
        for index, (val, k) in enumerate(l): self.tree.move(k, '', index)
        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    # --- ЛОГИКА АДМИН (CRUD) ---
    def open_passenger_crud(self):
        win = tk.Toplevel(self.root);
        win.title("Управление на Пътници")
        tk.Label(win, text="Passenger ID (0 за нов):").grid(row=0, column=0)
        e_id = tk.Entry(win);
        e_id.grid(row=0, column=1)
        tk.Label(win, text="Име:").grid(row=1, column=0);
        e_f = tk.Entry(win);
        e_f.grid(row=1, column=1)
        tk.Label(win, text="Фамилия:").grid(row=2, column=0);
        e_l = tk.Entry(win);
        e_l.grid(row=2, column=1)
        tk.Label(win, text="Паспорт:").grid(row=3, column=0);
        e_p = tk.Entry(win);
        e_p.grid(row=3, column=1)
        tk.Label(win, text="Националност:").grid(row=4, column=0);
        e_n = tk.Entry(win);
        e_n.grid(row=4, column=1)

        def save():
            conn = get_db_connection();
            cur = conn.cursor()
            try:
                cur.execute("CALL upsert_passenger(%s, %s, %s, %s, %s)",
                            (int(e_id.get()), e_f.get(), e_l.get(), e_p.get(), e_n.get()))
                conn.commit();
                messagebox.showinfo("Успех", "Данните са записани.");
                win.destroy()
            except Exception as e:
                messagebox.showerror("Грешка", str(e))
            finally:
                conn.close()

        tk.Button(win, text="ЗАПАЗИ", bg="green", fg="white", command=save).grid(row=5, columnspan=2, pady=10)

    def open_aircraft_crud(self):
        win = tk.Toplevel(self.root);
        win.title("Управление на Самолети")
        tk.Label(win, text="Aircraft ID:").grid(row=0, column=0);
        e_id = tk.Entry(win);
        e_id.grid(row=0, column=1)
        tk.Label(win, text="Модел:").grid(row=1, column=0);
        e_m = tk.Entry(win);
        e_m.grid(row=1, column=1)
        tk.Label(win, text="Капацитет:").grid(row=2, column=0);
        e_c = tk.Entry(win);
        e_c.grid(row=2, column=1)
        tk.Label(win, text="Авиолиния:").grid(row=3, column=0);
        e_a = tk.Entry(win);
        e_a.grid(row=3, column=1)

        def update():
            conn = get_db_connection();
            cur = conn.cursor()
            try:
                cur.execute("CALL update_aircraft_details(%s, %s, %s, %s)",
                            (int(e_id.get()), e_m.get(), int(e_c.get()), e_a.get()))
                conn.commit();
                messagebox.showinfo("Успех", "Данните са обновени.");
                win.destroy()
            except Exception as e:
                messagebox.showerror("Грешка", str(e))
            finally:
                conn.close()

        tk.Button(win, text="ОБНОВИ", bg="blue", fg="white", command=update).grid(row=4, columnspan=2, pady=10)

    def open_delete_flight(self):
        win = tk.Toplevel(self.root);
        win.title("Изтриване на полет")
        tk.Label(win, text="Flight ID за изтриване:").pack(pady=5)
        e_id = tk.Entry(win);
        e_id.pack(pady=5)

        def delete():
            if messagebox.askyesno("Потвърждение", "Сигурни ли сте? Всички билети за този полет ще бъдат изтрити!"):
                conn = get_db_connection();
                cur = conn.cursor()
                try:
                    cur.execute("CALL delete_flight_safe(%s)", (int(e_id.get()),))
                    conn.commit();
                    messagebox.showinfo("Успех", "Полетът е изтрит.");
                    win.destroy()
                except Exception as e:
                    messagebox.showerror("Грешка", str(e))
                finally:
                    conn.close()

        tk.Button(win, text="ИЗТРИЙ", bg="red", fg="white", command=delete).pack(pady=10)

    # Логика за справки
    def run_report(self, sql):
        win = tk.Toplevel(self.root);
        win.title("Резултат от справка")
        win.geometry("800x400")
        txt = tk.Text(win, padx=10, pady=10, font=("Consolas", 10))
        txt.pack(fill="both", expand=True)
        conn = get_db_connection()
        if conn:
            cur = conn.cursor()
            try:
                cur.execute(sql)
                rows = cur.fetchall()
                if not rows:
                    txt.insert("end", "Няма намерени резултати.")
                else:
                    for r in rows: txt.insert("end", f"{r}\n")
            except Exception as e:
                txt.insert("end", f"Грешка: {e}")
            finally:
                conn.close()


if __name__ == "__main__":
    root = tk.Tk()
    app = AirportApp(root)
    root.mainloop()
