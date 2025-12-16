from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()
KEY = os.getenv("MONGO_URI")
client = MongoClient(KEY)




try:
    client.admin.command("ping")
    print("Baza otwarta")

except Exception as e:
    print(f"Baza ma problem {e}")

app = Flask(__name__)

app.secret_key = os.getenv("SESSION_KEY")

class Logowanie:
    def __init__(self):
        db = client["Logowanie"]
        self.konta = db["Konta"]

    def zaloguj(self, login, haslo):
        user = self.konta.find_one({"Login": login})
        if not user:
            return "Zły login"
        if user["Haslo"] == haslo:
            return "Zalogowano pomyślnie"
        return "Błędne hasło"

    def zarejestruj(self, login, haslo):
        if self.konta.find_one({"Login": login}):
            return "Konto już istnieje"
        self.konta.insert_one({"Login": login, "Haslo": haslo})
        return "Konto zostało utworzone"

logowanie = Logowanie()

@app.route("/")
def sklep():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    msg = ""
    if request.method == "POST":
        login_val = request.form["login"]
        haslo_val = request.form["haslo"]
        msg = logowanie.zaloguj(login_val, haslo_val)

        if msg == "Zalogowano pomyślnie":
            session['user'] = login_val

            return redirect(url_for('sklep'))
    return render_template("login.html", msg=msg)

@app.route("/register", methods=["GET", "POST"])
def register_page():
    msg=''
    if request.method == "POST":
        login_val = request.form["login"]
        haslo_val = request.form["haslo"]
        msg = logowanie.zarejestruj(login_val, haslo_val)

    
    return render_template("rejestracja.html", msg=msg)

@app.route("/kupteraz_nike_run")
def kupteraz1():
    return render_template("kupteraz1.html")

@app.route("/kupteraz_nike")
def kupteraz2():
    return render_template("kupteraz2.html")


@app.route("/hoka_run")
def kupteraz3():
    return render_template("kupteraz3.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('sklep'))

@app.route('/Koszyk')
def koszyk():

    nike_run = 0
    but_nike = 0
    hoka = 0

    if 'koszyczek' not in session:
        session['koszyczek'] = []


    if 'user' not in session:
        return redirect(url_for('login_page'))
    

    if 'nike_run' in session['koszyczek']:
        for x in session['koszyczek']:
            if x == 'nike_run':
                nike_run += 1
    
    
    if 'but_nike' in session['koszyczek']:
        for x in session['koszyczek']:
            if x == 'but_nike':
                but_nike += 1



    if 'hoka' in session['koszyczek']:
        for x in session['koszyczek']:
            if x == 'hoka':
                hoka += 1
    


    return render_template('koszyk.html', nike_run=nike_run, but_nike=but_nike, hoka=hoka)

@app.route("/zakup", methods=['GET', 'POST'])
def zakup():

    if 'user' not in session:

        return redirect(url_for('login_page'))

    but = request.form['but']

    if 'koszyczek' not in session:

        session['koszyczek'] = []

    session['koszyczek'].append(but)
    session.modified = True

    print(session['koszyczek'])

    if but == 'nike_run':

        return render_template('zakup1.html')
    
    elif but == 'but_nike':
        return render_template('zakup2.html')
    
    elif but == 'hoka':
        return render_template('zakup3.html')


if __name__ == "__main__":
    app.run(debug=True)