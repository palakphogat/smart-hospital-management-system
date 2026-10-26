import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

class Patient:
    def __init__(self, patient_id, name, age, gender, contact):
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.contact = contact

    def get_details(self):
        return [
            self.patient_id,
            self.name,
            self.age,
            self.gender,
            self.contact
        ]

class Appointment:
    def __init__(self, appointment_id, patient_id, doctor, date, status):
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor = doctor
        self.date = date
        self.status = status

    def get_details(self):
        return [
            self.appointment_id,
            self.patient_id,
            self.doctor,
            self.date,
            self.status
        ]

class HealthRecord:
    def __init__(self, record_id, patient_id, date,
                 temperature, systolic_bp, diastolic_bp,
                 pulse, diagnosis_note, charges):
        self.record_id = record_id
        self.patient_id = patient_id
        self.date = date
        self.temperature = temperature
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.pulse = pulse
        self.diagnosis_note = diagnosis_note
        self.charges = charges

    def get_details(self):
        return [
            self.record_id,
            self.patient_id,
            self.date,
            self.temperature,
            self.systolic_bp,
            self.diastolic_bp,
            self.pulse,
            self.diagnosis_note,
            self.charges
        ]

def create_files():
    # 1. Patients file and initial sample data
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

    # 2. Appointments file and initial sample data
    if not os.path.exists("appointments.csv"):
        with open("appointments.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Appointment ID", "Patient ID", "Doctor", "Date", "Status"])
            writer.writerows([
                ["A001", "P001", "Dr. Mehta", "2026-06-01", "Completed"],
                ["A002", "P002", "Dr. Sen", "2026-06-02", "Completed"],
                ["A003", "P003", "Dr. Rao", "2026-06-03", "Scheduled"],
                ["A004", "P004", "Dr. Mehta", "2026-06-04", "Completed"],
                ["A005", "P005", "Dr. Sen", "2026-06-05", "Scheduled"]
            ])

    # 3. Health records file and initial sample data
    if not os.path.exists("health_records.csv"):
        with open("health_records.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Record ID", "Patient ID", "Date", "Temperature C", "Systolic BP", "Diastolic BP", "Pulse", "Diagnosis Note", "Charges"])
            writer.writerows([
                ["R001", "P001", "2026-06-01", 37.2, 120, 80, 72, "Normal checkup", 500.0],
                ["R002", "P002", "2026-06-02", 36.8, 110, 75, 68, "Mild fatigue", 450.0],
                ["R003", "P004", "2026-06-04", 38.1, 130, 85, 82, "Viral fever", 800.0],
                ["R004", "P003", "2026-06-01", 37.0, 140, 90, 76, "Hypertension follow-up", 600.0]
            ])


def read_rows(filename):
    with open(filename, "r", newline="") as file:
        return list(csv.DictReader(file))

