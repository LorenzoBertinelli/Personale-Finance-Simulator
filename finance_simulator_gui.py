import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from simulation_engine import FinancialSimulator  # Import aggiornato con il nuovo nome

class FinancialSimulatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulatore di Previsioni Finanziarie Personali")

        labels = [
            "Età (in anni):",
            "Capitale Liquido Attuale (es. 1.000,00 €):",
            "Spese Mensili (es. 2.300,50 €):",
            "Investimenti Mensili (es. 500,00 €):",
            "Rendimenti Stimati (% annuo, es. 5,00):",
            "Inflazione Stimata (% annuo, es. 2,00):",
            "Condizioni Abitative:",
            "Deviazione Standard dei Rendimenti (% annuo, es. 10,00):",
            "Percentuale Spese Variabili (% annuo, es. 20,00):",
            "Probabilità di Eventi Imprevisti (% annuo, es. 5,00):",
            "Crescita Stipendio/Entrate Annuale Prevista (% annuo, es. 3,00):",
            "Data Stimata di Pensionamento (in anni, es. 65):",
            "Tassazione Sugli Investimenti (% annuo, es. 15,00):",
            "Tipologia Investimento:"
        ]

        self.entries = {}
        for idx, label in enumerate(labels):
            tk.Label(root, text=label).grid(row=idx, column=0, sticky=tk.W, padx=5, pady=2)
            self.entries[label.split(":")[0]] = tk.Entry(root)
            self.entries[label.split(":")[0]].grid(row=idx, column=1, padx=5)

        idx_housing = labels.index("Condizioni Abitative:")
        tk.Label(root, text="Condizioni Abitative:").grid(row=idx_housing, column=0, sticky=tk.W, padx=5, pady=2)
        self.housing_combo = ttk.Combobox(root, values=["affitto", "mutuo", "mantenuto"], state="readonly")
        self.housing_combo.current(0)
        self.housing_combo.grid(row=idx_housing, column=1, padx=5)

        idx_invest = labels.index("Tipologia Investimento:")
        tk.Label(root, text="Tipologia Investimento:").grid(row=idx_invest, column=0, sticky=tk.W, padx=5, pady=2)
        self.investment_combo = ttk.Combobox(root, values=["basso", "medio", "alto"], state="readonly")
        self.investment_combo.current(1)
        self.investment_combo.grid(row=idx_invest, column=1, padx=5)

        tk.Button(root, text="Simula", command=self.run_simulation).grid(row=len(labels), column=0, columnspan=2,
                                                                         pady=10)

    def format_currency(self, value):
        """Formatta un numero come valuta in euro."""
        return f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".") + " €"

    def run_simulation(self):
        try:
            def parse_float(val):
                val = val.strip().replace(".", "").replace(",", ".")
                if val.endswith("."):
                    val = val[:-1]
                if val == "":
                    return 0.0
                return float(val)

            age_input = self.entries["Età"].get()
            if age_input.strip() == "":
                raise ValueError("L'età non può essere vuota.")
            if not age_input.isdigit() or int(age_input) <= 0:
                raise ValueError("L'età deve essere un numero positivo.")
            age = int(age_input)

            initial_capital = parse_float(self.entries["Capitale Liquido Attuale"].get())
            monthly_expenses = parse_float(self.entries["Spese Mensili"].get())
            monthly_investments = parse_float(self.entries["Investimenti Mensili"].get())
            estimated_returns = parse_float(self.entries["Rendimenti Stimati (%)"].get())
            inflation_rate = parse_float(self.entries["Inflazione Stimata (%)"].get())
            std_dev = parse_float(self.entries["Deviazione Standard dei Rendimenti (%)"].get()) / 100
            variable_expense_pct = parse_float(self.entries["Percentuale Spese Variabili (%)"].get()) / 100
            unexpected_events_prob = parse_float(self.entries["Probabilità di Eventi Imprevisti (%)"].get()) / 100
            salary_growth_rate = parse_float(
                self.entries["Crescita Stipendio/Entrate Annuale Prevista (%)"].get()) / 100

            retirement_age_input = self.entries["Data Stimata di Pensionamento"].get()
            if retirement_age_input.strip() == "":
                raise ValueError("La data stimata di pensionamento non può essere vuota.")
            if not retirement_age_input.isdigit() or int(retirement_age_input) <= 0:
                raise ValueError("La data stimata di pensionamento deve essere un numero positivo.")
            retirement_age = int(retirement_age_input)

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
                salary_growth_rate * 100,
                retirement_age, tax_rate * 100,
                investment_type, housing_condition,
                variable_expense_pct, std_dev
            )

            simulations = simulator.simulate()
            self.plot_results(simulations)

        except ValueError as ve:
            messagebox.showerror("Errore di Input", str(ve))
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante la simulazione:\n{str(e)}")

    def plot_results(self, simulations):
        plt.figure(figsize=(10, 6))
        for sim in simulations:
            plt.plot(sim, alpha=0.5)
        plt.title("Simulazioni del Patrimonio nel Tempo")
        plt.xlabel("Mesi")
        plt.ylabel("Capitale (€)")
        plt.grid(True)
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialSimulatorGUI(root)
    root.mainloop()