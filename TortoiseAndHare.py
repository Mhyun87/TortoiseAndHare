"""
Tortoise vs. Hare - The Big Race
demonstrate some thread functionality
"""

# set this flag True to turn on debug output
debug = False

import random, time
from threading import Thread

"""
race info is stored in the Race class which extends the Thread class
"""
class Race (Thread):
    def __init__(self, name):
        """
        Race object constructor
        """
        if (debug):
            print ("Race:__init__() called")

        # initialize the base Thread class
        Thread.__init__(self, name = name)
        print("")
        print( name )
        
        # store the race contestants in a list
        # each list entry is a Contestant object, which is a subclass of Thread
        # in gaming, each character that moves around is typically implemented as a Thread
        self.raceContestants = []

        # this race is 30 "steps" long
        self.raceLength = 30

        # at the end of the race, this will be either "Tortoise", "Hare", or "Tie"
        self.raceWinner = ""

        # the Race Thread wakes up and checks the race status every second
        self.sleepInterval = 1000 # in msec
            
    def drawRace(self):
        """
        this function shows the race status (i.e., the position of the Tortoise and Hare)
        """
        # each contestant has a letter and a position
        letter   = []
        position = []
        for contestant in self.raceContestants:
            if (debug):
                print("Race:drawRace() ", contestant.name, " position ", contestant.position )            
            letter.append( contestant.letter )
            position.append( contestant.position )
            
        nmax = self.raceLength
        for n in range(0,nmax):
            if (n==position[0] and n!=position[1]):
                # contestant 0 is in this position
                c = letter[0]
            elif (n!=position[0] and n==position[1]):
                # contestant 1 is in this position
                c = letter[1]
            elif (n==position[0] and n==position[1]):
                # both contestants are in this position
                c = "*"
            else:
                # neither contestant is in this position
                c = "-"
            print(c,end="")
        print()
        return
        
    def run(self):
        """
        this method is called when the Race Thread is started
        the Thread dies when we return from this method
        """
        if (debug):
            print ("Race:run() called")
            
        # announce the contestants
        print("The contestants are:")
        for contestant in self.raceContestants:
            print("   %s" % contestant.name)
            
        # start the race
        print("")
        print("BANG !!!!")
        print("And They're Off !!!!")
        print("")
        
        # use this global variable to stop the Contestant Threads at the end of the race
        global stop_threads
        stop_threads = False
        
        # start the Contestant Threads
        for contestant in self.raceContestants:
            # start() will invoke the Contestant Thread run() method
            contestant.start()
            
        # check periodically for winner
        # stay in this loop until we have a winner
        while (self.raceWinner == ""):
            # draw the race status
            self.drawRace()
            
            # we check the position of all contestants because there may be a tie 
            for contestant in self.raceContestants:
                if (debug):
                    name = contestant.name
                    position = contestant.position
                    print (name, " position ", position )
                    
                if (contestant.position >= self.raceLength):
                    # this contestant has reached the finish line
                    if (self.raceWinner == ""):
                        # so far, this is the winner
                        # if the other contestant also reached the finish line,
                        #   it will be a tie
                        self.raceWinner = contestant.name
                    else:
                        # both contestants have reached the finish line
                        self.raceWinner = "Tie"
                        
            # the race ends when we have a winner
            if (self.raceWinner != ""):
                # we have a winner!!!
                # announce the winner
                if (self.raceWinner == "Tie"):
                    print("The race is a tie")
                else:
                    print ("The winner is %s" % self.raceWinner)
                    
                # use the stop_threads global variable to stop the Contestant Threads
                # TODO: add your code here
                break;

            # sleep for a while, then check the race status again
            sec = self.sleepInterval / 1000
            time.sleep( sec )

        # hold window open to allow user to view output
        print("")
        input("Press ENTER to continue ")
        # when we return from the run() method, the Thread dies

