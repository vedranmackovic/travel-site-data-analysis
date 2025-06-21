from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/destination")
def destination():
    return render_template("destination.html")

@app.route("/destinations")
def destinations():
    return render_template("destinations.html")

if __name__ == '__main__':
    app.run(debug=True)