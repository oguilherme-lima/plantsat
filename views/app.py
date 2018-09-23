from flask import Flask
from flask import render_template

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def hello():
    return render_template('index.html', titulo="PlantSat")

if __name__ == '__main__':
    app.run()