import re
import os

#3. The Music Library Application Assignment
#By: Jack Fitzpatrick | 20090266

patternName = r'^[^*\n]{2,40}$' #regex expression for our script, decided on 40 characters since some song titles are fairly long, as well as very loose restrictions for odd names!
patternGroup = r'^[^*\n]{2,25}$' #regex for our group
patternGenre = r'^[a-zA-Z ]{3,20}$' #regex for genre (spaces)
patternPlaylist = r'^[a-zA-Z0-9 ]{3,20}$' #regex for playlists (spaces)
patternLib = r'^[a-zA-Z0-9]{3,20}$' #regex for libraries (no spaces)
patternYear = r'^[0-9]{4}$' #assuming most of the music inserted is either from the 20th or 21st century (maybe some from earlier like classical, which will fit the bill too!)
patternSel = r'^[0-9]{1,2}$' #our menu selection regex, itll be a 1-2 character long number!

#our song class (This is an OOP assignment)
class Song():
    #we could validate each and every setter and constructor for sanity purposes, but I'm just going to sanitise input! 
    #It would also be wise to mark these variables with the __doubleUnderscores__ to mark them as """private""", I just forgot to!
    def __init__(self, tName, tGroup, tYear, tGenre, tPlaylist):
        self.tuneName = tName
        self.tuneGroup = tGroup
        self.tuneYear = tYear
        self.tuneGenre = tGenre
        self.tunePlaylist = tPlaylist

    #getters for the song
    def getName(self):
        return self.tuneName
    def getGroup(self):
        return self.tuneGroup
    def getYear(self):
        return self.tuneYear
    def getGenre(self):
        return self.tuneGenre
    def getPlaylist(self):
        return self.tunePlaylist

    #setters for the song
    def setName(self, tName):
        self.tuneName = tName
    def setGroup(self, tGroup):
        self.tuneGroup = tGroup
    def setYear(self, tYear):
        self.tuneYear = tYear
    def setGenre(self, tGenre):
        self.tuneGenre = tGenre
    def setPlaylist(self, tPlaylist):
        self.tunePlaylist = tPlaylist

    #return a nice string
    def toString(self):
        return self.tuneName + " | " + self.tuneGroup + " | " + self.tuneYear
    
    #returns a string for writing
    def toStringWrite(self):
        return self.tuneName + "," + self.tuneGroup + "," + self.tuneYear + "," + self.tuneGenre + "," + self.tunePlaylist

#this class stores a list of songs
class Playlist():
    def __init__(self, sList, pName):
        self.songList = sList
        self.playlistName = pName

    #functions for the playlist
    def addSong(self, song):
        self.songList.append(song) #add a song to the playlist
    def removeSong(self, song):
        self.songList.remove(song) #remove a song from the playlist

    #getters
    def getPlaylistName(self):
        return self.playlistName
    def getSongList(self):
        return self.songList
    
    #setters
    def setSongList(self, sList):
        self.songList = sList
    def setPlaylistName(self, pName):
        self.playlistName = pName

    #rename the playlist and change any songs contained playlists to the new one!
    def rename(self, newName):
        self.playlistName = str(newName)
        for song in self.songList:
            song.setPlaylist(str(newName))

    def toString(self):
        returnStr = self.playlistName + " has " + str(len(self.songList)) + " songs:"
        return returnStr


