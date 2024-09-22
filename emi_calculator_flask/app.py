# app.py
from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Retrieve form data
        loan_amount = request.form.get("loanAmount")
        tenure_years = request.form.get("tenureYears")
        interest_rate_flat = request.form.get("interestRateFlat")
        interest_rate_reducing = request.form.get("interestRateReducing")
        loan_type = request.form.get("loanType")

        # Input Validation
        error_message = None

        if not loan_amount or not tenure_years:
            error_message = "Please fill in the Loan Amount and Tenure."
        elif loan_type == 'flat' and not interest_rate_flat:
            error_message = "Please enter the Flat Interest Rate."
        elif loan_type == 'reducing' and not interest_rate_reducing:
            error_message = "Please enter the Reducing Interest Rate."
        elif loan_type == 'both' and (not interest_rate_flat or not interest_rate_reducing):
            error_message = "Please enter both Flat and Reducing Interest Rates."

        if error_message:
            flash(error_message)
            return render_template("index.html")

        # Convert inputs to floats
        try:
            loan_amount = float(loan_amount)
            tenure_years = float(tenure_years)
            tenure_months = tenure_years * 12

            if loan_type == "flat":
                interest_rate_flat = float(interest_rate_flat) / 100
            if loan_type == "reducing":
                interest_rate_reducing = float(interest_rate_reducing) / 100
            if loan_type == "both":
                interest_rate_flat = float(interest_rate_flat) / 100
                interest_rate_reducing = float(interest_rate_reducing) / 100

        except ValueError:
            flash("Invalid input: Please enter valid numerical values.")
            return render_template("index.html")

        # Initialize result variables
        emi_flat = total_interest_flat = total_amount_flat = None
        emi_reducing = total_interest_reducing = total_payment_reducing = None

        # Calculate EMI for Flat Structure
        if loan_type in ["flat", "both"]:
            total_interest_flat = loan_amount * interest_rate_flat * tenure_years
            total_amount_flat = loan_amount + total_interest_flat
            emi_flat = total_amount_flat / tenure_months

        # Calculate EMI for Reducing Structure
        if loan_type in ["reducing", "both"]:
            reducing_monthly_rate = interest_rate_reducing / 12
            emi_reducing = (loan_amount * reducing_monthly_rate * (1 + reducing_monthly_rate)**tenure_months) / \
                           ((1 + reducing_monthly_rate)**tenure_months - 1)
            total_payment_reducing = emi_reducing * tenure_months
            total_interest_reducing = total_payment_reducing - loan_amount

        # Render results
        return render_template(
            "index.html",
            emi_flat=round(emi_flat, 2) if emi_flat else None,
            total_interest_flat=round(total_interest_flat, 2) if total_interest_flat else None,
            total_amount_flat=round(total_amount_flat, 2) if total_amount_flat else None,
            emi_reducing=round(emi_reducing, 2) if emi_reducing else None,
            total_interest_reducing=round(total_interest_reducing, 2) if total_interest_reducing else None,
            total_payment_reducing=round(total_payment_reducing, 2) if total_payment_reducing else None
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
