from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route('/')
def hello():
    return ("Hello world")

@app.route('/<name>')
def user(name):
    return (f"hello {name}")

@app.route('/hello/<name>')
def hellouser(name):
    return render_template("index.html", name=name)

@app.route('/trythis')
def trythis():
    return render_template("trythis.html")

@app.route('/login', methods = ["POST", "GET"])
def login():
    if request.method == 'POST':
        user = request.form["nm"]
        print(user)
        return redirect(url_for("userlogin", usergin=user))
    else:
        return render_template("login.html")

@app.route('/<usergin>')
def userlogin(userlogin):
    return (f"hello {userlogin}")

@app.route('/bootstrap')
def bootstrap():
    return render_template("bootstrap.html")

if __name__ == '__main__':
    app.debug = True
    app.run()
