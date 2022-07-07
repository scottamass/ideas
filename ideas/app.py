
import firebase_admin
from firebase_admin import credentials, firestore ,auth as fbauth
from flask import Flask, redirect, render_template,request,session,url_for
import pyrebase
import json



#App Config
app=Flask(__name__)


app.secret_key = "shhhh"



cred=credentials.Certificate('Key.json')
firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(json.load(open('FBcondig.json')))
auth=pb.auth()
fauth =firebase_admin
db=firestore.client()



@app.route('/')
def home():
    if('user' in session ):
        msg = session['user']
        
        return render_template('index.html' ,msg=msg)
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
                print(id.display_name)
                session['user'] = email
            
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
    
if __name__ =='__main__':
    app.run()