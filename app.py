from datetime import date
from flask import Flask, render_template, request

app = Flask(__name__)

def age_on(born, today=None):
    today = today or date.today()
    if born > today:
        raise ValueError("Birth date is in the future")
    years = today.year - born.year
    months = today.month - born.month
    days = today.day - born.day
    if days < 0:
        months -= 1
        prev_m = today.month - 1 or 12
        prev_y = today.year if today.month > 1 else today.year - 1
        days += (date(today.year, today.month, 1) - date(prev_y, prev_m, 1)).days
    if months < 0:
        years -= 1
        months += 12
    return years, months, days

@app.route("/", methods=["GET", "POST"])
def home():
    result = error = None
    birth = ""
    if request.method == "POST":
        birth = request.form.get("birth_date", "")
        try:
            y, m, d = age_on(date.fromisoformat(birth))
            result = {"years": y, "months": m, "days": d}
        except ValueError:
            error = "Please enter a valid date that is not in the future."
    return render_template("index.html", result=result, error=error,
                           birth=birth, today=date.today().isoformat())

if __name__ == "__main__":
    app.run(debug=True)
