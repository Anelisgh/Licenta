from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from datetime import date

class Angajati(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True)
    nume = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    actIdentitate = db.Column(db.String(120),unique=True, nullable=False)
    functie = db.Column(db.Enum('Director', 'Secretara', 'Consilier', 'Economist'), primary_key=True, nullable=False)
    dataAngajare = db.Column(db.String(20), primary_key=True, nullable=False)
    
class Utilizator(db.Model):
    id = db.Column(db.Integer, db.ForeignKey('angajati.id'), primary_key=True)
    nume = db.Column(db.String(80), unique=True, nullable=False)
    parola = db.Column(db.String(120), nullable=False)
    angajat = db.relationship('Angajati', backref=db.backref('utilizatori', lazy=True))
    
class Contract(db.Model):
    id = db.Column(db.Integer, unique=True, primary_key=True) 
    angajat_id = db.Column(db.Integer, db.ForeignKey('angajati.id'), unique=True, nullable=False)  
    dataAngajare = db.Column(db.String(20), db.ForeignKey('angajati.dataAngajare'), nullable=False)  
    functie = db.Column(db.Enum('Director', 'Secretara', 'Consilier', 'Economist'), db.ForeignKey('angajati.functie'), nullable=False) 
    vechimeInInstitutie = db.Column(db.Integer, nullable=False)
    vechimeAnterioara = db.Column(db.Integer, nullable=False)
    vechimeTotala = db.Column(db.Integer, nullable=False)
    salariu = db.Column(db.Integer, nullable=False)
    angajat = db.relationship('Angajati', backref=db.backref('contracte', lazy=True), foreign_keys=[angajat_id])

class ActIdentitate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    angajat_id = db.Column(db.Integer, db.ForeignKey('angajati.id'), nullable=False)
    angajat_nume = db.Column(db.String(80), db.ForeignKey('angajati.nume'), nullable=False)
    dataNastere = db.Column(db.String(20), nullable=False)
    angajat_actIdentitate = db.Column(db.String(120), db.ForeignKey('angajati.actIdentitate'), nullable=False)
    CNP = db.Column(db.Integer, unique=True)
    dataEmitere = db.Column(db.String(20), nullable=False)
    dataExpirare = db.Column(db.String(20), nullable=False)
    angajat = db.relationship('Angajati', backref=db.backref('acte_identitate', lazy=True), foreign_keys=[angajat_id])
    
def add_angajat(id, nume_angajat, actIdentitate, functie, dataAngajare, #Angajati
                nume_utilizator, parola, #Utilizator
                vechimeAnterioara, salariu, #Contract
                dataNastere, CNP, dataEmitere, dataExpirare): #ActIdentitate
    with app.app_context():
        # Crearea unui nou angajat
        nou_angajat = Angajati(id=id, nume=nume_angajat, actIdentitate=actIdentitate, functie=functie, dataAngajare=dataAngajare)
        db.session.add(nou_angajat)

        # Crearea unui nou utilizator cu același ID
        password_hash = generate_password_hash(parola)
        nou_utilizator = Utilizator(id=id, nume=nume_utilizator, parola=password_hash)
        db.session.add(nou_utilizator)
        
        # Calculează vechimea totală și vechimea in instituție
        vechimeInInstitutie = date.today().year - dataAngajare.year
        vechimeTotala = vechimeInInstitutie + int(vechimeAnterioara)
        
        # Crearea unui nou contract
        nou_contract = Contract(angajat_id=id, dataAngajare=dataAngajare, functie=functie, vechimeInInstitutie=vechimeInInstitutie, vechimeAnterioara=vechimeAnterioara, vechimeTotala=vechimeTotala, salariu=salariu)
        db.session.add(nou_contract)

        # Crearea unui nou act de identitate
        nou_act = ActIdentitate(angajat_id=id, angajat_nume=nume_angajat, dataNastere=dataNastere, angajat_actIdentitate=actIdentitate, CNP=CNP, dataEmitere=dataEmitere, dataExpirare=dataExpirare)
        db.session.add(nou_act)
    
        # Salvarea modificărilor în baza de date
        db.session.commit()

with app.app_context():
    db.create_all()
    # Adăugarea angajaților și a utilizatorilor
    # Pentru date se foloseste: date(an, luna, zi)
    add_angajat(1, 'Popescu Alina', 'AB 123456', 'Director', date(2022, 1, 26), # id, nume_angajat, actIdentitate, functie, dataAngajare,
                              'Anelis', '123', #nume_utilizator, parola,
                              '12', 10000, #vechimeAnterioara, salariu,
                              date(1989, 6, 23), 2890623406033, date(2014,6,23), date(2024,6,23)) #dataNastere, CNP, dataEmitere, dataExpirare
    add_angajat(2, 'Ionescu Claudia', 'CD 789012', 'Secretara', date(2023, 6, 23),
                              'Alina', '456',
                              '10', 5500,
                              date(1992, 4, 25), 2920425409191, date(2017,4,25), date(2027,4,25))
    add_angajat(3, 'Stanescu Mircea', 'EF 345678', 'Consilier', date(2022, 8, 29),
                              'Emma', '789',
                              '8', 6000,
                              date(1991, 9, 13), 1910913408015, date(2016,9,13), date(2026,9,13))
    add_angajat(4, 'Vasile Mihai','GH 901234', 'Consilier', date(2022, 11, 9),
                              'Mihai', '147',
                              '7', 6000,
                              date(1990, 12, 25), 1901225408381, date(2015,12,15), date(2025,12,15))
    add_angajat(5, ' Maria Carmen', 'IJ 567890', 'Economist', date(2023, 11, 14),
                              'Carmen', '258',
                              '2', 4000,
                              date(1992, 2, 7), 2920207405441, date(2017,2,7), date(2027,2,7))



