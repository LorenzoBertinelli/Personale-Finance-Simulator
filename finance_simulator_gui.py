import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import csv
import os
from simulation_engine import FinancialSimulator

class FinancialSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("📊 Simulatore Finanziario Personale")
        self.root.geometry("800x650")
        self.root.configure(bg='#f0f2f5')
        if os.path.exists("finance.ico"):
            self.root.iconbitmap("finance.ico")

        style = ttk.Style()
        style.configure("TLabel", background="#f0f2f5", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 11, "bold"))
        style.configure("TCombobox", font=("Segoe UI", 10))

        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill='both', expand=True)
        for i in range(15):
            frame.rowconfigure(i, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        labels = [
            "Età:", "Capitale Liquido Attuale:", "Spese Mensili:",
            "Investimenti Mensili:", "Rendimenti Stimati (% annuo):",
            "Inflazione Stimata (%):", "Condizioni Abitative:",
            "Deviazione Standard dei Rendimenti (%):",
            "Percentuale Spese Variabili (%):",
            "Probabilità di Eventi Imprevisti (%):",
            "Crescita Stipendio/Entrate Annuale Prevista (%):",
            "Data Stimata di Pensionamento:",
            "Tassazione Sugli Investimenti (%):", "Tipologia Investimento:"
        ]

        self.entries = {}
        for idx, label in enumerate(labels):
            if label in ["Condizioni Abitative:", "Tipologia Investimento:"]:
                continue
            ttk.Label(frame, text=label).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
            entry = ttk.Entry(frame)
            entry.grid(row=idx, column=1, sticky="ew", padx=5, pady=5)
            self.entries[label[:-1]] = entry

        idx_housing = labels.index("Condizioni Abitative:")
        ttk.Label(frame, text="Condizioni Abitative:").grid(row=idx_housing, column=0, sticky="w", padx=5, pady=5)
        self.housing_combo = ttk.Combobox(frame, values=["affitto", "mutuo", "mantenuto"], state="readonly")
        self.housing_combo.current(0)
        self.housing_combo.grid(row=idx_housing, column=1, sticky="ew", padx=5, pady=5)

        idx_invest = labels.index("Tipologia Investimento:")
        ttk.Label(frame, text="Tipologia Investimento:").grid(row=idx_invest, column=0, sticky="w", padx=5, pady=5)
        self.investment_combo = ttk.Combobox(frame, values=["basso", "medio", "alto"], state="readonly")
        self.investment_combo.current(1)
        self.investment_combo.grid(row=idx_invest, column=1, sticky="ew", padx=5, pady=5)

        simulate_button = ttk.Button(self.root, text="▶ Simula", command=self.run_simulation)
        simulate_button.pack(pady=15)

    def run_simulation(self):
        try:
            def parse_float(val):
                return float(val.replace(",", "."))

            for key, entry in self.entries.items():
                if not entry.get().strip():
                    raise ValueError("Inserire tutti i dati!")

            age = int(self.entries["Età"].get())
            initial_capital = parse_float(self.entries["Capitale Liquido Attuale"].get())
            monthly_expenses = parse_float(self.entries["Spese Mensili"].get())
            monthly_investments = parse_float(self.entries["Investimenti Mensili"].get())
            estimated_returns = parse_float(self.entries["Rendimenti Stimati (% annuo)"].get()) / 100
            inflation_rate = parse_float(self.entries["Inflazione Stimata (%)"].get()) / 100
            std_dev = parse_float(self.entries["Deviazione Standard dei Rendimenti (%)"].get()) / 100
            variable_expense_pct = parse_float(self.entries["Percentuale Spese Variabili (%)"].get()) / 100
            unexpected_events_prob = parse_float(self.entries["Probabilità di Eventi Imprevisti (%)"].get()) / 100
            salary_growth_rate = parse_float(self.entries["Crescita Stipendio/Entrate Annuale Prevista (%)"].get()) / 100
            retirement_age = int(self.entries["Data Stimata di Pensionamento"].get())
            tax_rate = parse_float(self.entries["Tassazione Sugli Investimenti (%)"].get()) / 100
            housing_condition = self.housing_combo.get()
            investment_level = self.investment_combo.get()

            investment_type = {
                "basso": {"mean": 0.04, "std_dev": 0.05},
                "medio": {"mean": 0.06, "std_dev": 0.10},
                "alto": {"mean": 0.08, "std_dev": 0.15},
            }[investment_level]

            simulator = FinancialSimulator(
                age, initial_capital, monthly_expenses, monthly_investments,
                estimated_returns, inflation_rate, unexpected_events_prob,
                salary_growth_rate * 100, retirement_age,
                tax_rate * 100, investment_type,
                housing_condition, variable_expense_pct, std_dev
            )

            simulations = simulator.simulate()
            self.plot_results(simulations)
            self.export_to_csv(simulations)

        except ValueError as ve:
            messagebox.showwarning("Dati Mancanti", str(ve))
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la simulazione:\n{str(e)}")

    def plot_results(self, simulations):
        for idx, sim in enumerate(simulations):
            plt.figure(figsize=(8, 4))
            plt.plot(sim, color='blue', linewidth=1.5)
            plt.title(f"Caso {idx+1}")
            plt.xlabel("Mesi")
            plt.ylabel("Capitale (€)")
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(f"simulazione_{idx+1}.png")
            plt.close()
        messagebox.showinfo("Simulazione completata", "Grafici salvati nella cartella del progetto.")

    def export_to_csv(self, simulations):
        output_path = os.path.join(os.getcwd(), "simulazioni_output.csv")
        with open(output_path, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for i, sim in enumerate(simulations):
                writer.writerow([f"Caso {i+1}:"])
                writer.writerow(["Mese", "Capitale (€)"])
                for month, val in enumerate(sim):
                    writer.writerow([month, round(val, 2)])
                writer.writerow([])
        messagebox.showinfo("Esportazione Completata", f"Dati salvati in:\n{output_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialSimulatorGUI(root)
    root.mainloop()