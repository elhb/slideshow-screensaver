import os
import random
import mimetypes

class Pictures():

    def __init__(self, pics_root=os.path.expanduser("~/Pictures")):
        
        self.pics_root = pics_root
        
        self.generate_list()
    
    def generate_list(self):
        
        self.pics = []
        for d in os.walk(self.pics_root):
            directory = d[0]
            
            for filename in d[2]:
                filepath = os.path.join(directory, filename)
                if mimetypes.guess_type(filepath)[0] == 'image/jpeg':
                    self.pics.append(filepath)
        print "{0} pictures found".format(len(self.pics))
                    
    def get_random(self):
    
        random_pic = random.choice(self.pics)
        return random_pic
