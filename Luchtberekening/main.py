from flask import Flask, render_template, request, redirect, url_for, session

import random

app = Flask(__name__)
app.secret_key = 'geheime_sleutel'  # Nodig voor sessies

begindrukLijst = [270, 275, 280, 285, 290, 295, 300, 305, 310, 315, 320, 325, 330]
aankomstdrukLijst = [190, 200, 210, 220, 230, 240, 250]
luchtverbruikLijst = [40, 50, 60, 70, 80, 90, 100]
reservedruk = 55

def terugtochtHeen(begindruk, reservedruk):
    return (begindruk + reservedruk) / 2

def terugtochtWerk(aankomstdruk, begindruk, reservedruk):
    return (begindruk - aankomstdruk) + reservedruk

def hoeveelheidLucht(druk, inhoud=6):
    return druk * inhoud

def werktijd(liter, luchtverbruik):
    tijd = liter / luchtverbruik
    minutes = int(tijd)
    seconds = round((tijd - minutes) * 60)
    return f"{minutes}:{seconds:02d}", tijd

@app.route('/')
def index():
    session['begindruk'] = random.choice(begindrukLijst)
    session['aankomstdruk'] = random.choice(aankomstdrukLijst)
    session['luchtverbruik'] = random.choice(luchtverbruikLijst)
    return render_template('index.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html', message=session.get('message', ''), next_url=session.get('next_url', url_for('index')))

@app.route('/startberekening', methods=['GET', 'POST'])
def startberekening():
    begindruk = session.get('begindruk', 300)
    correct_answer = terugtochtHeen(begindruk, reservedruk)

    if request.method == 'POST':
        user_answer = float(request.form['answer'])
        if user_answer == correct_answer:
            session['message'] = "Goed gedaan!"
        else:
            session['message'] = f"Fout! Het juiste antwoord was: {correct_answer} bar."
        session['next_url'] = url_for('terugtocht_werk')
        return redirect(url_for('feedback'))

    return render_template('terugtocht_heen.html', begindruk=begindruk, reservedruk=reservedruk)

@app.route('/terugtocht_werk', methods=['GET', 'POST'])
def terugtocht_werk():
    begindruk = session.get('begindruk', 300)
    aankomstdruk = session.get('aankomstdruk', 200)
    correct_answer = terugtochtWerk(aankomstdruk, begindruk, reservedruk)

    if request.method == 'POST':
        user_answer = float(request.form['answer'])
        if user_answer == correct_answer:
            session['message'] = "Goed gedaan!"
        else:
            session['message'] = f"Fout! Het juiste antwoord was: {correct_answer} bar."
        session['next_url'] = url_for('werktijd_page')
        return redirect(url_for('feedback'))

    return render_template('terugtocht_werk.html', begindruk=begindruk, aankomstdruk=aankomstdruk, reservedruk=reservedruk)

@app.route('/werktijd', methods=['GET', 'POST'])
def werktijd_page():
    begindruk = session.get('begindruk', 300)
    aankomstdruk = session.get('aankomstdruk', 200)
    luchtverbruik = session.get('luchtverbruik', 40)
    terugtochtdruk = terugtochtWerk(aankomstdruk, begindruk, reservedruk)

    werkDruk = aankomstdruk - terugtochtWerk(aankomstdruk, begindruk, reservedruk)
    lucht = hoeveelheidLucht(werkDruk)
    correct_answer, correct_answer2 = werktijd(lucht, luchtverbruik)
    round(correct_answer2, 2)

    if request.method == 'POST':
        user_answer = request.form['answer']
        if user_answer == correct_answer:
            session['message'] = "Goed gedaan!"
        else:
            session['message'] = f"Fout! Het juiste antwoord was: {correct_answer} minuten."
        session['next_url'] = url_for('index')
        return redirect(url_for('feedback'))

    return render_template('werktijd.html', begindruk=begindruk, aankomstdruk=aankomstdruk, luchtverbruik=luchtverbruik, reservedruk=reservedruk, terugtochtdruk=terugtochtdruk)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
