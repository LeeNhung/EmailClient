from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello():
    mail={'Subject': 'subject','From':'From', 'Date':'Date', 'Content':'body'}

    return render_template('test.html', mail = mail)

if __name__ == "__main__":
    app.run()