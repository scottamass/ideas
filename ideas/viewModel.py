
def details(idea):
        if 'details' in idea:
            return idea['details']
        else:
            return ""  

class Item:
    def __init__(self,id,title,level,date,user,bio=False):
        self.id=id
        self.title=title
        self.level =level
        
        if level==1:
            self.status = "Back Burner"
        if level==2:
            self.status = "Planning"
        if level==3:
            self.status = "Doing"
        if level==4:
            self.status = "Done"
        self.date =date
        self.user=user
        
                
        self.details=bio
            
    
           
  

    @classmethod
    def from_ideas(cls,idea,idea_id):
        return cls(idea_id,idea['body'],idea['level'],idea['ts'],idea['uid'],details(idea))