#this is the library class (gives option for multiple users to have their own libraries!)
class MyMusicLibrary():
    def __init__(self, oName, pList, sList):
        self.ownerName = oName
        self.playlistList = pList
        self.songList = sList
    
    #functions for the library 
    def searchLibrary(self, songName):
        for i in self.songList:
            if i.getName() == songName:
                return True

    #functions for the playlist
    def addPlaylist(self, playlist):
        self.playlistList.append(playlist) #add a song to the playlist
    def removePlaylist(self, playlist):
        self.playlistList.remove(playlist) #remove a song from the playlist
    
    #getters
    def getOwnerName(self):
        return self.ownerName
    def getPlaylistList(self):
        return self.playlistList
    def getSongList(self):
        return self.songList

    #setters
    def setOwnerName(self, oName):
        self.ownerName = oName
    def setPlaylistList(self, pList):
        self.playlistList = pList
    def setSongList(self, sList):
        self.songList = sList

    #generate song list from the songs.txt folder found in a library!
    def generateSongList(self):
        with open(self.ownerName + "/songs.txt", 'r') as f:
            for line in f:
                if line.rstrip(): #remove any blank lines or whitespace lines
                    line = line.rstrip() #remove the new line char from the line
                    sName,sGroup,sYear,sGenre,sPlaylist = line.split(',') #could also do this with array indexes song[0], song[1], etc..
                    song=Song(sName,sGroup,sYear,sGenre,sPlaylist)
                    self.songList.append(song)

    #basic method for generating a playlist from our list of songs!
    def generatePlaylists(self):
        #remove old playlists
        self.playlistList = []
        #get all the playlist names
        playlists = set() #make a blank set
        for song in self.songList:
            if not song.getPlaylist().upper() == "NONE": #if we dont have a song tagged with no playlist (any variation of the word "none" is no playlist)
                playlists.add(str(song.getPlaylist())) #add to the playlists set, if it exists already it wont be added!

        #generate the playlists
        for name in playlists:
            self.addPlaylist(Playlist([], name))

        for song in self.songList:
            for list in self.playlistList:
                if str(song.getPlaylist()) == str(list.getPlaylistName()) and str(song.getPlaylist).upper() != "NONE":
                    list.addSong(song)
    
    def listPlaylists(self):
        for list in self.playlistList:
            print(list.toString())
    
    def listSongs(self):
        for song in self.songList:
            print(song.toString())
    
    def listWholeLibrary(self):
        returnStr = ""
        noPlaylistCount=0 #counter for the songs with no playlist
        #print the playlists and their songs
        for list in self.playlistList:
            returnStr=returnStr + "\n" + list.toString()+"\n"
            for song in list.getSongList():
                returnStr=returnStr+"\t"+song.toString()+"\n" #we tab indent the songs
        #count the number of songs with no playlist
        for song in self.songList:
            if song.getPlaylist().upper() == "NONE":
                noPlaylistCount+=1
        returnStr=returnStr+"\n" + str(noPlaylistCount) + " Song(s) have no Playlist:\n" #print our line
       #now print all songs with no playlist
        for song in self.songList:
            if song.getPlaylist().upper() == "NONE":
                returnStr=returnStr+"\t"+song.toString()+"\n"
        return returnStr #return the string of our whole library!

    #method for loading from file inside library directory
    def loadFromFile(self):
        self.generateSongList()
        self.generatePlaylists() #generate the playlists
        self.listPlaylists()

    def addSong(self, song):
        self.songList.append(song)
        self.generatePlaylists() #regenerate our playlists
    
    def removeSong(self, song):
        self.songList.remove(song)
        self.generatePlaylists() #regenerate playlists
    
    def removePlaylist(self, playlist):
        #set any songs in the playlist to have no playlist!
        for song in playlist.getSongList():
            song.setPlaylist("None")
        self.playlistList.remove(playlist)
        self.generatePlaylists() #regenerate playlists
    
    def renamePlaylist(self, playlist, name):
        playlist.rename(name) #just calls the playlists own rename method, which will change the song playlists too!
        self.generatePlaylists()

    def saveChanges(self):
        with open(self.ownerName + "/songs.txt", 'w') as f:
            for song in self.songList:
                f.write(song.toStringWrite()+"\n")

    def toString(self):
        return self.ownerName +  "'s Library: " + str(len(self.songList)) + " songs, " + str(len(self.playlistList)) + " playlists."

#the following 2 methods are the 2 menus for picking or creating a library and then modifying, adding and deleing from the  
def menu():
    selection = -1
    print("\nWelcome to the Music Application!")
    while selection < 0 or selection > 3:
        print("1. Create a Library")
        print("2. Select a Library")
        print("0. Exit")

        selection = input("> ")
        #check our inputs before proceeding
        while not re.match(patternSel, str(selection)):
            if not re.match(patternSel, str(selection)):
                print("Invalid Input, Try Again!")
            selection = input("> ")

        selection = int(selection)

        if selection == 0:
            quit()
        elif selection == 1:
            createLibrary()
        elif selection == 2:
            #this try except catches any errors with the second menu but is mainly for if a user inputs an invalid library name!
            #try:
                libraryMenu(selectLibrary()) #make the user select a library and enter the menu
            #except:
                #selection = -1 #reset selection to allow user to try again!
                #print("Error, Please try Again!\n")
        else:
            print("Invalid Selection: " + str(selection))

