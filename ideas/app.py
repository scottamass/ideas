
import datetime
import json

import firebase_admin
import pyrebase
from firebase_admin import auth as fbauth
from firebase_admin import credentials, firestore

from flask import Flask, redirect, render_template, request, session, url_for

#App Config
app=Flask(__name__)


app.secret_key = "shhhh"



cred=credentials.Certificate('Key.json')
firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('FBcondig.json')))
auth=pb.auth()
fauth =firebase_admin
db=firestore.client()



@app.route('/',methods=['GET','POST'])
def home():
    
    if('user' in session ):
        uid = session['user']
        print(uid)
        if request.method == 'POST':
            body=request.form['idea']
            uid = uid
            data = {'body':body,'uid':uid, 'ts':datetime.datetime.now() }
            db.collection('posts').add(data)
            return redirect(url_for('home'))
        doc_ref = db.collection("posts").where("uid", "==", uid).get()
        for doc in doc_ref:
            print(doc.to_dict())
        return render_template('index.html' ,msg=uid ,doc_ref=doc_ref)
    else:
        return redirect(url_for('login'))   



#api route signin new users 
@app.route('/login', methods=['GET','POST'])
def login():
    
        if request.method == 'POST':
            email = request.form ['username']
            password= request.form ['pwd']

            try:
                user = auth.sign_in_with_email_and_password(email,password)
                id=fbauth.get_user_by_email(email)  
                print(id.uid)
                uid = id.uid
                session['user'] = uid
            
                return redirect(url_for('home'))
            except:
                return "incorrect password"    
        
        return render_template('login.html')        
    

@app.route('/sign-up', methods=['GET','POST'])
def signup():
    if request.method == 'POST': 
        display_name = request.form['name']
        email = request.form['username']
        password = request.form['pwd']
        user=auth.create_user_with_email_and_password(email,password)
        id=fbauth.get_user_by_email(email)
        print(id.uid)
        db.collection('users').document(id.uid).set({"display name":display_name,"email":id.email,"uid":id.uid})
        
             
        return redirect(url_for('home'))  


    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect(url_for('home'))

@app.route('/user/<string:id>')
def profile(id):
    req_user =db.collection('users').document(id).get()
    print(req_user.to_dict())
       
    return "hello " + id
    
if __name__ =='__main__':
    app.run()




""" fbauth.create_user(
    email='user@example.com',
    email_verified=False,
    phone_number='+15555550100',
    password='secretPassword',
    display_name='John Doe',
    disabled=False) """        
