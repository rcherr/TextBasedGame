class GameObject:

    # Class variables
    name=""
    desc=""
    take=""
    # Every object has different status values that determine the 'state' of the object
    # 0 - Normal (not in use or inventory)
    # 1 - In Use (not in inventory)
    # 2 - In Inventory (not in use)
    # 3 - In use from inventory
    # 99 - Static Openable Object
    room=0
    status_desc=[]
    interact_desc=[]
    status=0
    direction=0

    #
    def __init__(self,path):

        # Process the file
        self.__process_file(path)
    
    def set_initial_status(self,r,d,s):
        self.room=r
        self.direction=d
        self.status=s

        #self.desc=self.status_desc[s]
    #
    def interact(self, dest):
        if isinstance(dest, GameObject):
            print(self.name+" interacted with "+dest.name)
        else:
            print("Failed.")
    
    #
    def __process_file(self, path):
        
        # Open the file
        f=open(path, "r")
        
        #
        for line in f:
            self.__process_lines(line)

        # Set default desc
        self.desc=self.status_desc[self.status]

        # Close the file
        f.close()
    
    #
    def __process_lines(self, text):
        
        # Solve for name
        if text.startswith("name"):
            self.name=text.split("=")[1].replace("\n","")

        # Solve for take
        if text.startswith("take"):
            self.take=text.split("=")[1].replace("\n","")

        # Solve for desc
        if text.startswith("state"):
            self.status_desc.append(text.split(":")[2].replace("\n",""))

        # Solve for interactions
        if text.startswith("interact"):
            pass
            # Append to dictionary of {item:string}