"""
the Contestant class extends the Thread class
"""
class Contestant (Thread):
    def __init__(self, name, raceLength):
        """
        Contestant object constructor
        """
        if (debug):
            print ("Contestant:__init__() called")
            
        # initialize the base Thread class
        Thread.__init__(self, name = name)

        # this is the race length        
        self.raceLength = raceLength

        # we start at the beginning
        self.position = 0
        
        # a Contestant Thread wakes up and moves every second
        self.sleepInterval = 1000 # in msec

        # each Contestant subclass will fill in the contestant letter
        self.letter = " "
        
    def run(self):
        """
        this method is called when a Contestant Thread is started
        the Thread dies when we return from this method
        """
        if (debug):
            print ("Contestant:run() called")
            
        # the Race Thread uses this global value to stop the Contestant Threads when we have a winner
        global stop_threads
        
        # when we break out of this loop, we return from the run() method and the thread dies
        while (self.position < self.raceLength):
            # someone has won, stop moving
            if (stop_threads):
                break
            
            # sleep for a while, then move
            sec = self.sleepInterval / 1000
            time.sleep( sec )
            
            self.move()
            
    # subclasses override the move() method
    def move(self):
        if (debug):
            print ("Contestant:move() called", self.name, " position ", self.position)
            
        delta = 1
        self.position += delta;
        

"""
the TortoiseContestant class extends the Contestant class
"""
class TortoiseContestant (Contestant):
    def __init__(self, name, raceLength):
        if (debug):
            print ("TortoiseContestant:__init__() called")
            
        # initialize the base class
        Contestant.__init__(self, name, raceLength)
        
        # use this letter for the tortoise contestant
        self.letter = "T"
            
    # this is how the tortoise moves
    def move(self):
        if (debug):
            print ("TortoiseContestant:move() called", self.name, " position ", self.position)
            
        random_number = random.randint(1,100)
        if (random_number < 20): # hare sleeping 20% of time
            delta = 0
        elif (random_number < 40): # big hop 20% of time
            delta = 9
        elif (random_number < 50): # big slip 10% of time
            delta = -12
        elif (random_number < 80): # small hop 30% of time
            delta = 1
        else: # small slip 20% of time
            delta = -2
        self.position += delta
        
        if (self.position < 0):
            self.position = 0
        if (self.position > self.raceLength):
            self.position = self.raceLength

"""
the HareContestant class extends the Contestant class
"""
class HareContestant (Contestant):
    def __init__(self, name, raceLength):
        if (debug):
            print ("HareContestant:__init__() called")
            
        # initialize the base class
        Contestant.__init__(self, name, raceLength)
        
        # use this letter for the hare contestant
        self.letter = "H"
            
    # this is how the hare moves
    def move(self):
        if (debug):
            print ("HareContestant:move() called", self.name, " position ", self.position)
            
        random_number = random.randint(1,100)
        if (random_number < 20): # hare sleeping 20% of time
            delta = 0
        elif (random_number < 40): # big hop 20% of time
            delta = 9
        elif (random_number < 50): # big slip 10% of time
            delta = -12
        elif (random_number < 80): # small hop 30% of time
            delta = 1
        else: # small slip 20% of time
            delta = -2
        self.position += delta
        
        if (self.position < 0):
            self.position = 0
        if (self.position > self.raceLength):
            self.position = self.raceLength

"""
the tortoise and hare main program
"""
def main():

    # race info is in this Race object
    name = "Tortoise vs. Hare - The Big Race"
    race = Race( name )

    # initialize the list of race contestants
    name = "Tommy the Tortoise"
    contestant = TortoiseContestant( name, race.raceLength )
    race.raceContestants.append( contestant )

    name = "Harry the Hare"
    contestant = HareContestant( name, race.raceLength )
    race.raceContestants.append( contestant )

    # introduce the contestants and start the race
    race.start()

# call main() to start program execution
if __name__ == "__main__":
    main()

