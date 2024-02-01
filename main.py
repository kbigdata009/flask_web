from flask import Flask , render_template ,request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', name="김태뿅")

@app.route('/hello/<name>')
def hello(name):
    # print(action , sound)
    action = request.args.get('action')
    sound = request.args.get('sound')
    return render_template('hello.html' 
                           , data = {"name":name ,
                                     "action":action,
                                     "sound":sound} )
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        print(username , password)
        return "Success"
    elif request.method == 'GET':
        return render_template('login.html')
    
@app.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        print(username , password)
        return email
    elif request.method == 'GET':
        return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)