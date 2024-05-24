from flask import Flask, render_template, request, session
from main import enter, emptySlots, exit, paymentRequired, payment

app = Flask(__name__, static_folder="css")
app.secret_key = "secret"
@app.route('/')
def index():
    empty_slots = emptySlots()
    return render_template('home.html', available_slots=empty_slots)

@app.route('/enter', methods=['GET', 'POST'])
def enter_parking():
    if request.method == 'POST':
        plates = request.form["inputPlates"]
        response = enter(plates)
        empty_slots = emptySlots()
        return render_template('enter.html', result=response, available_slots=empty_slots)
    else:
        empty_slots = emptySlots()
        return render_template('enter.html', available_slots=empty_slots)


@app.route('/payment', methods=['GET', 'POST'])
def carInputForPayment():
    if request.method == 'POST':
        plates = request.form["inputPlates"].upper()
        session["payPlates"] = plates
        response = paymentRequired(plates)
        return render_template('payment.html', result1=response, resultPlates=plates, resultType=type(response))
    else:
        return render_template('payment.html')

@app.route('/paymentCar', methods=['GET', 'POST'])
def pay():
    if "payPlates" in session:
        if request.method == "POST":
            money = request.form['inputAmount']
            plates = session["payPlates"]
            response = payment(plates, money)
            return render_template('payment.html', result2=response, resultPlates=plates)
        else:
            return render_template('payment.html')
    else:
        if request.method == "POST":
            return 'Wprowadź numer rejestracyjny samochodu.'
        else:
            return render_template('payment.html')
@app.route('/exit', methods=['GET', 'POST'])
def leave():
    if request.method == 'POST':
        plates = request.form["inputPlates"].upper()
        response = exit(plates)
        empty_slots = emptySlots()
        return render_template('exit.html', result=response, available_slots=empty_slots)
    else:
        empty_slots = emptySlots()
        return render_template('exit.html', available_slots=empty_slots)




if __name__ == '__main__':
     app.run(debug=True)