from random import *

#1. The lottery python assignment 
#By: Jack Fitzpatrick | 20090266

#the min and max values of our lotto (numbers between 1 and 45 inclusive)
minVal = 1
maxVal = 45

def main():
    #initialise our 3 lotto lists and the user list
    lotto=[]
    lottoPlus1=[]
    lottoPlus2=[]
    userNumbers=[]
    
    userInput(userNumbers) #take user input, let them pick their numbers or do a quick pick
    doLotto(userNumbers,lotto,lottoPlus1, lottoPlus2) #run the lottery and ask the user if they want to do lotto+

def userInput(ulist):
    val=-1 #default value for the val variable

    while val < 0 or val > 2: #let user pick an option from the menu!
        print("Welcome to the lottery program! Please select an option below:")
        print("1 : Quick Pick Numbers")
        print("2 : Pick your Own Numbers")
        print("0 : Exit")
        try:
            val = int(input("> "))
            if val == 1:
                randomiseValues(ulist) #randomose the user value
            elif val == 2:
                userNumberChoice(ulist) #let the user choose
            elif val == 0:
                quit()
            else:
                print("Invalid Value:", val)
        except: #again sanitise our input make sure to notify the user if an invalid string/value is entered!
            print("Please enter a NUMBER!")

def userNumberChoice(l):
    while len(l) < 6: #until we get 6 values in the list!
        try: #validate our input!
            number = int(input("Please Enter a Number [1-45]: "))
            if number > 0 and number <= 45 and not checkDupes(l, number):
                l.append(number) #append the value
                print("Current Numbers:", l) #print the numbers the user has picked back!
            else:
                print("Invalid Value:", number) #tell our user the number is invalid
        except:
            print("Please enter a NUMBER!")

def doLotto(u, l, lP1, lP2): #takes in all the lists!
    userIn = -1
    while userIn < 1 or userIn > 2: #ask the user if they want to do lotto plus
        print("Do you want to do the lotto plus? (+2 Lines)")
        print("1 : Yes")
        print("2 : No")
        try:
            userIn = int(input("> "))
            if userIn == 1:
                #randomise our values
                randomiseValues(l)
                randomiseValues(lP1)
                randomiseValues(lP2)

                #check each draw and return the results to the user!
                print("---Lotto Draw Results---\n")
                checkResults(u, l)
                print("---Lotto Plus 1 Draw Results---\n")
                checkResults(u, lP1)
                print("---Lotto Plus 2 Draw Results---\n")
                checkResults(u, lP2)
            else:
                randomiseValues(l)
                print("---Lotto Draw Results---\n")
                checkResults(u, l)
        except:
            print("Invalid selection! Try Again!")


#this prints our results to the user so they know what they got!
def checkResults(list1, list2):
    results = returnResult(list1, list2) #get the ,match results from our lists!

    #this isn't a great way to do it in terms of speed, but we only run this once at the end so its acceptable!
    print("You matched:", results[0], "numbers and", results[1], "bonus, Therefore:")
    if results[0] == 6: #6 matched
        print("YOU WON THE JACKPOT!!!")
    elif results[0] == 5: #5 matched
        print("You won a HUGE cash prize!")
    elif results[0] == 4: #4 matched
        print("You won a cash prize!")
    elif results[0] == 5 and results[1] == 1: #5 + bonus matched
        print("You won a large cash prize!")
    elif results[0] == 4 and results[1] == 1: #4 + bonsu matched
        print("You won a sizeable cash prize!")
    elif results[0] == 3 and results[1] == 1: #3 + bonus matched
        print("You won a small cash prize!")
    elif (results[0]+results[1]) == 3: #match any 3
        print("You won a scratchcard!")
    else:
        print("You didn't win anything on this draw... Better luck next time! :(\n")

#The classes below serve as utility!
def randomiseValues(list):
    while len(list) < 7: #if the list has less than 7
        rand = randrange(minVal,maxVal) #generate a random value
        if not (checkDupes(list, rand)): #if its not a dupe
            list.append(rand) #add it to the list!

def returnResult(uList, lotList): #this checks our list to see how many matches and bonus matches we got!
    #tell the user what they've gotten and what the lotto returned!
    print("Your Numbers:",bonusless(uList))
    print("Lottery Draw Numbers:",bonusless(lotList), "| Bonus Number:", bonus(lotList),"\n")

    bonuslessMatches = set(bonusless(uList)).intersection(set(bonusless(lotList)))
    bonusMatches = 0 #this will only be 0 or 1, but I ke   pt it as an integer for ease of use!
    if not (bonuslessMatches) == 6: #as long as we haven't exhaused the user list with matches we have the potential to match the bonus!
        for i in range(0, len(uList)):
            if uList[i] == bonus(lotList):
                bonusMatches = 1 #we matched a bonus! 

    return [len(bonuslessMatches),bonusMatches] #return a list

def checkDupes(list, value): #checks for duplicate values!
    dupe = False #default it to false before we begin
    for i in range(0, len(list)): #cycle the list
        if list[i] == value: #if we find a matching value
            dupe = True #set it true
    return dupe #return it

def bonusless(list): #return a list with no bonus number!
    bonuslessList=[]
    for i in range(0, 6):
        bonuslessList.append(list[i]) 
    return bonuslessList

def bonus(list): #just get our bonus!
    return list[6] #return the bonus number from a list!

if __name__ == "__main__":
    main()