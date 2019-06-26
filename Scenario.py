import os
from GameObject import GameObject

class Scenario:

    # Class Variables
    path=""
    objects=[]
    desc_path=""
    status={}
    desc=[]

    #
    def __init__(self,path):
        self.path=path
        self.__read_scenario(path)

    # Read in the scenario
    def __read_scenario(self,path):

        # Open the file for reading
        f=open(path, "r")

        # Line by line
        for line in f:
            self.__process_sc_line(line)
        
        # Close the file
        f.close()
    
    def __read_desc(self,path):

        # Open the file for reading
        f=open(path,"r")

        for line in f:
            self.__process_desc_line(line)


        f.close()

    # Process each line in the file
    def __process_sc_line(self,text):
        
        # Store the description
        self.desc.append(text)

        # Arrangement (name:index:location:objectnum:objects;
        text=text.replace("\n","")
        info=text.split(":")

        # Find the object and description files        
        g=self.__find_desc_by_fname(info[2])
        
        # Read the Description
        self.__read_desc(os.path.join("scenarios",g))
        
    def __process_desc_line(self,text):

        # Arrangement (room:direction:status:desc:objects)
        text=text.replace("\n","")
        info=text.split(":")
        
        #
        b=info[0]+":"+info[1]+":"+info[2]
       
        #if not info[4]=="null.tobj":
            
        # Find the object
        f=self.__find_object_by_fname(info[4])
        
        go=GameObject(os.path.join("objects",f))
        go.set_initial_status(int(info[0]),int(info[1]),int(info[2]))

        # Create the object
        self.objects.append(go)

        # Append to the room:direction:status
        self.status.update({b:info[3]})
    
    #
    def __find_object_by_fname(self,text):
        
        # Start in the current working directory
        files=os.listdir("objects")
        
        # Go over all the files
        for x in files:
            if x.replace(" ", "")==text:
                return x
    
    def __find_desc_by_fname(self,text):

        #
        files=os.listdir("scenarios")

        #
        for x in files:
            if x.replace(" ","")==text:
                return x

    def get_objects_in_view(self,pl):
        
        # Player context
        r=pl.room
        d=pl.direction
        s=pl.status

        #
        outp=[]

        #
        for o in self.objects:
            if o.room==r and o.direction==d and o.status==0:
                outp.append(o)

        return outp

    def get_scenario_update(self,pl):
        
        # Find the description that matches
        key=str(str(pl.room)
                +":"+str(pl.direction)
                +":"+str(pl.status))
        
        # The key must exist
        if key in self.status:
            return self.status[key]

    def remove_object_from_view(self,pl,obj):
        
        #
        r=pl.room
        d=pl.direction
        s=pl.status

        # Find the objects
        v_objs=self.get_objects_in_view(pl)
        
        f=None

        # Roll over em all
        for x in v_objs:
            if x==obj:
                f=x

        # Remove it
        if not f==None:
            self.objects.remove(f)