def libraryMenu(library):
    exited = False
    #we don't need to check the selection number here because it will loop until we leave this menu!
    while not exited:
        selection = -1
        print("\nCurrent Library: " + library.getOwnerName())
        print("--------------------")
        print("1. Add song to Library")
        print("2. Remove song from Library")
        print("3. Modify a songs Details")
        print("4. List all songs in Library")
        print("--------------------")
        print("5. Remove Playlist")
        print("6. Rename Playlist")
        print("7. List Playlists")
        print("--------------------")
        print("8. Rename Library")
        print("9. Delete Library")
        print("10. Show Library Details")
        print("11. Show Whole Library")
        print("--------------------")
        print("12. Save Changes to Library")
        print("--------------------")
        print("0. Exit to Main Menu")
        
        selection = input("> ")
        #check our inputs before proceeding
        while not re.match(patternSel, str(selection)):
            if not re.match(patternSel, str(selection)):
                print("Invalid Input, Try Again!")
            selection = input("> ") #let user retry!
        
        selection=int(selection)

        if selection == 0:
            exited = True #exit this menu
        elif selection == 1:
            addSongs(library)
        elif selection == 2:
            removeSong(library)
        elif selection == 3:
            modifySong(library)
        elif selection == 4:
            library.listSongs()
        elif selection == 5:
            removePlaylist(library)
        elif selection == 6:
            renamePlaylist(library)
        elif selection == 7:
            library.listPlaylists()
        elif selection == 8:
            renameLibrary(library)
        elif selection == 9:
            removeLibrary(library)
            exited=True #we want to exit this menu now since we removed the library!
        elif selection == 10:
            print(library.toString())
        elif selection == 11:
            print(library.listWholeLibrary())
        elif selection == 12:
            library.saveChanges()
            print("Changes to Library Saved!")
        else:
            print("Invalid Selection: " + str(selection))
    menu() #return to the main menu

#list out the files in the directory with the script, this will show you the created libraries! 
def listLibraries(): 
    path = os.listdir()
    for file in path:
        if os.path.isdir(file):
            print(file)

def createLibrary(): #this creates an initialises the library for our user!
    valid = True
    lName = ""

    while not re.match(patternLib, lName):
        lName = input("Enter the name of the library: ")
        if not re.match(patternLib, lName):
            print("Invalid Library Name: " + lName + ", Try Again!")
            valid = False #just in case it jumps out for some reason!
        else:
            valid = True

    path=os.listdir()
    for file in path:
        if os.path.isdir(file) and str(file).upper() == lName.upper():
            valid = False
    
    if valid:
        #create the library and the directory for it!
        os.mkdir(lName) #create the library directory!
        f = open(lName + "\songs.txt", "x") #create the songs.txt file
        print("Created new Library: ", lName)
    else:
        print("Error: This library already exists! Try a different name!")

def selectLibrary():
    found = False
    print("Current Libraries: ")
    listLibraries()
    print("\n")
    lName = input("Enter a library name to use (Case Sensitive): ")
    path = os.listdir()
    for file in path:
        if os.path.isdir(file):
            if str(file) == str(lName):
                print("File found!")
                found = True
                currentLib=MyMusicLibrary(str(file), [], [])
                currentLib.loadFromFile()
                print(currentLib.toString())
                return currentLib
    if not found:
        input(lName + " not found. Enter to return to menu.")

def addSongs(library):
    #initialise the variables for the regex checks
    tName = ""
    tGroup = ""
    tYear = ""
    tGenre = ""
    tPlaylist = ""

    #check our inputs with regex to make sure theyre what we want going in!
    while not re.match(patternName, tName):
        tName = input("Enter a track name: ")
    while not re.match(patternGroup, tGroup):
        tGroup = input("Enter a track group: ")
    while not re.match(patternYear, tYear):
        tYear = input("Enter a track year: ")
    while not re.match(patternGenre, tGenre):
        tGenre = input("Enter a track genre: ")
    while not re.match(patternPlaylist, tPlaylist):
        tPlaylist = input("Enter a playlist ['None' for no playlist]: ")

    #create the song once we have our values!
    newSong = Song(tName, tGroup, tYear, tGenre, tPlaylist)
    
    print(newSong.toString())
    library.addSong(newSong) #add our song to our library!

