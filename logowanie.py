from flask import Flask, render_template, request, redirect, url_for
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

@app.route('/Koszyk')
def koszyk():
    return render_template('koszyk.html')

@app.route("/zakup", methods=['GET', 'POST'])
def zakup():

    but = request.form['but']
    

    if but == 'nike_run':
        return render_template('zakup1.html')
    
    elif but == 'but_nike':
        return render_template('zakup2.html')
    
    elif but == 'hoka':
        return render_template('zakup3.html')


if __name__ == "__main__":
    app.run(debug=True)