def register_patient():
    patient_id = input("Enter Patient ID: ").strip()
    name = input("Enter Patient Name: ").strip()

    if not patient_id or not name:
        print("Patient ID and name are required.")
        return

    patients = read_rows("patients.csv")

    if any(p["Patient ID"] == patient_id for p in patients):
        print("Patient ID already exists.")
        return

    try:
        age = int(input("Enter Age: "))
        if age < 0 or age > 120:
            print("Enter a valid age.")
            return
    except ValueError:
        print("Age must be a whole number.")
        return

    gender = input("Enter Gender: ").strip()
    contact = input("Enter Contact Number: ").strip()

    if not gender or not contact:
        print("Gender and contact are required.")
        return

    patient = Patient(patient_id, name, age, gender, contact)

    with open("patients.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(patient.get_details())

    print("Patient registered successfully.")

def show_patients():
    patients = read_rows("patients.csv")

    if not patients:
        print("No patients registered.")
        return

    print("\n--- Registered Patients ---")

    for p in patients:
        print(
            "ID:", p["Patient ID"],
            "| Name:", p["Name"],
            "| Age:", p["Age"],
            "| Gender:", p["Gender"],
            "| Contact:", p["Contact"]
        )

def add_appointment():
    appointment_id = input("Enter Appointment ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()

    appointments = read_rows("appointments.csv")
    patients = read_rows("patients.csv")

    if not appointment_id:
        print("Appointment ID is required.")
        return

    if any(a["Appointment ID"] == appointment_id for a in appointments):
        print("Appointment ID already exists.")
        return

    if not any(p["Patient ID"] == patient_id for p in patients):
        print("Patient not found. Register the patient first.")
        return

    doctor = input("Enter Doctor Name: ").strip()
    date_text = input("Enter Date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        print("Enter a valid date in YYYY-MM-DD format.")
        return

    if not doctor:
        print("Doctor name is required.")
        return

    status = input(
        "Enter Status (Scheduled/Completed/Cancelled): "
    ).strip().title()

    if status not in ["Scheduled", "Completed", "Cancelled"]:
        print("Invalid appointment status.")
        return

    appointment = Appointment(
        appointment_id, patient_id, doctor, date_text, status
    )

    with open("appointments.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(appointment.get_details())

    print("Appointment added successfully.")

def show_appointments():
    appointments = read_rows("appointments.csv")
    patients = read_rows("patients.csv")

    names = {
        p["Patient ID"]: p["Name"] for p in patients
    }

    if not appointments:
        print("No appointments available.")
        return

    print("\n--- Appointment List ---")

    for a in appointments:
        print(
            "Appointment ID:", a["Appointment ID"],
            "| Patient:", names.get(a["Patient ID"], "Unknown"),
            "| Doctor:", a["Doctor"],
            "| Date:", a["Date"],
            "| Status:", a["Status"]
        )

def add_health_record():
    record_id = input("Enter Record ID: ").strip()
    patient_id = input("Enter Patient ID: ").strip()

    patients = read_rows("patients.csv")
    records = read_rows("health_records.csv")

    if not record_id:
        print("Record ID is required.")
        return

    if any(r["Record ID"] == record_id for r in records):
        print("Record ID already exists.")
        return

    if not any(p["Patient ID"] == patient_id for p in patients):
        print("Patient not found. Register the patient first.")
        return

    date_text = input("Enter Visit Date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(date_text, "%Y-%m-%d")

        temperature = float(input("Enter Temperature (C): "))
        systolic = int(input("Enter Systolic BP: "))
        diastolic = int(input("Enter Diastolic BP: "))
        pulse = int(input("Enter Pulse Rate: "))
        charges = float(input("Enter Visit Charges (Rs.): "))

        if (
            temperature <= 0 or systolic <= 0
            or diastolic <= 0 or pulse <= 0 or charges < 0
        ):
            print("Please enter valid positive measurements and charges.")
            return

    except ValueError:
        print("Enter valid dates and numeric values.")
        return

    note = input("Enter Clinical Note: ").strip()

    record = HealthRecord(
        record_id, patient_id, date_text, temperature,
        systolic, diastolic, pulse, note, charges
    )

    with open("health_records.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(record.get_details())

    print("Health record saved successfully.")
    print("Visit Charges: Rs.", round(charges, 2))

def show_health_records():
    records = read_rows("health_records.csv")
    patients = read_rows("patients.csv")

    names = {
        p["Patient ID"]: p["Name"] for p in patients
    }

    if not records:
        print("No health records available.")
        return

    print("\n--- Health Records ---")

    for r in records:
        print(
            "Record ID:", r["Record ID"],
            "| Patient:", names.get(r["Patient ID"], "Unknown"),
            "| Date:", r["Date"],
            "| Temperature:", r["Temperature C"], "C",
            "| BP:", r["Systolic BP"], "/", r["Diastolic BP"],
            "| Pulse:", r["Pulse"],
            "| Charges: Rs.", r["Charges"]
        )

def analyse_hospital():
    patients = read_rows("patients.csv")
    records = read_rows("health_records.csv")
    appointments = read_rows("appointments.csv")

    if not patients:
        print("Register patients before analysing data.")
        return

    ages = np.array([int(p["Age"]) for p in patients])

    print("\n--- Hospital Data Analysis ---")
    print("Total Registered Patients:", len(patients))
    print("Total Health Records:", len(records))
    print("Total Appointments:", len(appointments))
    print("Average Patient Age:", round(np.mean(ages), 2))
    print("Youngest Patient Age:", np.min(ages))
    print("Oldest Patient Age:", np.max(ages))

    patient_ids = [p["Patient ID"] for p in patients]
    visit_counts = np.array([
        sum(1 for r in records if r["Patient ID"] == pid)
        for pid in patient_ids
    ])

    print("Total Recorded Visits:", np.sum(visit_counts))

    if records:
        temperatures = np.array([
            float(r["Temperature C"]) for r in records
        ])
        charges = np.array([
            float(r["Charges"]) for r in records
        ])

        print(
            "Average Recorded Temperature:",
            round(np.mean(temperatures), 2), "C"
        )
        print(
            "Total Recorded Charges: Rs.",
            round(np.sum(charges), 2)
        )

    create_graphs(patients, records)

def create_graphs(patients, records):
    # 1. Bar Chart: Patients by Age
    ages = [int(p["Age"]) for p in patients]

    plt.figure(figsize=(9, 5))
    plt.bar([p["Name"] for p in patients], ages)
    plt.xlabel("Patients")
    plt.ylabel("Age")
    plt.title("Age of Registered Patients")
    plt.xticks(rotation=30)
    plt.tight_layout()

    # 2. Line Graph: Recorded Temperature by Date
    if records:
        records_sorted = sorted(records, key=lambda r: r["Date"])
        dates = [r["Date"] for r in records_sorted]
        temperatures = [
            float(r["Temperature C"]) for r in records_sorted
        ]

        plt.figure(figsize=(9, 5))
        plt.plot(dates, temperatures, marker="o")
        plt.xlabel("Visit Date")
        plt.ylabel("Recorded Temperature (C)")
        plt.title("Recorded Temperature Across Visits")
        plt.xticks(rotation=30)
        plt.grid(True)
        plt.tight_layout()

        # 3. Pie Chart: Distribution of Visit Charges by Patient
        patient_names = [p["Name"] for p in patients]
        charges = [
            sum(
                float(r["Charges"])
                for r in records
                if r["Patient ID"] == p["Patient ID"]
            )
            for p in patients
        ]

        if sum(charges) > 0:
            plt.figure(figsize=(7, 7))
            plt.pie(
                charges,
                labels=patient_names,
                autopct="%1.1f%%"
            )
            plt.title("Share of Recorded Visit Charges")
            plt.tight_layout()

        # 4. Box Plot: Distribution of Patient Ages
        plt.figure(figsize=(7, 5))
        plt.boxplot(ages, tick_labels=["Patient Ages"])
        plt.ylabel("Age")
        plt.title("Distribution of Registered Patient Ages")
        plt.tight_layout()

    else:
        print("Add health records to generate visit-based graphs.")

    plt.show()

def main():
    create_files()

    while True:
        print("\n====================================")
        print(" SMART HOSPITAL MANAGEMENT SYSTEM")
        print("====================================")
        print("1. Register Patient")
        print("2. View Patients")
        print("3. Add Appointment")
        print("4. View Appointments")
        print("5. Add Health Record")
        print("6. View Health Records")
        print("7. Analyse Hospital Data and Show Graphs")
        print("8. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            register_patient()
        elif choice == "2":
            show_patients()
        elif choice == "3":
            add_appointment()
        elif choice == "4":
            show_appointments()
        elif choice == "5":
            add_health_record()
        elif choice == "6":
            show_health_records()
        elif choice == "7":
            analyse_hospital()
        elif choice == "8":
            print("Thank you for using the Smart Hospital System.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()