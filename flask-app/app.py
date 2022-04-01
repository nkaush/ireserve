from flask import Flask, render_template
from db import *

app = Flask(__name__)

@app.route('/')
def home(): 
    return render_template(
        "main_page.html", name="neil"
    )

if __name__ == '__main__':
    app.run()