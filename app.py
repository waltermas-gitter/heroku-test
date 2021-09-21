from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
# from send_mail import send_mail

app = Flask(__name__)

# ENV = 'dev'
ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/lexus'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://opkgjmueikhwdp:7eae4fe3e5cc93a07609daf0e725d02c17a9a696d2fdab43baa2df2d8e667285@ec2-44-198-223-154.compute-1.amazonaws.com:5432/d145g85r87to1g'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

class Notas(db.Model):
    __tablename__ = 'notas'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), unique=True)
    nota = db.Column(db.Text())
    url = db.Column(db.String(300))

    def __init__(self, titulo, nota, url):
        self.titulo = titulo
        self.nota = nota
        self.url = url
 
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        customer = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer, dealer, rating, comments)
        if customer == '' or dealer == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            # send_mail(customer, dealer, rating, comments)
            return render_template('success.html')
        return render_template('index.html', message='You have already submitted feedback')

@app.route('/form')
def llenarFormulario():
    return render_template('form.html')

@app.route('/submitnota', methods=['POST'])
def submitnota():
    if request.method == 'POST':
        titulo = request.form['titulo']
        nota = request.form['nota']
        url = request.form['url']
        if db.session.query(Notas).filter(Notas.titulo == titulo).count() == 0:
            data = Notas(titulo, nota, url)
            db.session.add(data)
            db.session.commit()
        else:
            return ('titulo ya existe')
        return redirect(url_for('notaslist'))

@app.route('/notas')
def notaslist():
    query = db.session.query(Notas).all()
    for item in query:
        print(query)
    return render_template('notaslist.html', notas=query)


@app.route('/edit')
def edit():
    idNota = request.args.get("idNota")
    query = db.session.query(Notas).filter(Notas.id == idNota).first()
    return render_template('editarnota.html', nota=query)


@app.route('/submitnotaeditada', methods=['POST'])
def submitnotaeditada():
    if request.method == 'POST':
        titulo = request.form['titulo']
        nota = request.form['nota']
        url = request.form['url']
        query = db.session.query(Notas).filter(Notas.titulo == titulo).first()
        query.nota = nota
        query.url = url
        db.session.commit()
    return redirect(url_for('notaslist'))
        
@app.route('/delete')
def delete():
    idNota = request.args.get("idNota")
    query = db.session.query(Notas).filter(Notas.id == idNota).first()
    return render_template('deleteconfirm.html', nota=query)

@app.route('/deleteconfirm', methods=['POST'])
def deleteconfirm():
    titulo = request.form['titulo']
    query = db.session.query(Notas).filter(Notas.titulo == titulo).delete()
    db.session.commit()
    return redirect(url_for('notaslist'))
if __name__ == '__main__':
    app.run()
