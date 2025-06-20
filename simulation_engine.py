import numpy as np

class FinancialSimulator:
    def __init__(
        self, age, initial_capital, monthly_expenses, monthly_investments,
        estimated_returns, inflation_rate, unexpected_events_prob,
        salary_growth_rate, retirement_age, tax_rate,
        investment_type, housing_condition,
        variable_expense_pct, manual_std_dev,
        years=40, num_simulations=30
    ):
        self.age = age
        self.capital = initial_capital
        self.monthly_expenses = monthly_expenses
        self.monthly_investments = monthly_investments
        self.estimated_returns = estimated_returns / 100
        self.inflation_rate = inflation_rate / 100
        self.unexpected_events_prob = unexpected_events_prob / 100
        self.salary_growth_rate = salary_growth_rate / 100
        self.retirement_age = retirement_age
        self.tax_rate = tax_rate / 100
        self.investment_type = investment_type
        self.housing_condition = housing_condition
        self.variable_expense_pct = variable_expense_pct
        self.manual_std_dev = manual_std_dev

        self.years = years
        self.num_simulations = num_simulations
        self.months = years * 12

    def simulate(self):
        all_simulations = []

        for _ in range(self.num_simulations):
            capital = self.capital
            age = self.age
            monthly_expenses = self.monthly_expenses
            monthly_income = self.monthly_investments
            history = []

            for month in range(self.months):
                current_year = month // 12

                # Calcolo rendimento mensile simulato (random walk)
                mean_return = self.investment_type['mean'] / 12
                std_dev = self.investment_type['std_dev'] / np.sqrt(12)
                monthly_return = np.random.normal(mean_return, std_dev)

                # Inflazione mensile
                inflation_monthly = (1 + self.inflation_rate) ** (1 / 12) - 1

                # Aggiustamento delle spese (spese variabili e inflazione)
                variable_factor = np.random.uniform(1 - self.variable_expense_pct, 1 + self.variable_expense_pct)
                expenses_this_month = monthly_expenses * variable_factor
                expenses_this_month *= (1 + inflation_monthly) ** month

                # Imprevisti occasionali
                if np.random.rand() < self.unexpected_events_prob / 12:
                    expenses_this_month += np.random.uniform(500, 3000)

                # Pensionamento: stop investimenti
                if age + month / 12 >= self.retirement_age:
                    monthly_income = 0

                # Applica rendimento e tassazione
                profit = capital * monthly_return
                if profit > 0:
                    profit *= (1 - self.tax_rate)
                capital += profit

                # Aggiungi investimenti, togli spese
                capital += monthly_income
                capital -= expenses_this_month

                # Impedisci che vada sotto 0
                capital = max(capital, 0)

                history.append(capital)

                # Crescita dello stipendio annuale
                if month % 12 == 0 and month > 0:
                    monthly_income *= (1 + self.salary_growth_rate)

            all_simulations.append(history)

        return all_simulations
