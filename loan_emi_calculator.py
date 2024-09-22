import numpy as np
import pandas as pd

# Loan details
loan_amount = 1800000  # in INR
tenure_years = 7
tenure_months = tenure_years * 12

# Interest rates
flat_rate = 8.99 / 100
reducing_rate = 9.6 / 100

# Monthly interest rates for reducing structure
reducing_monthly_rate = reducing_rate / 12

# EMI for flat structure
total_interest_flat = loan_amount * flat_rate * tenure_years
total_amount_flat = loan_amount + total_interest_flat
emi_flat = total_amount_flat / tenure_months

# EMI for reducing structure using formula
emi_reducing = (loan_amount * reducing_monthly_rate * (1 + reducing_monthly_rate)**tenure_months) / ((1 + reducing_monthly_rate)**tenure_months - 1)

# Total interest and amount for reducing structure
total_payment_reducing = emi_reducing * tenure_months
total_interest_reducing = total_payment_reducing - loan_amount

# Create a table for comparison
data = {
    'Loan Type': ['Flat Structure', 'Reducing Structure'],
    'Interest Rate (%)': [flat_rate * 100, reducing_rate * 100],
    'EMI (INR)': [emi_flat, emi_reducing],
    'Total Interest (INR)': [total_interest_flat, total_interest_reducing],
    'Total Amount Payable (INR)': [total_amount_flat, total_payment_reducing]
}

# Create DataFrame for visualization
df = pd.DataFrame(data)

# Save DataFrame to an Excel file
output_file = '/home/user/Downloads/python_bible/python-bible/loan_emi_calculator/loan_comparison_table.xlsx'
df.to_excel(output_file, index=False)

output_file

# Display the DataFrame
# import ace_tools as tools; tools.display_dataframe_to_user(name="Loan Comparison Table", dataframe=df)
