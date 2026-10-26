import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

# --- BACKEND FUNCTIONS (Your existing logic) ---
def create_files():
    if not os.path.exists("patients.csv"):
        with open("patients.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Patient ID", "Name", "Age", "Gender", "Contact"])
            writer.writerows([
                ["P001", "Aarav Sharma", 45, "Male", "9876543210"],
                ["P002", "Priya Patel", 32, "Female", "9123456789"],
                ["P003", "Rajesh Kumar", 58, "Male", "9988776655"],
                ["P004", "Ananya Roy", 27, "Female", "9765432109"],
                ["P005", "Vikram Singh", 63, "Male", "9112233445"]
            ])
    if not os.path.exists("appointments.csv"):
        with open("appointments.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Appointment ID", "Patient ID", "Doctor", "Date", "Status"])
            writer.writerows([
                ["A001", "P001", "Dr. Mehta", "2026-06-01", "Completed"],
                ["A002", "P002", "Dr. Sen", "2026-06-02", "Completed"],
                ["A003", "P003", "Dr. Rao", "2026-06-03", "Scheduled"]
            ])
    if not os.path.exists("health_records.csv"):
        with open("health_records.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Record ID", "Patient ID", "Date", "Temperature C", "Systolic BP", "Diastolic BP", "Pulse", "Diagnosis Note", "Charges"])
            writer.writerows([
                ["R001", "P001", "2026-06-01", 37.2, 120, 80, 72, "Normal checkup", 500.0],
                ["R002", "P002", "2026-06-02", 36.8, 110, 75, 68, "Mild fatigue", 450.0],
                ["R003", "P004", "2026-06-04", 38.1, 130, 85, 82, "Viral fever", 800.0]
            ])

def read_rows(filename):
    with open(filename, "r", newline="") as file:
        return list(csv.DictReader(file))

