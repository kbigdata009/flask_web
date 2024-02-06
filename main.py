from flask import Flask , request ,render_template ,redirect,session
import argparse
from pymongo import MongoClient
from passlib.hash import pbkdf2_sha256
import json
from functools import wraps
import bson

app = Flask(__name__)
app.secret_key='ubion8'

mongodb_URI = "mongodb+srv://root:1234@ubion9.fcwrafy.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_URI)
# print("TEST2")
db = client.ubion

@app.route("/", methods=['GET', 'POST'])
def main():
    name="김태경"
    return render_template('main.html', data = name )
    

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    
    elif request.method =='POST':
        #create document
        users = db.users
        username = request.form['username']
        email = request.form.get('email')
        password = request.form.get('password')
        password_hash = pbkdf2_sha256.hash(password)

        user = users.find_one({'email': email})
        if user:
            return redirect('/register')
        # print(username)
        else:
            users.insert_one({
                "username":username,
                "email" : email,
                "password":password_hash
            })
            return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])   
def login():
    if request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        # email 조회 및 password verify
        users = db.users
        result = users.find_one({'email': email})
        print(result)
        if result:
            pw = result['password']

            auth = pbkdf2_sha256.verify(password , pw )
            print(auth)
            if auth == True:
                return redirect('/')
            else:
                return redirect('/login')
        else:
            return redirect('/login')
        
    elif request.method == "GET":
        return render_template('login.html')

@app.route('/list')
# @is_logged_in
def list():
    lists = db.lists
    results = lists.find()
    print(results)
    # for i in results:
    #     print(i)
    return render_template('list.html', list = results )

@app.route('/create_list', methods=['GET', 'POST'])
def create():
    if request.method == "GET":
        return render_template('create_list.html')
    else:
        #create document
        lists = db.lists
        title = request.form['title']
        desc = request.form.get('desc')
        author = request.form.get('author')
        lists.insert_one({
                "title":title,
                "desc" : desc,
                "author":author
            })
        return redirect('/list')

# ids 를 parameter 처리
@app.route('/detail/<list_id>')
def detail(list_id):
    lists = db.lists
    result = lists.find_one({'_id':bson.ObjectId(list_id)})
    print(result)
    return render_template('detail.html', data=result)


@app.route('/edit/<list_id>' , methods=['GET', 'POST'])
def edit(list_id):
    if request.method == 'GET':
        lists = db.lists
        result = lists.find_one({'_id':bson.ObjectId(list_id)})
        print(result)
        return render_template('edit.html', data=result)
    elif request.method == 'POST':
        lists = db.lists
        title = request.form['title']
        desc = request.form.get('desc')
        author = request.form.get('author')
        lists.update_one(
            {'_id' : bson.ObjectId(list_id)},
            {"$set": {
                "title":title,
                "desc" : desc,
                "author":author
            }},
            upsert=False

            )
        
        return redirect('/list')

@app.route('/delete/<list_id>')
def delete(list_id):
    lists = db.lists
    lists.delete_one({"_id": bson.ObjectId(list_id) })
    return redirect('/list')


if __name__ == '__main__':
    # print("TEST1")
    app.run(debug=True)