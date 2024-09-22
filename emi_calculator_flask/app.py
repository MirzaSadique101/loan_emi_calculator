from flask import Flask, render_template, request, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for flashing error messages

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get form data
        loan_amount = request.form.get("loanAmount")
        tenure_years = request.form.get("tenureYears")
        interest_rate_flat = request.form.get("interestRateFlat")
        interest_rate_reducing = request.form.get("interestRateReducing")
        loan_type = request.form.get("loanType")

        # Validate inputs
        if not loan_amount or not tenure_years or (loan_type == 'flat' and not interest_rate_flat) or (loan_type == 'reducing' and not interest_rate_reducing):
            flash("Please fill in all required fields.")
            return render_template("index.html", loan_amount=loan_amount, tenure_years=tenure_years, interest_rate_flat=interest_rate_flat, interest_rate_reducing=interest_rate_reducing, loan_type=loan_type)

        # Convert inputs to float
        try:
            loan_amount = float(loan_amount)
            tenure_years = float(tenure_years)
            tenure_months = tenure_years * 12

            if loan_type in ["flat", "both"]:
                interest_rate_flat = float(interest_rate_flat) / 100  # Convert to decimal

            if loan_type in ["reducing", "both"]:
                interest_rate_reducing = float(interest_rate_reducing) / 100  # Convert to decimal

        except ValueError:
            flash("Invalid input: Please enter valid numbers.")
            return render_template("index.html", loan_amount=loan_amount, tenure_years=tenure_years, interest_rate_flat=interest_rate_flat, interest_rate_reducing=interest_rate_reducing, loan_type=loan_type)

        # Initialize result variables
        emi_flat = total_interest_flat = total_amount_flat = None
        emi_reducing = total_interest_reducing = total_payment_reducing = None

        # Calculate EMI for flat structure
        if loan_type in ["flat", "both"]:
            total_interest_flat = loan_amount * interest_rate_flat * tenure_years
            total_amount_flat = loan_amount + total_interest_flat
            emi_flat = total_amount_flat / tenure_months

        # Calculate EMI for reducing structure
        if loan_type in ["reducing", "both"]:
            reducing_monthly_rate = interest_rate_reducing / 12
            emi_reducing = (loan_amount * reducing_monthly_rate * (1 + reducing_monthly_rate)**tenure_months) / \
                           ((1 + reducing_monthly_rate)**tenure_months - 1)
            total_payment_reducing = emi_reducing * tenure_months
            total_interest_reducing = total_payment_reducing - loan_amount

        # Render the results along with the original input values
        return render_template(
            "index.html",
            emi_flat=round(emi_flat, 2) if emi_flat else None,
            total_interest_flat=round(total_interest_flat, 2) if total_interest_flat else None,
            total_amount_flat=round(total_amount_flat, 2) if total_amount_flat else None,
            emi_reducing=round(emi_reducing, 2) if emi_reducing else None,
            total_interest_reducing=round(total_interest_reducing, 2) if total_interest_reducing else None,
            total_payment_reducing=round(total_payment_reducing, 2) if total_payment_reducing else None,
            loan_amount=loan_amount,
            tenure_years=tenure_years,
            interest_rate_flat=interest_rate_flat * 100 if interest_rate_flat else None,  # Reconvert to percentage for display
            interest_rate_reducing=interest_rate_reducing * 100 if interest_rate_reducing else None,  # Reconvert to percentage for display
            loan_type=loan_type
        )
    
    # For GET requests
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
