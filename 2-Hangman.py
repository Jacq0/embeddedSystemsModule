from random import *

#2. The Hangman Assignment
#By: Jack Fitzpatrick | 20090266

wordList = ["COMPUTER", "PROGRAM", "ERROR", "SCRIPT", "LAB", "CODE"] #our list of words for the hangman game! 

def main():
    word = str(pickWord()) #initialise our word!
    numGuesses = len(word)-1 #the number of guesses the user has!
    lettersGuessed=[] #this stores at each index if the letter was lettersGuessed or not, 0 for no and 1 for yes!
    lettersUsed=[] #the letters we lettersUsed during the program, so the user cant use the same char twice!
    
    for i in word: #loop through and initialise the array!
        lettersGuessed.append(0) #0 if the letter isn't lettersGuessed, 1 if it is!

    print("Welcome to Hangman! Try guess the", len(word),"letter word: ",returnRevealed(word, lettersGuessed) + ", You have", numGuesses,"letter guesses !")

    #while we have letter guesses left!
    while numGuesses > 0:
        letter = input("Please Enter a Letter\n> ") #let the user input a letter

        if validInput(letter): #if we have a valid input letter
            if not checkLettersUsed(letter, lettersUsed): #if the letter isn't used
                lettersUsed.append(letter.upper()) #add the letter to the used list!
                if checkLetterInWord(letter, word, lettersGuessed): #if the letter is in the word
                    if checkWordFinished(lettersGuessed): #if the word is finished we congratulate the user
                        print("CONGRATULATIONS! The word was:",word.upper())
                        quit()
                    else:
                        print("This letter is in this word:",returnRevealed(word, lettersGuessed),"You have", numGuesses, "guesses left!")
                else:
                    numGuesses = numGuesses-1
                    print("This letter is NOT in this word:", returnRevealed(word, lettersGuessed) + ", you have", numGuesses, "guesses left!")
            else:
                print("This letter has already been used!")
        else:
            print("Invalid, please try again!")

    while numGuesses == 0: #when we are out of letter guesses
        wordGuess = input("You have ran out of letter guesses, Please try guess the word!\n> ")

        if wordGuess.upper() == word.upper(): #if we match the words
            print("Well done you got it, BANG ON!")
            quit()
        else:
            print("Incorrect")

        
def validInput(input): #make sure our user input is valid!
    if input.isalpha() and len(input) == 1: #if our input contains only alpha characters and is a single character long...
        return True
    else:
        return False

#this checks if we have already used the letter
def checkLettersUsed(letter, lettersUsed):
    used=False
    for ltr in lettersUsed:
        if ltr.upper() == letter.upper(): #if they match
            used = True #the letter has been used!
    return used

#returns a string with the letters of the word we haven't guessed blanked out!
def returnRevealed(word, lettersGuessed): #this method returns an obfuscated string based on the lettersGuessed indexes!
    revealed=""
    index = 0
    for char in word:
        if lettersGuessed[index] == 1:
            revealed+=str(char.upper()) #append the string uppercase to the value
        else:
            revealed+=str("_") #add an underscore for an unguessed letter
        index=index+1
    return revealed #return the string!

def checkLetterInWord(letter, word, lettersGuessed):
    index=0 #keep track of the index so we can see whats lettersGuessed
    inWord=False
    for char in word: #loop through the characters in the word!
        if char.upper() == letter.upper():
            lettersGuessed[index]=1
            inWord=True
        index=index+1 #increment the index!
    return inWord #return the status!

def checkWordFinished(lettersGuessed):
    complete = False
    count = len(lettersGuessed) #to keep track of the number we are expecting
    counter = 0 #the counter (incremented)
    for i in lettersGuessed:
        if i == 1:
            counter=counter+1 #incrememt the counter
    if count == counter:
        complete = True #if we complete the word, and all slots in the guesses are 1
    return complete

def pickWord():
    return wordList[randrange(0,len(wordList))] #pick a random word from the word list!

if __name__ == "__main__":
    main()