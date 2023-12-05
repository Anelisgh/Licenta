from flask import jsonify, render_template, request, redirect, url_for, session, flash
from datetime import timedelta
from werkzeug.security import check_password_hash
from app import app, db
from mydatabase import Utilizator, Angajati, Contract, ActIdentitate
from functools import wraps # for @login_required
# de adaugat grafice si diagrame, nu stiu exact unde momentan, dar gasesc eu
# Abilitatea de a filtra și sorta tabelele pe baza diferitelor criterii.
# Incarcarea si descarcarea de fisiere

app.permanent_session_lifetime = timedelta(hours=8) # după cât timp să delogheze utilizatorul

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            flash("Conecteaza-te pentru a accesa pagina.", "info")
            return redirect(url_for("conectare"))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/acasa", methods=["POST", "GET"])
@login_required
def index():
    user = session.get('user', 'Guest')
    return render_template("index.html", user=user)

@app.route("/", methods=["POST", "GET"])
def conectare():
    if request.method == "POST":
        session.permanent = True # Se foloseste app.permanent_session_lifetime = timedelta(hours=8) pt ca utilizatorul sa stea logat doar pt 8 ore
        nume = request.form["nume"]
        parola = request.form['parola']
        user = Utilizator.query.filter_by(nume=nume).first()
        if user:
            if check_password_hash(user.parola, parola):
                session['user'] = nume
                flash(f"Bine ai revenit, {nume}!", "info")  # Adăugați mesajul flash aici
                return redirect(url_for('index'))
            else:
                flash('Parola este incorecta')
        else:
            flash('Numele este incorect')
    else:
        if "user" in session:
            return redirect(url_for('index'))
    return render_template("conectare.html")

@app.route("/deconectare")
def deconectare():
    session.pop("user", None) # Elimină utilizatorul din sesiune.
    flash("Te-ai deconectat cu succes!", "info")
    return redirect(url_for("conectare"))

@app.route("/angajati", methods=["POST", "GET"])
@login_required
def angajati():
    # Interogarea tuturor angajaților
    lista_angajati = Angajati.query.all()
    # Trimiterea datelor către șablonul HTML
    return render_template("angajati.html", url=request.url, angajati=lista_angajati)

@app.route("/documente", methods=["POST", "GET"])
@login_required
def documente():
    lista_angajati = Angajati.query.all()
    return render_template("documente.html", url=request.url, angajati=lista_angajati)

@app.route("/unitate", methods=["POST", "GET"])
@login_required
def unitate():
    return render_template("unitate.html", url=request.url)

@app.route("/angajati/<string:nume_angajat>", methods=["POST","GET"])
@login_required
def contract(nume_angajat):
    angajat = Angajati.query.filter_by(nume=nume_angajat).first()
    if angajat is None:
        return "Nu există niciun angajat cu acest nume."
    lista_contracte = Contract.query.filter_by(angajat_id=angajat.id).all()
    return render_template("contract.html", url=request.url, contracte=lista_contracte)

@app.route('/update_contract', methods=['POST'])
@login_required
def update_contract():
    data = request.get_json()

    if 'rowId' not in data:
        return 'Error: rowId not in data', 400

    if 'columnIndex' not in data:
        return 'Error: columnIndex not in data', 400

    row_id = int(data['rowId'])
    column_index = int(data['columnIndex'])
    new_value = data['newValue']

    contract = db.session.get(Contract, row_id)
    if contract:
        if column_index == 0:
            contract.angajat.nume = new_value
        elif column_index == 1:
            contract.dataAngajare = new_value
        elif column_index == 2:
            contract.functie = new_value
        elif column_index == 3:
            contract.salariu = new_value
        db.session.commit()

    return '', 204

@app.route("/angajati/<string:nume_angajat>/acte_de_identitate", methods=["POST","GET"])
@login_required
def act_identitate(nume_angajat):
    angajat = Angajati.query.filter_by(nume=nume_angajat).first()
    if angajat is None:
        return "Nu există niciun angajat cu acest nume."
    lista_acte = ActIdentitate.query.filter_by(angajat_id=angajat.id).all()
    return render_template("act_identitate.html", url=request.url, act_identitate=lista_acte)

if __name__ == "__main__":
    app.run(debug=True)
