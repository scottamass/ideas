#v.5

import datetime

import os

import firebase_admin
import pyrebase
from firebase_admin import auth as fbauth
from firebase_admin import credentials, firestore


from flask import Flask, redirect, render_template, request, send_from_directory, session, url_for

def create_app():
    app=Flask(__name__)

    app.config['SESSION_PERMANENT'] = True
    app.secret_key = "shhhh"

    FBconfig= {
        "apiKey": os.getenv('APIKEY'),
        "authDomain": "ideapad-9e040.firebaseapp.com",
        "databaseURL":"",
        "projectId": "ideapad-9e040",
        "storageBucket": "ideapad-9e040.appspot.com",
        "messagingSenderId": "227399805304",
        "appId": "1:227399805304:web:cd7e7b86e9c8b99999808d"
    }

    Key = {
    "type": "service_account",
    "project_id": "ideapad-9e040",
    "private_key_id": os.getenv('PRIV_KEY_ID'),
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDMpPzs+r34dGar\nvUGMWKviGeG8KDNh1QTULREUoXledd9RWrR5JBEMmLv1A1Ns74yNGlMxG/wSyubW\nhLG7HunTFoYbrTH5zkJdrbh0Cas5gP1KVQf0/SeciHK9wj4Qa9nmiU1CEEsnNfEe\na1YJycFWpgd/0s0OS9V4Do0QHsWxQICROzkNmLUbKXjuYoNK+Qh1up/7/L+7febC\nAWshhIdwVHFBVrF090XZzxQ5vMh9X103V6TGJNwRDKE2CDGUyiRaNcrBjwlBHFnS\nii5WFEopkAG3TImvWPxTBU0zmAkSgrNCBN9BO3A/9NyxhMqFjCjpnIV2cHvO90ES\nteCbiMYFAgMBAAECggEAUDtHJinQHP6V2jMi5cFF8ikvhTNFoc+ASyc4ERyVluEj\noqOrKetn+8ZNumuJY6YvNorhntlX5I5EHkp7297s0WN9RJCMjWG+Rzf6nxPDW5Ik\nu+XGbthplUcxpQ/ogUunbGjcL1BwBnlxhPmUC9ZbxHrnacfduQMmOCGMUIuf+jOa\nL95KPB/TLMXdAYx8VaaGSKORQfHkwh3L0sh4VERwA0uieWjTji/12PiFiBOUz65V\nQzhXdxNVA6CSE3FCmGaWBgo8OHtpTkQs6kUkK49mTYqa3GRNYfQfAYgTErxmTY8V\nWEE5vj9M0pH4SV/B60IuxA4JJNmlRi07fpjmyEWMqQKBgQDp+REMLlKTJUwLkgGj\nrXgXrWt9GxpaWdGpvCFHc54uskNk7JGH30hn2F+zUTlCyQb+s6lVUuEKhi+Zi8Ya\nuV5khStQnTkCT4q+HYpRm9TP8RCulJrl7KB698kZzT/HDrN7X8wQe4DIHTrnkD49\nfV+bxa3G9yjTdOdVG9EXP41P8wKBgQDf6RU2EwDfvNLyqEPNKWGn9U4uSA3UWpz5\nms5GGwLwWTNTGdBKu5vRGooJH+Y2BkDENJhiTo0/fTe4S98SjmlvALKyY2NhVb8C\nfDUaMd99wh95Aane11R7pA6VDZiNKMy9BXyZS0Sy/z+tjzEJdwGMiknq2HHSUcma\nbO+xVfYIJwKBgQDQgP+7LjCyJqOtD/FcDoOd/hJzC8shRze7nga+KP+HN58telB6\nl/VrbXxjTXfM117fbfXyLoiTm18h41ioihbfV3lxPpsGPyIyKBsSfN9aa8Zk/dNI\nIOYmj1hsIOe8GZLC2Gz/J0BtlPbgUz/UBj1EkRY64BlGz8AzrTVZFW52FwKBgQC9\nVcG65NzTVD7oM8KJZFmQhcxjNEiFbU3Zfr635zVX+YV92pEX8IY0jgV068Vln2n6\nvyKv1g54RjDspTNu5H9g/q0cTRCHCNOojVD14oBCPfkRAIgcx+ZHWpV+Em4RxxNB\nLreKhGwGE/JLl452m2vy5CjW7clpeAFKlJ0mTjLp9wKBgCrPMOsMdD5rxoVjL8zV\nw4TNAs+yxR9yD9w9xjEy9+YKUPIWbrkYh9O8nLXQMZlXMFt5tI7B2TUJpmDGacnX\ngHcmrh2AhsVPd4/B2rGW75aggaTGmr7omT4zOAKlQlY1dD4o/lEu8qD4gIEZ89e4\n3Plsi9W3xwVTNrdKcuY8kyjS\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-888uq@ideapad-9e040.iam.gserviceaccount.com",
    "client_id": "103732885096478217662",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-888uq%40ideapad-9e040.iam.gserviceaccount.com"
    }

    key = os.getenv('KEY')

    cred=credentials.Certificate(Key)
    firebase_admin.initialize_app(cred)
    pb = pyrebase.initialize_app(FBconfig)
    auth=pb.auth()
    fauth =firebase_admin
    db=firestore.client()

    @app.before_request
    def make_sessions_permanant():
        session.permanent =True

    """ @app.route('/static/<path:path>')
    def static_dir(path):
        return send_from_directory("static",path) """


    @app.route('/',methods=['GET','POST'])
    def home():
        print(os.environ.get('APIKEY'))
        if('user' in session ):
            uid = session['user']
            print(uid)
            user_query = db.collection('users').document(uid).get()
            name = user_query.to_dict()['display name']
            if request.method == 'POST':
                body=request.form['idea']
                uid = uid
                data = {'body':body,'uid':uid, 'idea':'on the back burner','level':1, 'ts':datetime.datetime.now() }
                db.collection('posts').add(data)
                return redirect(url_for('home'))
            doc_ref = db.collection("posts")
            query = doc_ref.where("uid","==",uid).order_by('ts', direction=firestore.Query.DESCENDING)
            #doc_ref = db.collection("posts").where("uid", "==", uid).get()
            results =query.get()
            print(results)
            for doc in results:
                print(doc.to_dict())
            return render_template('index.html' ,uid=uid,msg=name ,doc_ref=results)
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
            uid=display_name
            email = request.form['username']
            password = request.form['pwd']
            #user=auth.create_user_with_email_and_password(email,password)
            user=fbauth.create_user(uid=uid,display_name=display_name,email=email,password=password)
            id=fbauth.get_user_by_email(email)
            print(id.uid)
            db.collection('users').document(id.uid).set({"display name":display_name,"email":id.email,"uid":display_name})
            
                
            return redirect(url_for('home'))  


        
        return render_template('signup.html')

    @app.route('/logout')
    def logout():
        session.pop('user')
        return redirect(url_for('home'))

    @app.route('/user/<string:id>')
    def profile(id):
        req_user =db.collection('users').document(id).get()
        user_details=req_user.to_dict()
        
        return render_template('userprofile.html',user_details = user_details)

    @app.route('/edit_user/<string:id>',methods=['GET','POST'])
    def edit_profile(id):
        
            if id == session['user']:
                req_user =db.collection('users').document(id).get()
                user_details=req_user.to_dict()
                if request.method =='POST':
                    bio = request.form['bio']
                    db.collection('users').document(id).set({'bio':bio},merge=True)
                    return redirect(request.url)

                return render_template('editprof.html',user_details = user_details)
        
            else: return "You Shall not Pass",401
    if __name__ =='__main__':
        app.run()




    """ fbauth.create_user(
        email='user@example.com',
        email_verified=False,
        phone_number='+15555550100',
        password='secretPassword',
        display_name='John Doe',
        disabled=False) """       
    return app     