# --- GUI DASHBOARD APPLICATION ---
class HospitalDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Hospital Management Dashboard")
        self.root.geometry("700x500")
        self.root.config(bg="#f4f6f9")

        create_files()

        # Title Header
        header = tk.Label(root, text="🏥 Smart Hospital Dashboard", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white", pady=15)
        header.pack(fill=tk.X)

        # Main Frame for Buttons
        btn_frame = tk.Frame(root, bg="#f4f6f9")
        btn_frame.pack(pady=40)

        # Dashboard Action Buttons
        btn_style = {"font": ("Arial", 11, "bold"), "width": 25, "pady": 8, "bd": 0, "cursor": "hand2"}
        
        tk.Button(btn_frame, text="📋 View Registered Patients", bg="#3498db", fg="white", command=self.show_patients_window, **btn_style).grid(row=0, column=0, padx=15, pady=10)
        tk.Button(btn_frame, text="📅 View Appointments", bg="#2ecc71", fg="white", command=self.show_appointments_window, **btn_style).grid(row=0, column=1, padx=15, pady=10)
        tk.Button(btn_frame, text="🩺 View Health Records", bg="#e67e22", fg="white", command=self.show_records_window, **btn_style).grid(row=1, column=0, padx=15, pady=10)
        tk.Button(btn_frame, text="📊 Run Analytics & Show Graphs", bg="#9b59b6", fg="white", command=self.run_analytics, **btn_style).grid(row=1, column=1, padx=15, pady=10)

        # Exit Button
        tk.Button(root, text="❌ Exit Application", bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=20, command=root.quit).pack(pady=20)

    def show_patients_window(self):
        patients = read_rows("patients.csv")
        self.open_table_view("Registered Patients", ["Patient ID", "Name", "Age", "Gender", "Contact"], 
                             [[p["Patient ID"], p["Name"], p["Age"], p["Gender"], p["Contact"]] for p in patients])

    def show_appointments_window(self):
        appointments = read_rows("appointments.csv")
        self.open_table_view("Appointment Schedule", ["Appointment ID", "Patient ID", "Doctor", "Date", "Status"], 
                             [[a["Appointment ID"], a["Patient ID"], a["Doctor"], a["Date"], a["Status"]] for a in appointments])

    def show_records_window(self):
        records = read_rows("health_records.csv")
        self.open_table_view("Health Records", ["Record ID", "Patient ID", "Date", "Temp (°C)", "BP", "Charges (Rs.)"], 
                             [[r["Record ID"], r["Patient ID"], r["Date"], r["Temperature C"], f"{r['Systolic BP']}/{r['Diastolic BP']}", r["Charges"]] for r in records])

    def open_table_view(self, title, headers, data):
        """Creates a popup window with a structured Data Table grid."""
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("650x350")

        tk.Label(win, text=title, font=("Arial", 14, "bold"), pady=10).pack()

        # Treeview Widget for Tables
        tree = ttk.Treeview(win, columns=headers, show="headings", height=10)
        for col in headers:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        for row in data:
            tree.insert("", tk.END, values=row)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_analytics(self):
        patients = read_rows("patients.csv")
        records = read_rows("health_records.csv")
        
        if not patients:
            messagebox.showerror("Error", "No patient data found!")
            return

        ages = np.array([int(p["Age"]) for p in patients])
        
        # Create a small selection window for individual graphs
        graph_win = tk.Toplevel(self.root)
        graph_win.title("Select Graph to View")
        graph_win.geometry("350x300")
        graph_win.config(bg="#f4f6f9")

        tk.Label(graph_win, text="Choose a Visual Chart", font=("Arial", 12, "bold"), bg="#f4f6f9", pady=10).pack()

        def show_bar_chart():
            plt.figure(figsize=(7, 4))
            plt.bar([p["Name"] for p in patients], ages, color='skyblue')
            plt.xlabel("Patients")
            plt.ylabel("Age")
            plt.title("Age of Registered Patients")
            plt.xticks(rotation=25)
            plt.tight_layout()
            plt.show()

        def show_line_graph():
            if not records:
                messagebox.showerror("Error", "No health records available for temperature trend!")
                return
            records_sorted = sorted(records, key=lambda r: r["Date"])
            dates = [r["Date"] for r in records_sorted]
            temperatures = [float(r["Temperature C"]) for r in records_sorted]

            plt.figure(figsize=(7, 4))
            plt.plot(dates, temperatures, marker="o", color='crimson', linewidth=2)
            plt.xlabel("Visit Date")
            plt.ylabel("Recorded Temperature (°C)")
            plt.title("Recorded Temperature Across Visits")
            plt.xticks(rotation=25)
            plt.grid(True)
            plt.tight_layout()
            plt.show()

        def show_pie_chart():
            if not records:
                messagebox.showerror("Error", "No health records available for charges breakdown!")
                return
            
            # Filter and get only patients who have charges > 0
            chart_labels = []
            chart_charges = []
            
            for p in patients:
                # Sum up charges for this patient
                p_charges = sum(float(r["Charges"]) for r in records if r["Patient ID"] == p["Patient ID"])
                if p_charges > 0:  # Only include if they have a non-zero charge
                    chart_labels.append(p["Name"])
                    chart_charges.append(p_charges)

            if chart_charges:
                plt.figure(figsize=(6, 6))
                plt.pie(chart_charges, labels=chart_labels, autopct="%1.1f%%", startangle=140)
                plt.title("Share of Recorded Visit Charges")
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("Info", "No valid charges recorded to display.")

        def show_box_plot():
            plt.figure(figsize=(6, 4))
            plt.boxplot(ages, tick_labels=["Patient Ages"])
            plt.ylabel("Age")
            plt.title("Distribution of Registered Patient Ages")
            plt.tight_layout()
            plt.show()

        # Buttons inside the graph selection window
        btn_st = {"font": ("Arial", 10), "width": 25, "pady": 5, "cursor": "hand2"}
        tk.Button(graph_win, text="1. Patient Age Bar Chart", bg="#3498db", fg="white", command=show_bar_chart, **btn_st).pack(pady=5)
        tk.Button(graph_win, text="2. Temperature Trend Line Graph", bg="#e67e22", fg="white", command=show_line_graph, **btn_st).pack(pady=5)
        tk.Button(graph_win, text="3. Visit Charges Pie Chart", bg="#2ecc71", fg="white", command=show_pie_chart, **btn_st).pack(pady=5)
        tk.Button(graph_win, text="4. Age Distribution Box Plot", bg="#9b59b6", fg="white", command=show_box_plot, **btn_st).pack(pady=5)

if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalDashboard(root)
    root.mainloop()