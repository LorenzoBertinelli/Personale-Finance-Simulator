import numpy as np

class FinancialSimulator:
    def __init__(self, age, initial_capital, monthly_expenses, monthly_investments,
                 estimated_returns, inflation_rate, unexpected_events_prob, salary_growth_rate,
                 retirement_age, tax_rate, investment_type, housing_condition,
                 variable_expense_pct=0.1, std_dev=0.10):
        self.age = age
        self.initial_capital = initial_capital
        self.monthly_expenses = monthly_expenses
        self.monthly_investments = monthly_investments
        self.estimated_returns = estimated_returns / 100
        self.inflation_rate = inflation_rate / 100
        self.unexpected_events_prob = unexpected_events_prob
        self.salary_growth_rate = salary_growth_rate / 100
        self.retirement_age = retirement_age
        self.tax_rate = tax_rate / 100
        self.investment_type = investment_type
        self.housing_condition = housing_condition
        self.variable_expense_pct = variable_expense_pct
        self.std_dev = std_dev

    def simulate(self, years=30, num_simulations=30):
        simulations = []
        for _ in range(num_simulations):
            capital = self.initial_capital
            age = self.age
            capital_history = []

            for month in range(years * 12):
                current_age = age + month // 12

                monthly_return = np.random.normal(
                    loc=self.investment_type['mean'] / 12,
                    scale=self.std_dev / 12
                )
                capital *= (1 + monthly_return)
                if monthly_return > 0:
                    capital *= (1 - self.tax_rate)

                if current_age >= self.retirement_age:
                    adjusted_expenses = self.monthly_expenses * 0.8
                else:
                    adjusted_expenses = self.monthly_expenses

                expense_variation = adjusted_expenses * (
                    1 + np.random.uniform(-self.variable_expense_pct, self.variable_expense_pct)
                )
                capital -= expense_variation

                if current_age < self.retirement_age:
                    capital += self.monthly_investments

                if month % 60 == 0 and month > 0:
                    if np.random.rand() < self.unexpected_events_prob:
                        capital -= np.random.randint(1000, 5000)

                capital /= (1 + self.inflation_rate / 12)

                if self.housing_condition == "affitto":
                    capital -= 500
                elif self.housing_condition == "mutuo":
                    capital -= 700

                capital_history.append(max(capital, 0))

            simulations.append(capital_history)

        return simulations