from flask import Flask, render_template, request, redirect, url_for, session
from shuttleai import ShuttleClient
import re

app = Flask(__name__)
app.secret_key = "tu_clave_secreta"  # Asegúrate de cambiar esto a una clave segura en un entorno de producción
API_KEY = "shuttle-ojocjod92qf5mgxpm9yy"
USER = "admin"
PASSWORD = "123"

# Ruta para el inicio de sesión
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == USER and password == PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("ia"))
    return render_template("login.html")

# Ruta para la página de la IA (página principal)
@app.route("/", methods=["GET", "POST"])
def ia():
    if not session.get("logged_in"):
        return redirect(url_for("login"))

    if request.method == "POST":
        question = request.form.get("question")
        answer = get_ai_response(question)
        return render_template("ia.html", question=question, answer=answer)

    return render_template("ia.html", question=None, answer=None)

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