#simple remove methods for the songs and playlists from our library!
def removeSong(library):
    library.listSongs()
    tName = input("Enter the name of a song to remove (Case Sensitive): ")

    for song in library.getSongList():
        if song.getName() == tName:
            library.removeSong(song)
            print("Removed Song: " + tName)

def modifySong(library):
    library.listSongs()
    name = input("Enter the name of a song you want to modify (Case Sensitive): ")

    for song in library.getSongList():
        if song.getName() == name:
            #default values that won't trigger the blank detection
            tName="a"
            tGroup="a"
            tYear="a"
            tGenre="a"
            tPlaylist="a"

            #if the input is either valid or blank, we allow it!
            print("Press enter on blank to keep the same value (shown in brackets)")
            while (not re.match(patternName, tName)) and not (len(tName) == 0): #NAND here, since we only want one or the other, and never both!
                tName = input("Track Name (" + song.getName() + "): ")
            while (not re.match(patternGroup, tGroup)) and not (len(tGroup) == 0):
                tGroup = input("Track group (" + song.getGroup() + "): ")
            while (not re.match(patternYear, tYear)) and not (len(tYear) == 0):
                tYear = input("Track year (" + song.getYear() + "): ")
            while (not re.match(patternGenre, tGenre)) and not (len(tGenre) == 0):
                tGenre = input("Track Genre (" + song.getGenre() + "): ")
            while (not re.match(patternPlaylist, tPlaylist)) and not (len(tPlaylist) == 0):
                tPlaylist = input("Track Playlist (" + song.getPlaylist() + "): ")

            #reset defaults if we have blank input
            if len(tName) == 0:
                tName = song.getName()
            if len(tGroup) == 0:
                tGroup = song.getGroup()
            if len(tYear) == 0:
                tYear = song.getYear()
            if len(tGenre) == 0:
                tGenre = song.getGenre()
            if len(tPlaylist) == 0:
                tPlaylist = song.getPlaylist()
        
            #change the variables now
            song.setName(tName)
            song.setGroup(tGroup)
            song.setYear(tYear)
            song.setGenre(tGenre)
            song.setPlaylist(tPlaylist)
            
            #regenerate playlists
            library.generatePlaylists()

def removePlaylist(library):
    library.listPlaylists()
    pName = input("Enter the name of a playlist to remove (Case Sensitive): ")

    for playlist in library.getPlaylistList():
        if playlist.getPlaylistName() == pName:
            library.removePlaylist(playlist)
            print("Removed Playlist: " + pName)

#rename our playlist
def renamePlaylist(library):
    library.listPlaylists()
    pName = input("Enter the name of a playlist to rename (Case Sensitive): ")
    newName = ""

    for playlist in library.getPlaylistList():
        if playlist.getPlaylistName() == pName:
            #check with regex
            while not re.match(patternPlaylist, newName):
                newName = input("Enter a new name: ")
                if not re.match(patternPlaylist, newName):
                    print("Invalid Name: " + newName + ", please try again!")
            library.renamePlaylist(playlist, newName)
            print("Renamed Playlist: " + pName)

#rename our library to what we want!
def renameLibrary(library):
    #we can change its name referenced in the code:
    originalName = library.getOwnerName() #have to ref this before we change name
    newName = ""
    while not re.match(patternLib, newName):
        newName = input("Enter a new name: ")
        if not re.match(patternLib, newName):
            print("Invalid Name: " + newName + ", please try again!")
    library.setOwnerName(newName)  
    
    #now we need to change the files too to match it (the library name is grabbed from the file name on start)
    os.rename(originalName, newName)

#all we have to do is remove the file, since the library is linked to it!
def removeLibrary(library):
    os.remove(library.getOwnerName()+"\songs.txt") #remove the file first!
    os.rmdir(library.getOwnerName())
    
def main():
    menu()

if __name__ == "__main__":
    main()
