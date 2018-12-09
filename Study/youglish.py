from ServerStart import app
from flask import render_template

@app.route("/Web/Youglish")
def show_youglish():
    return render_template('youglish.html')