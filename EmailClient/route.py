from flask import Flask, render_template, request, redirect
import utils

app = Flask(__name__)


# username = "nhungleqaz2@gmail.com"
# password = "pfnrbgsnqhuehhmb"


@app.route("/", methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get("email")
        password = request.form.get("password")

        utils.login(username=username,password= password)

        return redirect('/home')
    return render_template("login.html")
    


@app.route('/home')
def read_page():
    return render_template('home.html', mails = utils.listMails())



if __name__ == "__main__":
    app.run(debug=True)