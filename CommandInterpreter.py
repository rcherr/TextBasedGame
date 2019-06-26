import random
from Scenario import Scenario
from GameObject import GameObject

class CommandInterpreter:
    
    #
    sc=None
    pl=None

    # All of our acceptable words
    sp_objects=["inventory","bag"]
    sp_targets=["left","right"]
    target=["the","at","on","around","my"]
    actions=["use", "exit", "look","open","take","turn"]
    action_alt={
        "utilize,operate":"use",
        "leave,go":"exit",
        "inspect,view,observe":"look",
        "grab,steal,borrow":"take",
        "check":"open",
        "rotate":"turn",
    }

    # Our escape characters for displaying terminal text
    bc_ylwbld="\033[1;33;20m"
    bc_whtnrm="\033[0;37;20m"
    bc_grnbld="\033[1;32;40m"
    bc_lblnrm="\033[1;34;20m"
    
    def __init__(self, pl, sc_path):
        self.sc=Scenario(sc_path)
        self.pl=pl

        # Automatically print the -1 scenario
        print(self.sc.get_scenario_update(pl))
        self.pl.direction=0

    def update(self, inp):
        
        if inp.lower()=="exit":
            return False
        # Update will first parse the users
        # text into chunks, then remove useless words,
        # and finally push whats left as actions.
        inp=self.__parse(inp)

        # Remove Junk will return one array of three arrays
        # The first containing all the actions
        # One containing targets["on","the","at"]
        # The other containing Objects for the target command
        inp=self.__remove_junk(inp)

        # Change the environment based on text input
        self.__interpret(inp)

        # Print scenario response to action
        #print(self.sc.get_scenario_update(0,self.pl.direction,0)) 
        
        # Continue the Game
        return True

    def get_challenge_text(self):
        return self.bc_grnbld+"What will you do? "+self.bc_whtnrm

    def __is_alternate(self, inp):
        return False if self.__get_alternative(inp)==None else True
    
    def __get_alternative_of(self, inp):
        
        # Go over the dictionary
        for key,val in self.action_alt.items():
            
            # Split it up
            chunks=key.split(",")
            
            # Go over the splits
            for x in chunks:
                if x==inp:
                    return self.action_alt.get(x)

    def __get_alternative(self,inp):

        for key,val in self.action_alt.items():
            
            #Split it Up
            chunks=key.split(",")
            
            # If the word entered exists as an alternative in
            # the dictionary then cool beans.
            if inp.lower() in chunks:
                return val

    def __interpret(self,inp):
        if len(inp[0])==0:
            a=random.randint(1,3)
            r=""
            if a==1:
                r="Think..."
            elif a==2:
                r="If only it were that easy..."
            elif a==3:
                r="You are wasting time..."
            print(r)
            return
        # Looking for certain commands
        try:
            
            # Attempt to find an alternative first
            cmd=self.__get_alternative(inp[0][0])
            
            # If there was no alternative for the word entered
            # use the original.
            if cmd==None:
                cmd=inp[0][0]

            # If the first index is a command
            # feed the rest of the list to the command
            if cmd in self.actions:
                getattr(self, cmd)(inp[1],inp[2])
            else:
                print("Command {} not found".format(inp[0][0]))
        except (AttributeError, IndexError) as ae:
            print("Failed to parse command {}".format(ae))
    
    def __parse(self,inp):
        
        # Return a Lowercased version of the input with no
        # new lines and split by spaces.
        return inp.lower().replace("\n","").split(" ")
    
    def __remove_junk(self,inp):

        #
        arr=[]

        # Keep objects in the scenario
        sc_list=[]

        # If the Scenario has objects
        # that the input contains, do not remove them.
        for c in self.sc.objects:
            if c.name.lower() in inp:
                sc_list.append(c.name.lower())

        for i in self.pl.inventory:
            if i.name.lower() in inp:
                sc_list.append(i.name.lower())

        # Remove all words in the array that aren't
        # recognized by the targets and actions.
        for x in inp:
            
            # Allow for alternate versions of commands.
            is_cmd=False if x not in self.actions and not self.__is_alternate(x) else True
            
            # If the current word is a target word
            # or action(command) or an item in the scenario
            # keep it.
            if x in self.target or is_cmd or x in sc_list:
                
                # Now check the scenario for items in view
                arr.append(x)               
        
        # Remove all entries from the scene list
        actions=[a for a in arr if a in self.actions or self.__is_alternate(a)] 
        targets=[t for t in arr if t not in sc_list and t not in actions]
        objects=[o for o in arr if o not in targets and o not in actions]
        
        # Add on Special Objects if we use the 'open' command
        if self.__get_alternative_of(inp[0])=="open" and ("inventory" in inp or "bag" in inp):
            objects.append("inventory")
        elif inp[0]=="turn" or self.__get_alternative_of(inp[0])=="turn":
            for t in inp:
                for p in self.sp_targets:
                    if t==p:
                        targets.append(p)
                        break

        # Return the original chunks with the useless words removed.
        return [actions,targets,objects]
    
    def open(self,tar,obj):
        
        if len(obj)>0:
        
            # Special case for the word inventory
            if obj[0]=="inventory" and ("the" in tar or "my" in tar or len(tar)==0):           
            
                # Grab the inventory
                p_objs=self.pl.inventory
            
                #
                f=None

                #
                print(self.bc_whtnrm+"You "
                        +self.bc_ylwbld+"Open"
                        +self.bc_whtnrm+" your bag and see:")

                # Grab all the items from the player's inventory
                for x in p_objs:
                    f=x
                    print("A "+self.bc_lblnrm+x.name+self.bc_whtnrm)

                if f==None:
                    print(self.bc_whtnrm+"Nothing but air."+self.bc_whtnrm)
            else:
            
                # Grab all the objects from the view
                v_objs=self.sc.get_objects_in_view(self.pl)
        else:
            print(self.bc_ylwbld+"Check"+self.bc_whtnrm+" what?")

    def turn(self,tar,obj):

        # Current player context

        # Turn only processes the first target
        if len(obj)==0:
            if tar[0]=="left":
                self.pl.direction=3 if self.pl.direction==0 else self.pl.direction-1
                print(self.sc.get_scenario_update(self.pl))
            elif tar[0]=="right":
                self.pl.direction=0 if self.pl.direction==3 else self.pl.direction+1
                print(self.sc.get_scenario_update(self.pl))
            elif tar[0]=="around":
                self.pl.direction=(self.pl.direction+2)%4
                print(self.sc.get_scenario_update(self.pl))

    def take(self,tar,obj):
        
        # Eventually add context objects based on last successful command
        if len(obj)==0:
            print(self.bc_ylwbld+"Take"+self.bc_whtnrm+" what?")
            return
        # Don't allow grabbing more than one item at a time.
        elif len(obj) > 1:
            print("You need more hands to grab all that at once.")
            return

        # Now Grab all those objects in our current view
        v_objs=self.sc.get_objects_in_view(self.pl)
        
        # Mull over the objects in the view
        for x in v_objs:
            
            # The item is in the state to be grabbed. (Implement Strength Values if RPG)
            if x.status==0 and x.name.lower()==obj[0]:
                
                # Add the item to the player's inventory
                self.pl.add_item(x)

                # Play the Objects take text.
                print(str(self.bc_whtnrm+x.take
                        +self.bc_whtnrm).format(self.bc_ylwbld+x.name
                        +self.bc_whtnrm))
                self.sc.remove_object_from_view(self.pl,x)
                break

    def look(self,tar,obj):

        #
        v_objs=self.sc.get_objects_in_view(self.pl)
        
        # No target objects and no targeting words.
        if len(obj)==0 and len(tar)>=1:
            
            # Around is a special case.
            if tar[0]=="around":
                
                #
                if len(v_objs)>0:
                
                    #
                    print(self.bc_whtnrm +"You "
                            +self.bc_ylwbld+"look"
                            +self.bc_whtnrm+" around and see:"
                            +self.bc_whtnrm)
                
                    #
                    for v in v_objs:
                        print(self.bc_lblnrm+v.name+self.bc_whtnrm+" - '"+v.desc+"'")
                else:
                    print(self.bc_whtnrm+"There is nothing to see here."+self.bc_whtnrm)
            else:
                print(self.bc_ylwbld+"Look"+self.bc_whtnrm+" at what?"+self.bc_whtnrm)
        elif len(obj)==1 and len(tar)>1:
            found=False
            for v in v_objs:
                if v.name.lower()==obj[0]:
                    found=True
                    print(self.bc_lblnrm+v.desc+self.bc_whtnrm)
                    break
            if found==False:
                print("There is no "+self.bc_ylwbld+obj[0]+self.bc_whtnrm+" nearby.")
    def use(self,tar,obj):
        
        # Use only accepts two values
        # The object that is being used
        # and the object it is being used on
        if len(obj)==0:
            print(self.bc_ylwbld+"Use"+self.bc_whtnrm+" what?")
            return

        if len(self.pl.inventory)==0:
            print(self.bc_whtnrm+"You have nothing to "+self.bc_ylwbld+"Use"+self.bc_whtnrm)

        for o in self.pl.inventory:

            # Cool Beans, the player has the item
            if obj[0]==o.name.lower():

                # Grab all the items in view
                v_objs=self.sc.get_objects_in_view(self.pl)
                
                # Two objects to act on
                if len(obj)==2:
                    
                    #
                    for v in v_objs:

                        # The Scenario has the item we want to act on in view.
                        if v.name.lower()==obj[1].lower():

                            # Boom, interact with each other.
                            o.interact(v)
                else:
                    print(str(
                            self.bc_ylwbld+"Use"+self.bc_whtnrm+" the "
                            +self.bc_lblnrm+o.name+self.bc_whtnrm+" on what?"))
