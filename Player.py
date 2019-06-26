from GameObject import GameObject

class Player (GameObject):

    # The values that the player has
    inventory=[]
    direction=-1

    def __init__(self, d):
        self.direction=d

    def add_item(self,obj):
        if isinstance(obj, GameObject):
            if obj.status==0:
                self.inventory.append(obj)
