from flask import Flask, render_template, request, redirect, url_for, session
from shuttleai import ShuttleClient
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
API_KEY = "shuttle-ojocjod92qf5mgxpm9yy"

USERS = {
    'admin': '12345',
    'user': 'user1'
}

@app.route("/", methods=["GET", "POST"])
def ia():
    
    if not session.get("logged_in") or (session.get("username") not in USERS):
      return redirect(url_for("login"))

    if request.method == "POST":
        question = request.form.get("question")
        answer = get_ai_response(question)
        return render_template("ia.html", question=question, answer=answer)

    return render_template("ia.html", question=None, answer=None)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USERS and USERS[username] == password:
            session["logged_in"] = True
            session["username"] = username
            return redirect(url_for("ia"))
        else:
            error = "Usuario o contraseña incorrecta"
            return render_template("login.html", error=error)
    return render_template("login.html")

@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

def get_ai_response(question):
    shuttle = ShuttleClient(api_key=API_KEY)
    messages = [{"role": "user", "content": question}]
    response = shuttle.chat_completion(
        model="gpt-4",
        messages=messages,
        stream=False,
        plain=False,
        image=None,
        citations=False
    )
    answer = response['choices'][0]['message']['content']
    answer = format_bold_words(answer)
    return answer

def format_bold_words(text):
    return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
