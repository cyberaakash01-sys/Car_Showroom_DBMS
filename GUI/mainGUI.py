import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import pandas as pd
import sqlalchemy as sa
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

# Ensure parent directory is in sys.path to import dbms and analysis modules
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from dbms import mysql_connection
except ImportError:
    def mysql_connection():
        return sa.create_engine("sqlite:///:memory:")

class CarShowroomGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Car Showroom DBMS - Desktop Application")
        self.geometry("1280x820")
        self.minsize(1024, 700)

        # Theme Colors (Dark Theme)
        self.colors = {
            "bg_dark": "#11111b",
            "sidebar": "#181825",
            "card_bg": "#1e1e2e",
            "card_border": "#313244",
            "accent": "#89b4fa",
            "accent_hover": "#74c7ec",
            "text_main": "#cdd6f4",
            "text_sub": "#a6adc8",
            "table_heading": "#313244",
            "success": "#a6e3a1",
            "warning": "#f9e2af",
            "danger": "#f38ba8",
            "entry_bg": "#313244",
            "entry_fg": "#cdd6f4"
        }

        self.configure(bg=self.colors["bg_dark"])
        self._setup_styles()

        # Engine Cache
        self.engine = None
        self.is_connected = False
        self._init_db_connection()

        # Main Container
        self.container = tk.Frame(self, bg=self.colors["bg_dark"])
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        self.show_login_frame()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use("clam")

        # Treeview styling
        self.style.configure("Treeview",
                             background=self.colors["card_bg"],
                             foreground=self.colors["text_main"],
                             fieldbackground=self.colors["card_bg"],
                             rowheight=32,
                             font=("Segoe UI", 10))
        self.style.map("Treeview",
                       background=[('selected', self.colors["accent"])],
                       foreground=[('selected', '#11111b')])

        self.style.configure("Treeview.Heading",
                             background=self.colors["table_heading"],
                             foreground=self.colors["text_main"],
                             font=("Segoe UI", 10, "bold"),
                             borderwidth=1)
        self.style.map("Treeview.Heading",
                       background=[('active', self.colors["accent_hover"])])

        # Scrollbar style
        self.style.configure("Vertical.TScrollbar",
                             background=self.colors["card_border"],
                             troughcolor=self.colors["bg_dark"],
                             borderwidth=0,
                             arrowcolor=self.colors["text_sub"])

        # Combobox style
        self.style.configure("TCombobox",
                             fieldbackground=self.colors["entry_bg"],
                             background=self.colors["card_border"],
                             foreground=self.colors["entry_fg"],
                             darkcolor=self.colors["card_border"],
                             lightcolor=self.colors["card_border"])

    def _init_db_connection(self):
        try:
            self.engine = mysql_connection()
            # Test connection
            with self.engine.connect() as conn:
                pass
            self.is_connected = True
        except Exception as e:
            self.is_connected = False
            self.db_error_msg = str(e)

    def show_login_frame(self):
        for widget in self.container.winfo_children():
            widget.destroy()

        login_frame = tk.Frame(self.container, bg=self.colors["bg_dark"])
        login_frame.pack(fill="both", expand=True)

        # Center Card
        card = tk.Frame(login_frame, bg=self.colors["card_bg"], highlightbackground=self.colors["card_border"], highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=480)

        # Logo / Title
        tk.Label(card, text="🚗", font=("Segoe UI", 48), bg=self.colors["card_bg"]).pack(pady=(30, 5))
        tk.Label(card, text="CAR SHOWROOM DBMS", font=("Segoe UI", 18, "bold"), fg=self.colors["accent"], bg=self.colors["card_bg"]).pack(pady=5)
        tk.Label(card, text="Admin Login Gateway", font=("Segoe UI", 10), fg=self.colors["text_sub"], bg=self.colors["card_bg"]).pack(pady=(0, 25))

        # Username Input
        tk.Label(card, text="Username", font=("Segoe UI", 10, "bold"), fg=self.colors["text_main"], bg=self.colors["card_bg"], anchor="w").pack(fill="x", padx=40)
        un_entry = tk.Entry(card, font=("Segoe UI", 11), bg=self.colors["entry_bg"], fg=self.colors["entry_fg"], insertbackground=self.colors["text_main"], relief="flat")
        un_entry.pack(fill="x", padx=40, pady=(5, 15), ipady=6)
        un_entry.insert(0, "ADMIN")

        # Password Input
        tk.Label(card, text="Password", font=("Segoe UI", 10, "bold"), fg=self.colors["text_main"], bg=self.colors["card_bg"], anchor="w").pack(fill="x", padx=40)
        pw_entry = tk.Entry(card, font=("Segoe UI", 11), show="•", bg=self.colors["entry_bg"], fg=self.colors["entry_fg"], insertbackground=self.colors["text_main"], relief="flat")
        pw_entry.pack(fill="x", padx=40, pady=(5, 20), ipady=6)
        pw_entry.insert(0, "cars")

        # Status Label
        status_lbl = tk.Label(card, text="", font=("Segoe UI", 9), fg=self.colors["danger"], bg=self.colors["card_bg"])
        status_lbl.pack(pady=(0, 10))

        def attempt_login():
            un = un_entry.get().strip()
            pw = pw_entry.get().strip()
            if un == "ADMIN" and pw == "cars":
                self.show_main_app()
            else:
                status_lbl.config(text="Invalid Username or Password! Try again.")

        login_btn = tk.Button(card, text="LOGIN TO SYSTEM", font=("Segoe UI", 11, "bold"), bg=self.colors["accent"], fg="#11111b", activebackground=self.colors["accent_hover"], activeforeground="#11111b", relief="flat", cursor="hand2", command=attempt_login)
        login_btn.pack(fill="x", padx=40, ipady=8, pady=(0, 20))

        # Enter Key listener
        self.bind("<Return>", lambda event: attempt_login())

    def show_main_app(self):
        self.unbind("<Return>")
        for widget in self.container.winfo_children():
            widget.destroy()

        # Header Bar
        header = tk.Frame(self.container, bg=self.colors["card_bg"], height=60)
        header.pack(side="top", fill="x")

        title_lbl = tk.Label(header, text="🚗 CAR SHOWROOM MANAGEMENT SYSTEM", font=("Segoe UI", 14, "bold"), fg=self.colors["accent"], bg=self.colors["card_bg"])
        title_lbl.pack(side="left", padx=20, pady=15)

        # Connection Badge
        conn_text = "● DB Connected" if self.is_connected else "⚠️ MySQL Disconnected (Sample/Local Mode)"
        conn_color = self.colors["success"] if self.is_connected else self.colors["warning"]
        conn_lbl = tk.Label(header, text=conn_text, font=("Segoe UI", 9, "bold"), fg=conn_color, bg=self.colors["card_bg"])
        conn_lbl.pack(side="left", padx=10)

        # User tag & Logout
        user_lbl = tk.Label(header, text="👤 Admin", font=("Segoe UI", 10, "bold"), fg=self.colors["text_main"], bg=self.colors["card_bg"])
        user_lbl.pack(side="right", padx=(10, 20))

        logout_btn = tk.Button(header, text="Logout", font=("Segoe UI", 9, "bold"), bg=self.colors["danger"], fg="#11111b", activebackground="#f5c2e7", relief="flat", cursor="hand2", command=self.show_login_frame)
        logout_btn.pack(side="right", padx=10)

        # Main Body Layout (Sidebar + Content)
        body = tk.Frame(self.container, bg=self.colors["bg_dark"])
        body.pack(side="top", fill="both", expand=True)

        # Sidebar
        sidebar = tk.Frame(body, bg=self.colors["sidebar"], width=230)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Content Stack Frame
        self.content_area = tk.Frame(body, bg=self.colors["bg_dark"])
        self.content_area.pack(side="right", fill="both", expand=True, padx=15, pady=15)

        # Navigation Options
        self.nav_buttons = {}
        nav_items = [
            ("dashboard", "📊 Dashboard"),
            ("cars", "🚗 Cars Info"),
            ("customers", "👤 Customers"),
            ("employees", "👨‍💼 Employees"),
            ("orders", "📦 Orders"),
            ("payments", "💳 Payments"),
            ("analytics", "📈 Analytics")
        ]

        tk.Label(sidebar, text="NAVIGATION", font=("Segoe UI", 8, "bold"), fg=self.colors["text_sub"], bg=self.colors["sidebar"]).pack(anchor="w", padx=20, pady=(20, 10))

        for key, label in nav_items:
            btn = tk.Button(sidebar, text=f"  {label}", font=("Segoe UI", 10, "bold"), anchor="w", bg=self.colors["sidebar"], fg=self.colors["text_sub"], activebackground=self.colors["card_bg"], activeforeground=self.colors["accent"], relief="flat", cursor="hand2", command=lambda k=key: self.switch_tab(k))
            btn.pack(fill="x", padx=10, pady=3, ipady=6)
            self.nav_buttons[key] = btn

        # Initialize View Frames
        self.views = {
            "dashboard": self._create_dashboard_view(),
            "cars": self._create_table_view("cars", ["Car_Id", "Car_Name", "Company", "Car_Type", "Fuel_Type", "Price($)", "Engine_Type", "Power(HP)"]),
            "customers": self._create_table_view("customers", ["Customer_Id", "Customer_Name", "Phone_Number", "City", "Address"]),
            "employees": self._create_table_view("employees", ["Employee_Id", "Employee_Name", "Phone_Number", "Designation", "Salary"]),
            "orders": self._create_table_view("orders", ["Order_Id", "Customer_Id", "Car_Id", "Employee_Id", "Order_Date", "Total_Amount"]),
            "payments": self._create_table_view("payments", ["Payment_Id", "Order_Id", "Payment_Method", "Payment_Status", "Amount", "Payment_Date"]),
            "analytics": self._create_analytics_view()
        }

        self.switch_tab("dashboard")

    def switch_tab(self, tab_key):
        for key, btn in self.nav_buttons.items():
            if key == tab_key:
                btn.config(bg=self.colors["card_bg"], fg=self.colors["accent"])
            else:
                btn.config(bg=self.colors["sidebar"], fg=self.colors["text_sub"])

        for key, frame in self.views.items():
            if key == tab_key:
                frame.pack(fill="both", expand=True)
                if hasattr(frame, "refresh_data"):
                    frame.refresh_data()
            else:
                frame.pack_forget()

    # --- DB Fetching Helper ---
    def get_table_df(self, table_name, default_cols=None):
        if self.is_connected and self.engine:
            try:
                df = pd.read_sql(f"SELECT * FROM `{table_name}`", self.engine)
                return df
            except Exception as e:
                pass

        # Sample Fallback Data if local database engine has no tables yet or connection offline
        sample_data = {
            "cars": pd.DataFrame([
                [101, "City", "Honda", "Sedan", "Petrol", 15000, "VTEC 1.5", 119],
                [102, "Creta", "Hyundai", "SUV", "Petrol", 18000, "1.5 MPI", 113],
                [103, "Fortuner", "Toyota", "SUV", "Diesel", 45000, "2.8L", 201],
                [104, "Mustang", "Ford", "Coupe", "Petrol", 65000, "5.0 V8", 450],
                [105, "Model 3", "Tesla", "Sedan", "Electric", 52000, "Dual Motor", 450]
            ], columns=["Car_Id", "Car_Name", "Company", "Car_Type", "Fuel_Type", "Price($)", "Engine_Type", "Power(HP)"]),

            "customers": pd.DataFrame([
                [1, "Aakash Samai", "9876543210", "Delhi", "Connaught Place"],
                [2, "Rahul Sharma", "9811223344", "Mumbai", "Bandra West"],
                [3, "Priya Patel", "9722334455", "Ahmedabad", "CG Road"]
            ], columns=["Customer_Id", "Customer_Name", "Phone_Number", "City", "Address"]),

            "employees": pd.DataFrame([
                [10, "Vikram Singh", "9988776655", "Sales Manager", 65000],
                [11, "Neha Gupta", "9977665544", "Sales Executive", 42000],
                [12, "Rohan Verma", "9966554433", "Service Technician", 35000]
            ], columns=["Employee_Id", "Employee_Name", "Phone_Number", "Designation", "Salary"]),

            "orders": pd.DataFrame([
                [5001, 1, 101, 11, "2026-01-15", 15000],
                [5002, 2, 103, 10, "2026-02-10", 45000],
                [5003, 3, 102, 11, "2026-02-20", 18000]
            ], columns=["Order_Id", "Customer_Id", "Car_Id", "Employee_Id", "Order_Date", "Total_Amount"]),

            "payments": pd.DataFrame([
                [901, 5001, "Credit Card", "Paid", 15000, "2026-01-15"],
                [902, 5002, "Bank Transfer", "EMI", 15000, "2026-02-10"],
                [903, 5003, "UPI", "Pending", 18000, "2026-02-20"]
            ], columns=["Payment_Id", "Order_Id", "Payment_Method", "Payment_Status", "Amount", "Payment_Date"])
        }

        if table_name in sample_data:
            return sample_data[table_name]
        elif default_cols:
            return pd.DataFrame(columns=default_cols)
        return pd.DataFrame()

    # --- Dashboard View ---
    def _create_dashboard_view(self):
        view = tk.Frame(self.content_area, bg=self.colors["bg_dark"])

        # Title
        tk.Label(view, text="Dashboard Overview", font=("Segoe UI", 16, "bold"), fg=self.colors["text_main"], bg=self.colors["bg_dark"]).pack(anchor="w", pady=(0, 15))

        cards_frame = tk.Frame(view, bg=self.colors["bg_dark"])
        cards_frame.pack(fill="x", pady=(0, 20))

        self.kpi_labels = {}
        metrics = [
            ("cars", "Total Cars", "🚗", self.colors["accent"]),
            ("customers", "Customers", "👤", self.colors["success"]),
            ("employees", "Employees", "👨‍💼", self.colors["warning"]),
            ("orders", "Total Orders", "📦", "#f5c2e7"),
            ("payments", "Total Revenue", "💳", "#cba6f7")
        ]

        for idx, (key, title, icon, color) in enumerate(metrics):
            card = tk.Frame(cards_frame, bg=self.colors["card_bg"], highlightbackground=self.colors["card_border"], highlightthickness=1)
            card.grid(row=0, column=idx, padx=8, sticky="nsew")
            cards_frame.grid_columnconfigure(idx, weight=1)

            top_line = tk.Frame(card, bg=color, height=4)
            top_line.pack(fill="x")

            tk.Label(card, text=f"{icon} {title}", font=("Segoe UI", 10, "bold"), fg=self.colors["text_sub"], bg=self.colors["card_bg"]).pack(anchor="w", padx=12, pady=(10, 2))
            lbl = tk.Label(card, text="0", font=("Segoe UI", 20, "bold"), fg=self.colors["text_main"], bg=self.colors["card_bg"])
            lbl.pack(anchor="w", padx=12, pady=(0, 12))
            self.kpi_labels[key] = lbl

        # Chart Preview on Dashboard
        chart_card = tk.Frame(view, bg=self.colors["card_bg"], highlightbackground=self.colors["card_border"], highlightthickness=1)
        chart_card.pack(fill="both", expand=True)

        tk.Label(chart_card, text="📊 Quick Fleet & Orders Summary", font=("Segoe UI", 12, "bold"), fg=self.colors["accent"], bg=self.colors["card_bg"]).pack(anchor="w", padx=15, pady=10)

        chart_container = tk.Frame(chart_card, bg=self.colors["card_bg"])
        chart_container.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh_dashboard():
            cars_df = self.get_table_df("cars")
            cust_df = self.get_table_df("customers")
            emp_df = self.get_table_df("employees")
            orders_df = self.get_table_df("orders")
            pay_df = self.get_table_df("payments")

            self.kpi_labels["cars"].config(text=str(len(cars_df)))
            self.kpi_labels["customers"].config(text=str(len(cust_df)))
            self.kpi_labels["employees"].config(text=str(len(emp_df)))
            self.kpi_labels["orders"].config(text=str(len(orders_df)))

            if "Amount" in pay_df.columns:
                total_rev = pay_df["Amount"].sum()
                self.kpi_labels["payments"].config(text=f"${total_rev:,.0f}")
            else:
                self.kpi_labels["payments"].config(text="$0")

            # Render Chart
            for w in chart_container.winfo_children():
                w.destroy()

            plt.close('all')
            fig = Figure(figsize=(9, 3.8), facecolor=self.colors["card_bg"])
            ax1 = fig.add_subplot(121)
            ax2 = fig.add_subplot(122)
            ax1.set_facecolor(self.colors["card_bg"])
            ax2.set_facecolor(self.colors["card_bg"])
            for spine in ax1.spines.values():
                spine.set_color(self.colors["card_border"])
            for spine in ax2.spines.values():
                spine.set_color(self.colors["card_border"])
            
            # Helper to find column case-insensitively
            def find_col(df, names):
                if df.empty:
                    return None
                for n in names:
                    for col in df.columns:
                        if col.lower().strip() == n.lower().strip():
                            return col
                return None

            # Subplot 1: Cars by Company
            comp_col = find_col(cars_df, ["Company", "company"])
            if not cars_df.empty and comp_col:
                comp_counts = cars_df[comp_col].value_counts()
                ax1.bar(comp_counts.index, comp_counts.values, color=self.colors["accent"])
                ax1.set_title("Cars by Brand/Company", color=self.colors["text_main"], fontsize=10, fontweight="bold")
                ax1.tick_params(colors=self.colors["text_sub"], labelsize=8)
            else:
                ax1.text(0.5, 0.5, "No Car Stock Data", ha="center", va="center", color=self.colors["text_sub"], fontsize=10)
                ax1.set_xticks([])
                ax1.set_yticks([])

            # Subplot 2: Payment Status
            status_col = find_col(pay_df, ["Payment_Status", "payment_status", "status"])
            if not pay_df.empty and status_col:
                p_status = pay_df[status_col].value_counts()
                pie_res = ax2.pie(p_status.values, labels=p_status.index, colors=[self.colors["success"], self.colors["warning"], self.colors["danger"]], autopct='%1.0f%%', textprops={'color': self.colors["text_main"], 'fontsize': 9, 'weight': 'bold'})
                if len(pie_res) == 3:
                    for at in pie_res[2]:
                        at.set_color("#11111b")
                        at.set_fontsize(10)
                        at.set_weight("bold")
                ax2.set_title("Payment Status Breakdown", color=self.colors["text_main"], fontsize=10, fontweight="bold")
            else:
                ax2.text(0.5, 0.5, "No Payment Records Yet", ha="center", va="center", color=self.colors["text_sub"], fontsize=10)
                ax2.set_xticks([])
                ax2.set_yticks([])

            fig.tight_layout()

            canvas = FigureCanvasTkAgg(fig, master=chart_container)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

        view.refresh_data = refresh_dashboard
        return view

    # --- Generic Table View Component ---
    def _create_table_view(self, table_name, default_cols):
        view = tk.Frame(self.content_area, bg=self.colors["bg_dark"])

        # Header Control Bar
        ctrl_bar = tk.Frame(view, bg=self.colors["bg_dark"])
        ctrl_bar.pack(fill="x", pady=(0, 10))

        tk.Label(ctrl_bar, text=f"{table_name.capitalize()} Data Table", font=("Segoe UI", 16, "bold"), fg=self.colors["text_main"], bg=self.colors["bg_dark"]).pack(side="left")

        # Search Bar
        tk.Label(ctrl_bar, text="🔍 Search:", font=("Segoe UI", 10, "bold"), fg=self.colors["text_sub"], bg=self.colors["bg_dark"]).pack(side="left", padx=(30, 5))
        search_var = tk.StringVar()
        search_entry = tk.Entry(ctrl_bar, textvariable=search_var, font=("Segoe UI", 10), bg=self.colors["entry_bg"], fg=self.colors["entry_fg"], insertbackground=self.colors["text_main"], relief="flat", width=22)
        search_entry.pack(side="left", ipady=4)

        # Action Buttons
        btn_frame = tk.Frame(ctrl_bar, bg=self.colors["bg_dark"])
        btn_frame.pack(side="right")

        # Treeview Container
        tree_card = tk.Frame(view, bg=self.colors["card_bg"], highlightbackground=self.colors["card_border"], highlightthickness=1)
        tree_card.pack(fill="both", expand=True)

        tree = ttk.Treeview(tree_card, show="headings", selectmode="browse")
        vsb = ttk.Scrollbar(tree_card, orient="vertical", command=tree.yview)
        hsb = ttk.Scrollbar(tree_card, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        view.current_df = pd.DataFrame()

        def load_data():
            df = self.get_table_df(table_name, default_cols)
            view.current_df = df
            populate_tree(df)

        def populate_tree(df_to_show):
            tree.delete(*tree.get_children())
            cols = list(df_to_show.columns)
            tree["columns"] = cols

            for col in cols:
                tree.heading(col, text=col, anchor="w")
                tree.column(col, width=130, minwidth=80, anchor="w")

            for _, row in df_to_show.iterrows():
                tree.insert("", "end", values=list(row))

        def filter_data(*args):
            query = search_var.get().lower().strip()
            if not query:
                populate_tree(view.current_df)
                return
            filtered_df = view.current_df[view.current_df.astype(str).apply(lambda x: x.str.lower().str.contains(query)).any(axis=1)]
            populate_tree(filtered_df)

        search_var.trace("w", filter_data)

        # Add Record Action
        def add_record():
            if view.current_df.empty:
                cols = default_cols
            else:
                cols = list(view.current_df.columns)

            dialog = tk.Toplevel(self)
            dialog.title(f"Add New Record - {table_name}")
            dialog.geometry("450x520")
            dialog.configure(bg=self.colors["card_bg"])
            dialog.transient(self)
            dialog.grab_set()

            tk.Label(dialog, text=f"Add {table_name.capitalize()} Record", font=("Segoe UI", 12, "bold"), fg=self.colors["accent"], bg=self.colors["card_bg"]).pack(pady=15)

            entries = {}
            form_frame = tk.Frame(dialog, bg=self.colors["card_bg"])
            form_frame.pack(fill="both", expand=True, padx=25)

            for col in cols:
                row_f = tk.Frame(form_frame, bg=self.colors["card_bg"])
                row_f.pack(fill="x", pady=4)
                tk.Label(row_f, text=col, font=("Segoe UI", 9, "bold"), fg=self.colors["text_sub"], bg=self.colors["card_bg"], width=15, anchor="w").pack(side="left")
                ent = tk.Entry(row_f, font=("Segoe UI", 10), bg=self.colors["entry_bg"], fg=self.colors["entry_fg"], insertbackground=self.colors["text_main"], relief="flat")
                ent.pack(side="right", fill="x", expand=True, ipady=3)
                entries[col] = ent

            def save_new():
                new_row = {}
                for c, ent in entries.items():
                    val = ent.get().strip()
                    try:
                        val = int(val)
                    except ValueError:
                        try:
                            val = float(val)
                        except ValueError:
                            pass
                    new_row[c] = val

                if self.is_connected and self.engine:
                    try:
                        new_df = pd.DataFrame([new_row])
                        new_df.to_sql(name=table_name, con=self.engine, index=False, if_exists='append')
                        messagebox.showinfo("Success", "Record added to database successfully!")
                    except Exception as ex:
                        messagebox.showerror("Database Error", f"Failed to save record: {ex}")
                else:
                    view.current_df.loc[len(view.current_df)] = new_row
                    messagebox.showinfo("Success (Local)", "Record added to local view!")

                dialog.destroy()
                load_data()

            tk.Button(dialog, text="SAVE RECORD", font=("Segoe UI", 10, "bold"), bg=self.colors["success"], fg="#11111b", relief="flat", cursor="hand2", command=save_new).pack(pady=20, ipady=6, padx=25, fill="x")

        # Edit Selected Record
        def edit_record():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Record", "Please select a row to edit.")
                return

            item_values = tree.item(selected[0], "values")
            cols = list(view.current_df.columns)

            dialog = tk.Toplevel(self)
            dialog.title(f"Edit Record - {table_name}")
            dialog.geometry("450x520")
            dialog.configure(bg=self.colors["card_bg"])
            dialog.transient(self)
            dialog.grab_set()

            tk.Label(dialog, text=f"Edit {table_name.capitalize()} Record", font=("Segoe UI", 12, "bold"), fg=self.colors["accent"], bg=self.colors["card_bg"]).pack(pady=15)

            entries = {}
            form_frame = tk.Frame(dialog, bg=self.colors["card_bg"])
            form_frame.pack(fill="both", expand=True, padx=25)

            for idx, col in enumerate(cols):
                row_f = tk.Frame(form_frame, bg=self.colors["card_bg"])
                row_f.pack(fill="x", pady=4)
                tk.Label(row_f, text=col, font=("Segoe UI", 9, "bold"), fg=self.colors["text_sub"], bg=self.colors["card_bg"], width=15, anchor="w").pack(side="left")
                ent = tk.Entry(row_f, font=("Segoe UI", 10), bg=self.colors["entry_bg"], fg=self.colors["entry_fg"], insertbackground=self.colors["text_main"], relief="flat")
                ent.pack(side="right", fill="x", expand=True, ipady=3)
                ent.insert(0, str(item_values[idx]) if idx < len(item_values) else "")
                entries[col] = ent

            def update_save():
                id_col = cols[0]
                rec_id = item_values[0]

                if self.is_connected and self.engine:
                    try:
                        with self.engine.connect() as conn:
                            for col_name, ent in entries.items():
                                val = ent.get().strip()
                                conn.execute(sa.text(f"UPDATE `{table_name}` SET `{col_name}`='{val}' WHERE `{id_col}`='{rec_id}'"))
                            conn.commit()
                        messagebox.showinfo("Success", "Record updated successfully!")
                    except Exception as ex:
                        messagebox.showerror("Database Error", f"Update failed: {ex}")
                else:
                    messagebox.showinfo("Updated", "Local record updated.")

                dialog.destroy()
                load_data()

            tk.Button(dialog, text="UPDATE RECORD", font=("Segoe UI", 10, "bold"), bg=self.colors["warning"], fg="#11111b", relief="flat", cursor="hand2", command=update_save).pack(pady=20, ipady=6, padx=25, fill="x")

        # Delete Selected Record
        def delete_record():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Select Record", "Please select a row to delete.")
                return

            item_values = tree.item(selected[0], "values")
            rec_id = item_values[0]
            id_col = view.current_df.columns[0]

            if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete record with {id_col} = {rec_id}?"):
                if self.is_connected and self.engine:
                    try:
                        with self.engine.connect() as conn:
                            conn.execute(sa.text(f"DELETE FROM `{table_name}` WHERE `{id_col}`='{rec_id}'"))
                            conn.commit()
                        messagebox.showinfo("Deleted", "Record deleted from database.")
                    except Exception as ex:
                        messagebox.showerror("Delete Error", f"Failed: {ex}")
                else:
                    messagebox.showinfo("Deleted", "Local record removed.")
                load_data()

        # Add Column
        def add_column():
            col_name = simpledialog.askstring("Add Data Category", "Enter new Column/Category Name:")
            if col_name:
                default_val = simpledialog.askstring("Default Value", f"Enter default value for {col_name}:", initialvalue="N/A")
                if self.is_connected and self.engine:
                    try:
                        with self.engine.connect() as conn:
                            conn.execute(sa.text(f"ALTER TABLE `{table_name}` ADD COLUMN `{col_name}` VARCHAR(255) DEFAULT '{default_val}'"))
                            conn.commit()
                        messagebox.showinfo("Column Added", f"Added column `{col_name}` successfully.")
                    except Exception as ex:
                        messagebox.showerror("Error", f"Failed to add column: {ex}")
                load_data()

        # Export CSV
        def export_csv():
            if not view.current_df.empty:
                filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
                if filepath:
                    view.current_df.to_csv(filepath, index=False)
                    messagebox.showinfo("Export Successful", f"Data exported to {filepath}")

        # Add Buttons to Control Bar
        tk.Button(btn_frame, text="➕ Add Record", font=("Segoe UI", 9, "bold"), bg=self.colors["accent"], fg="#11111b", relief="flat", cursor="hand2", command=add_record).pack(side="left", padx=3)
        tk.Button(btn_frame, text="✏️ Edit", font=("Segoe UI", 9, "bold"), bg=self.colors["warning"], fg="#11111b", relief="flat", cursor="hand2", command=edit_record).pack(side="left", padx=3)
        tk.Button(btn_frame, text="🗑️ Delete", font=("Segoe UI", 9, "bold"), bg=self.colors["danger"], fg="#11111b", relief="flat", cursor="hand2", command=delete_record).pack(side="left", padx=3)
        tk.Button(btn_frame, text="➕ Add Column", font=("Segoe UI", 9, "bold"), bg=self.colors["card_border"], fg=self.colors["text_main"], relief="flat", cursor="hand2", command=add_column).pack(side="left", padx=3)
        tk.Button(btn_frame, text="📥 Export CSV", font=("Segoe UI", 9, "bold"), bg=self.colors["success"], fg="#11111b", relief="flat", cursor="hand2", command=export_csv).pack(side="left", padx=3)
        tk.Button(btn_frame, text="🔄 Refresh", font=("Segoe UI", 9, "bold"), bg=self.colors["card_border"], fg=self.colors["text_main"], relief="flat", cursor="hand2", command=load_data).pack(side="left", padx=3)

        view.refresh_data = load_data
        return view

    # --- Analytics View Component ---
    def _create_analytics_view(self):
        view = tk.Frame(self.content_area, bg=self.colors["bg_dark"])

        header = tk.Frame(view, bg=self.colors["bg_dark"])
        header.pack(fill="x", pady=(0, 10))

        tk.Label(header, text="📈 Showroom Data Analytics & Reports", font=("Segoe UI", 16, "bold"), fg=self.colors["text_main"], bg=self.colors["bg_dark"]).pack(side="left")

        # Report Selector Dropdown
        tk.Label(header, text="Select Report:", font=("Segoe UI", 10, "bold"), fg=self.colors["text_sub"], bg=self.colors["bg_dark"]).pack(side="left", padx=(30, 5))
        report_var = tk.StringVar(value="Showroom General Overview")
        report_combo = ttk.Combobox(header, textvariable=report_var, state="readonly", width=35)
        report_combo["values"] = [
            "Showroom General Overview",
            "Company Wise Car Count & Prices",
            "Fuel Type Distribution & Prices",
            "Car Price Segment Breakdown",
            "Payment Status & Method Summary"
        ]
        report_combo.pack(side="left", ipady=3)

        # Dual Panel Container (Left: Chart, Right: Data Summary Text Box)
        main_card = tk.Frame(view, bg=self.colors["card_bg"], highlightbackground=self.colors["card_border"], highlightthickness=1)
        main_card.pack(fill="both", expand=True)

        chart_frame = tk.Frame(main_card, bg=self.colors["card_bg"], width=520)
        chart_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        info_frame = tk.Frame(main_card, bg=self.colors["sidebar"], width=400, highlightbackground=self.colors["card_border"], highlightthickness=1)
        info_frame.pack(side="right", fill="both", padx=10, pady=10)
        info_frame.pack_propagate(False)

        tk.Label(info_frame, text="📊 Detailed Summary Report", font=("Segoe UI", 12, "bold"), fg=self.colors["accent"], bg=self.colors["sidebar"]).pack(anchor="w", padx=15, pady=(12, 5))

        # Scrollable Text Area for Summary Stats
        info_text = tk.Text(info_frame, font=("Consolas", 10), bg=self.colors["card_bg"], fg=self.colors["text_main"], relief="flat", padx=10, pady=10, insertbackground=self.colors["text_main"])
        info_scroll = ttk.Scrollbar(info_frame, orient="vertical", command=info_text.yview)
        info_text.configure(yscrollcommand=info_scroll.set)

        info_scroll.pack(side="right", fill="y")
        info_text.pack(fill="both", expand=True, padx=5, pady=5)

        def find_col(df, names):
            if df.empty:
                return None
            for n in names:
                for col in df.columns:
                    if col.lower().strip() == n.lower().strip():
                        return col
            return None

        def render_report(*args):
            for w in chart_frame.winfo_children():
                w.destroy()

            info_text.config(state="normal")
            info_text.delete("1.0", tk.END)

            report_type = report_var.get()
            cars_df = self.get_table_df("cars")
            cust_df = self.get_table_df("customers")
            emp_df = self.get_table_df("employees")
            ord_df = self.get_table_df("orders")
            pay_df = self.get_table_df("payments")

            plt.close('all')
            fig = Figure(figsize=(5.5, 4.5), facecolor=self.colors["card_bg"])
            ax = fig.add_subplot(111)
            ax.set_facecolor(self.colors["card_bg"])
            for spine in ax.spines.values():
                spine.set_color(self.colors["card_border"])

            comp_col = find_col(cars_df, ["Company", "company"])
            fuel_col = find_col(cars_df, ["Fuel_Type", "fuel_type", "Fuel"])
            price_col = find_col(cars_df, ["Price($)", "price($)", "Price", "price"])
            name_col = find_col(cars_df, ["Car_Name", "car_name", "Car", "car"])
            status_col = find_col(pay_df, ["Payment_Status", "payment_status", "status"])
            method_col = find_col(pay_df, ["Payment_Method", "payment_method", "method"])
            amount_col = find_col(pay_df, ["Amount", "amount"])

            summary_output = []

            if report_type == "Showroom General Overview":
                summary_output.append("=== SHOWROOM GENERAL OVERVIEW ===")
                summary_output.append(f"• Total Cars in Fleet: {len(cars_df)}")
                summary_output.append(f"• Registered Customers: {len(cust_df)}")
                summary_output.append(f"• Total Active Employees: {len(emp_df)}")
                summary_output.append(f"• Total Orders Processed: {len(ord_df)}")
                summary_output.append(f"• Total Payment Records: {len(pay_df)}\n")

                if price_col and not cars_df.empty:
                    tot_val = cars_df[price_col].sum()
                    avg_val = cars_df[price_col].mean()
                    summary_output.append(f"• Total Stock Value: ${tot_val:,.2f}")
                    summary_output.append(f"• Average Car Price: ${avg_val:,.2f}")

                # Plot overview bar chart
                categories = ["Cars", "Customers", "Employees", "Orders", "Payments"]
                counts = [len(cars_df), len(cust_df), len(emp_df), len(ord_df), len(pay_df)]
                ax.bar(categories, counts, color=[self.colors["accent"], self.colors["success"], self.colors["warning"], "#f5c2e7", "#cba6f7"])
                ax.set_title("Showroom Entity Totals", color=self.colors["text_main"], fontsize=11, fontweight="bold")
                ax.tick_params(colors=self.colors["text_sub"], labelsize=8)

            elif report_type == "Company Wise Car Count & Prices" and comp_col and not cars_df.empty:
                counts = cars_df[comp_col].value_counts()
                ax.bar(counts.index, counts.values, color=self.colors["accent"])
                ax.set_title("Company Wise Stock Count", color=self.colors["text_main"], fontsize=11, fontweight="bold")
                ax.tick_params(colors=self.colors["text_sub"], labelsize=8, rotation=15)

                summary_output.append("=== COMPANY WISE CAR BREAKDOWN ===")
                for comp, count in counts.items():
                    comp_sub = cars_df[cars_df[comp_col] == comp]
                    avg_p = comp_sub[price_col].mean() if price_col else 0
                    summary_output.append(f"• {comp}: {count} car(s) | Avg: ${avg_p:,.0f}")

                if price_col and name_col:
                    exp_idx = cars_df[price_col].idxmax()
                    che_idx = cars_df[price_col].idxmin()
                    summary_output.append(f"\n🌟 Most Expensive: {cars_df.loc[exp_idx, name_col]} (${cars_df.loc[exp_idx, price_col]:,.0f})")
                    summary_output.append(f"💡 Most Affordable: {cars_df.loc[che_idx, name_col]} (${cars_df.loc[che_idx, price_col]:,.0f})")

            elif report_type == "Fuel Type Distribution & Prices" and fuel_col and not cars_df.empty:
                fuel_counts = cars_df[fuel_col].value_counts()
                pie_res = ax.pie(fuel_counts.values, labels=fuel_counts.index, colors=[self.colors["accent"], self.colors["success"], self.colors["warning"], "#cba6f7"], autopct='%1.1f%%', textprops={'color': self.colors["text_main"], 'fontsize': 9, 'weight': 'bold'})
                if len(pie_res) == 3:
                    for at in pie_res[2]:
                        at.set_color("#11111b")
                        at.set_fontsize(10)
                        at.set_weight("bold")
                ax.set_title("Fuel Type Category Share", color=self.colors["text_main"], fontsize=11, fontweight="bold")

                summary_output.append("=== FUEL TYPE DISTRIBUTION ===")
                for fuel, count in fuel_counts.items():
                    f_sub = cars_df[cars_df[fuel_col] == fuel]
                    avg_p = f_sub[price_col].mean() if price_col else 0
                    summary_output.append(f"• {fuel}: {count} model(s) (Avg: ${avg_p:,.0f})")

            elif report_type == "Car Price Segment Breakdown" and price_col and not cars_df.empty:
                budget = cars_df[cars_df[price_col] < 30000]
                mid = cars_df[(cars_df[price_col] >= 30000) & (cars_df[price_col] <= 60000)]
                luxury = cars_df[cars_df[price_col] > 60000]

                categories = ["Budget (<$30k)", "Mid ($30k-$60k)", "Luxury (>$60k)"]
                values = [len(budget), len(mid), len(luxury)]
                ax.bar(categories, values, color=[self.colors["success"], self.colors["warning"], self.colors["danger"]])
                ax.set_title("Price Segment Breakdown", color=self.colors["text_main"], fontsize=11, fontweight="bold")
                ax.tick_params(colors=self.colors["text_sub"], labelsize=8)

                summary_output.append("=== PRICE SEGMENT ANALYSIS ===")
                summary_output.append(f"🟢 Budget (<$30k): {len(budget)} model(s)")
                summary_output.append(f"🟡 Mid-Range ($30k-$60k): {len(mid)} model(s)")
                summary_output.append(f"🔴 Luxury (>$60k): {len(luxury)} model(s)")

                summary_output.append("\n• Overall Fleet Avg Price: $" + (f"{cars_df[price_col].mean():,.2f}" if price_col else "0"))

            elif report_type == "Payment Status & Method Summary" and not pay_df.empty:
                summary_output.append("=== PAYMENTS & REVENUE SUMMARY ===")
                if status_col:
                    s_counts = pay_df[status_col].value_counts()
                    ax.bar(s_counts.index, s_counts.values, color=[self.colors["success"], self.colors["warning"], self.colors["danger"]])
                    ax.set_title("Payment Status Counts", color=self.colors["text_main"], fontsize=11, fontweight="bold")
                    ax.tick_params(colors=self.colors["text_sub"], labelsize=8)

                    for st, cnt in s_counts.items():
                        sub_pay = pay_df[pay_df[status_col] == st]
                        tot_amt = sub_pay[amount_col].sum() if amount_col else 0
                        summary_output.append(f"• Status [{st}]: {cnt} transaction(s) | Total: ${tot_amt:,.2f}")

                if method_col:
                    m_counts = pay_df[method_col].value_counts()
                    summary_output.append("\n=== PAYMENT METHODS USED ===")
                    for mth, cnt in m_counts.items():
                        summary_output.append(f"• {mth}: {cnt} payment(s)")
            else:
                ax.text(0.5, 0.5, "No Data Available", ha="center", va="center", color=self.colors["text_sub"], fontsize=12)
                ax.set_xticks([])
                ax.set_yticks([])
                summary_output.append("No record entries available for this report.")

            fig.tight_layout()
            canvas = FigureCanvasTkAgg(fig, master=chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            info_text.insert(tk.END, "\n".join(summary_output))
            info_text.config(state="disabled")

        report_combo.bind("<<ComboboxSelected>>", render_report)
        view.refresh_data = render_report
        return view

if __name__ == "__main__":
    app = CarShowroomGUI()
    app.mainloop()
