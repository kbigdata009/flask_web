from flask import Flask , render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name="김태뿅")

@app.route('/hello')
def hello():
    return "안녕! 반가워!"

if __name__ == '__main__':
    app.run(debug=True)