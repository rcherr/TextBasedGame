import time, os
from datetime import date
from Scenario import Scenario
from GameObject import GameObject
from Player import Player
from CommandInterpreter import CommandInterpreter

class Game:

    # Globals
    ci=None
    file_progress="progress.txt"
    file_progress_stream=None

    # Scenario status codes
    room=0
    status=0

    # Our text codes
    def __init__(self,ci):
        self.ci=ci
        self.file_progress_stream=open(self.file_progress,"w")    
    
    # Return the time the command was called
    def get_time(self):
        return date.fromtimestamp(time.time()).isoformat()

    def create_file(self,path):
        # Append to a progress file or create if it doesn't exist
        try:
            if os.path.isfile(path):
                return open(path, "a")
            else:
                return open(path, "w+")
        except IOError:
            print("Something went wrong with the file.")

# Our initial shovel
shv=GameObject("objects/shovel.tobj")
shv.set_initial_status(-1,-1,1)
# Setting the Game up
# Create a new Player
player=Player(-1)
player.add_item(shv)
ci=CommandInterpreter(player,"scenarios/barn.txt")

# Create our Game and supply it with the location of the starting scenario
game=Game(ci)

# Keep going until the 'exit' command is sent
on=True
while on:
    # on is set to false when 'exit' is entered by the user
    on=ci.update(input(ci.get_challenge_text()))
