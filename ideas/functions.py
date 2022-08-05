import firebase_admin
import pyrebase
from firebase_admin import auth as fbauth
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Increment
from ideas.viewModel import Item

key = os.getenv('KEY')

cred=credentials.Certificate(Key)
firebase_admin.initialize_app(cred)
pb = pyrebase.initialize_app(FBconfig)
auth=pb.auth()
fauth =firebase_admin
db=firestore.client()
storage=pb.storage()

def get_ideas(uid):
        doc_ref = db.collection("posts")
        query = doc_ref.where("uid","==",uid).order_by('ts', direction=firestore.Query.DESCENDING)
            
        results =query.get()
        print(results)
        items=[]
        for idea in results:
            idea_id=idea.id
            idea=idea.to_dict()
            item=Item.from_ideas(idea,idea_id)
            print (item.title)
            items.append(item)
        return items
def add_files(id,file):
    storage.child(f"Static/profile_pics/{id}").put(file)

def set_idea_lvl(level):
        if level==1:
            return "Back Burner"
        if level==2:
            return "Planning"
        if level==3:
            return "Doing"
        if level==4:
            return "Done"    