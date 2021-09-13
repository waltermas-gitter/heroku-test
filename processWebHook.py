from flask import Flask, redirect, url_for, render_template

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


if __name__ == '__main__':
    app.debug = True
    app.run()
