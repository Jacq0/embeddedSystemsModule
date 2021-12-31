#!/bin/bash

#The linux scripting tables assignment
#by Jack Fitzpatrick | 20090266

NUMBER=0 #the number for the arithmetic questions
CHOICE=-1 #the users choice for menus
ARITH_OP=0 #the arithmetic operator
NUM_QUESTIONS=0 #number of questions the user has (depends on age group)
LEVEL=0 #the level (1:teacher or 2:student)
INPUT=-1 #user input for answers
USR="" #username
PASS="" #password
FNAME="" #first name
AGE_GROUP="" #age group (1-3)
CURR_USER="" #current user
ELAPSED_TIME=0 #for our quiz to time the student!

declare -A STORE_RESULTS #this is the pseudo 2D array (actually an associative array) for storing the results (currently empty)

#could just use the alphanumeric or number regex experssions either!
USRRE='^[A-Za-z0-9]{3,20}$' #the user string can be between 3 and 20 characters long!
PWDRE='^[A-Za-z0-9]{5,30}$' #pass has a min length of 5 and a max of 30! Potential to make it require a capital and number!
FNMRE='^[A-Za-z]{2,25}$' #first name only contains alpha chars and has to be between 2 and 25 chars long!
NUMRE='^[0-9]$'

main()
{
	createLoginFile #will create a login file if it doesnt exist

	#reset choice
	CHOICE=-1
	clear

	#let the user choose to login or exit
	until [ $CHOICE -ge 0 -a $CHOICE -le 1 ]
	do
		echo -e "Welcome to the Tables Program! ^_^\n"
		echo "Please Select an option below: "
		echo "1 : Login"
		echo "0 : Exit Program"
		echo -n "> "
		read CHOICE
		case $CHOICE in
			0)
				echo -e "\nBye Bye! o7"
				;;
			1)
				makeChoice
				;;
			*)
				clear
				echo -e "Invalid Option: $CHOICE\n"
				;;
		esac
	done
	#done
}

createLoginFile() #if it doesn't exist we make it and a default user
{
	FILE="login.txt" #the name of the file

	if [ ! -f "$FILE" ] #if the file doesn't exist
	then
		touch "$FILE" #make the file
		echo -ne "administrator\tadmin\tpassword\t1\t0\n" >> "$FILE" #create a default admin user
	fi
}

makeChoice() #this function is for picking your options!
{
clear
login

#reset the CHOICE variable
CHOICE=-1

if [ $LEVEL -eq 1 ]
then
	while [ $LEVEL -eq 1 ]
	do
		CHOICE=-1 #reset choice
		until [ $CHOICE -ge 0 -a $CHOICE -le 3 ]
		do
			clear
			echo "Current User: $FNAME [$CURR_USER]"
			echo "1 : Review Student Results"
			echo "2 : Modify/Delete an Account"
			echo "3 : Add account to System"
			echo "0 : Logout"
			echo -n "> "
			read CHOICE
			case $CHOICE in
				0)
					echo "Bye Bye!"
					exec "$0" #restart the script!
					#resetDetails
					#main
					;;
				1)
					echo "Review student Results"
					readResults
					;;
				2)
					echo "Review student stats"
					modifyDeleteUser
					;;
				3)
					echo "Add account to System"
					createAccount
					;;
				*)
					echo "Invalid option: $CHOICE"
					;;
			esac
		done
	done
elif [ $LEVEL -eq 2 ]
then
	while [ $LEVEL -eq 2 ]
	do
		CHOICE=-1 #reset choice
		until [ $CHOICE -ge 0 -a $CHOICE -le 3 ]
		do
			clear
			echo "Current User: $FNAME [$CURR_USER]"
			echo "Please choose one of the options below:"
			echo "1 : Learn Tables"
			echo "2 : Take Quiz"
			echo "3 : Take Challenge"
			echo "0 : Logout"
			echo -n "> "
			read CHOICE

			case $CHOICE in #let the user choose from the list
				0)
					echo "Bye Bye!"
					exec "$0" #this just reruns our script
					#main
					;;
				1)
					echo "Learn Tables"
					learnTables
					;;
				2)
					echo "Take Quiz"
					takeQuiz
					;;
				3)
					echo "Take Challenge!"
					takeChallenge
					;;
				*)
					echo "Invalid Option"
					;;
			esac
		done
	done
else
	main
fi
}

learnTables() #our tables, which just lets the user go through and learn their tables!
{
	chooseNumber
	chooseArithOp
	clear

	CORRECT=0 #stores the n umber of correct answers

	case $ARITH_OP in
		1)
			for((i=1; i<=12; i++))
			do
				ANS=$((NUMBER+i))
				echo "$NUMBER + $i = ?"
				read INPUT
				if [ $INPUT -eq  $ANS ]
				then
					echo "Correct!"
					CORRECT=$((CORRECT+1))
				else
					echo "WRONG!"
				fi
			done
			;;
		2)
			for((i=1;i<=12;i++))
			do
				ANS=$((NUMBER-i))
				echo "$NUMBER - $i = ?"
				read INPUT
				if [ $INPUT -eq $ANS ]
				then
					echo "Correct!"
					CORRECT=$((CORRECT+1))
				else
					echo "WRONG!"
				fi
			done
			;;
		3)
			for((i=1;i<=12;i++))
			do
				ANS=$((NUMBER*i))
				echo "$NUMBER x $i = ?"
				read INPUT
				if [ $INPUT -eq $ANS ]
				then
					echo "Correct!"
					CORRECT=$((CORRECT+1))
				else
					echo "WRONG!"
				fi
			done
			;;
		4)
			for((i=1;i<=12;i++))
			do
				DIVNUM=$((NUMBER*i))
				ANS=$((DIVNUM/i))
				echo "$DIVNUM / $i = ?"
				read INPUT
				if [ $INPUT -eq $ANS ]
				then
					echo "Correct!"
					CORRECT=$((CORRECT+1))
				else
					echo "WRONG!"
				fi
			done
			;;
		*)
			;;
	esac

	echo "You got $CORRECT / 12 correct!"
}

chooseNumber() #pick the number for the times tables!
{
	clear
	until [ $NUMBER -gt 0 -a $NUMBER -le 12 ]
	do
		echo "Pick a number [ 1 - 12 ]"
		read NUMBER

		if [ $NUMBER -lt 1 -o $NUMBER -gt 12 ] 
		then
			clear
			echo "$NUMBER outside range!"
		fi
	done
}

chooseArithOp()
{
	clear
	until [ $ARITH_OP -gt 0 -a $ARITH_OP -le 4 ] #until we pick a valid arithmetic operator!
	do
		echo "Pick an operator:"
		echo "1) Addition [+]"
		echo "2) Subtraction [-]"
		echo "3) Multiplication [x]"
		echo "4) Division [/]"
		read ARITH_OP

		if [ $ARITH_OP -lt 1 -o $ARITH_OP -gt 4 ]
		then
			clear
			echo "$ARITH_OP is an invalid option, Try Again!"
		fi
	done
}

writeToFile()
{
	local FOLDER="results/" #this is to create the results folder, since its not created with the file

	if [ ! -d "$FOLDER" ]
	then
		mkdir $FOLDER
	fi

	#write to the results directory!
	local FILE=$FOLDER$USR"-"$(date "+%Y%m%d%H%M%S")"-"$((RANDOM%999+1))".txt" #date command to supply a specific date

	if [ ! -f "$FILE" ] #if the file doesn't exist
	then
		touch "$FILE" #make the file
	fi

	>$FILE #clear contents in case it exists
	echo "Writing to file: $FILE"

	#add the lables for each line to make it easier toread, we can remove it later
	echo -ne "O1\tAO\tO2\tANS\tUANS\tCRT\n" >> "$FILE"

	#write to file
	for((i=0;i<$NUM_QUESTIONS;i++)) #replace numquestiosn with 10
	do
		for((j=0;j<6;j++)) #replaced c with 6
		do
			echo -ne "${STORE_RESULTS[${i},${j}]}\t" >> "$FILE"
		done
		echo -ne "\n" >> "$FILE"
	done

	echo "Time taken: $ELAPSED_TIME ms" >> "$FILE" #write our elapsed time to the file too!
}

takeQuiz()
{
	ELAPSED_TIME=0 #reset our time! (not needed since its reset anyway at the bottom but nice to have!)
	local START=$(date +%s%N) #get our result in nanoseconds

	#change the number of questions based on our users level!
	case $AGE_GROUP in #get our number of questions based on the level!
		1)
			NUM_QUESTIONS=10
			echo "Low Level"
			;;
		2)
			NUM_QUESTIONS=15
			echo "Medium Level"
			;;
		3)
			NUM_QUESTIONS=20
			echo "High level"
			;;
	esac

	for ((i=0;i<$NUM_QUESTIONS;i++))
	do
		ARITH_OP=$((RANDOM%4+1)) #random number between 1 and 4, the +1 is starting at one
		OPERAND1=NUMBER
		OPERAND2=0
		ANS=0
		USR_ANS=0
		CORRECT=0

		#echo "Quiz Time!"

		case $ARITH_OP in
			1)	#echo "Addition"
				clear
				echo "Question $((i+1)):"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((RANDOM%12+1))
				ANS=$((OPERAND1+OPERAND2))
				echo "$OPERAND1 + $OPERAND2 = ?"
				;;
			2)	#echo "Subtraction"
				clear
				echo "Question $((i+1)):"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((OPERAND2+(RANDOM%12+1))) #the random number here has to be +12 on the number so we never get a negative value!
				ANS=$((OPERAND1-OPERAND2))
				echo "$OPERAND1 - $OPERAND2 = ?"
				;;
			3)	#echo "Multiplication"
				clear
				echo "Question $((i+1)):"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((RANDOM%12+1))
				ANS=$((OPERAND1*OPERAND2))
				echo "$OPERAND1 * $OPERAND2 = ?"
				;;
			4) 	#echo "Division"
				clear
				echo "Question $((i+1)):"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((OPERAND2*(RANDOM%12+1)))
				ANS=$((OPERAND1/OPERAND2))
				echo "$OPERAND1 / $OPERAND2 = ?"
				;;
		esac

		echo -n "Input an Answer: "
		read USR_ANS

		if [ $USR_ANS -eq $ANS ]
		then
			CORRECT=1 #if they answer correctly we want to flag the question as correct!
		fi

		#Put our values into our pseudo 2D array!
		STORE_RESULTS[$i,0]=$OPERAND1
		STORE_RESULTS[$i,1]=$ARITH_OP
		STORE_RESULTS[$i,2]=$OPERAND2
		STORE_RESULTS[$i,3]=$ANS
		STORE_RESULTS[$i,4]=$USR_ANS
		STORE_RESULTS[$i,5]=$CORRECT
	done

	local END=$(date +%s%N)
	local ELAPSED=$(($END-$START)) #our elapsed time in nanoseconds! Need to reduce it
	ELAPSED_TIME=$(($ELAPSED/1000000)) #convert our time to milliseconds

	writeToFile
}

#its a quiz but with a timer and a lives system!
takeChallenge()
{
	ELAPSED_TIME=0 #reset our time! (not needed since its reset anyway at the bottom but nice to have!)

	local MAXTIME=0 #our max time in milliseconds for each level!
	local LIVES=0
	local CURR_QUESTION=0
	local ELAPSED=0
	local ELAPSED_MIL=0

	#change the dificulty based on our users level!
	case $AGE_GROUP in #get our number of questions based on the level!
		1)
			NUM_QUESTIONS=10
			MAXTIME=45000
			LIVES=5
			echo "Low Level"
			;;
		2)
			NUM_QUESTIONS=15
			MAXTIME=40000
			LIVES=4
			echo "Medium Level"
			;;
		3)
			NUM_QUESTIONS=20
			MAXTIME=35000
			LIVES=3
			echo "High level"
			;;
	esac

	clear
	echo "You have $LIVES lives and $MAXTIME seconds to finish $NUM_QUESTIONS questions, GOOD LUCK! [Press Enter to Begin]"
	read

	local START=$(date +%s%N) #get our result in nanoseconds, start the timer here!

	while [ $LIVES -gt 0 -a $MAXTIME -gt $ELAPSED_MIL -a $CURR_QUESTION -lt $NUM_QUESTIONS ]
	do
		ARITH_OP=$((RANDOM%4+1)) #random number between 1 and 4, the +1 is starting at one
		OPERAND1=NUMBER
		OPERAND2=0
		ANS=0
		USR_ANS=0
		CORRECT=0

		#echo "Quiz Time!"

		case $ARITH_OP in
			1)	#echo "Addition"
				clear
				echo "Question $(($CURR_QUESTION+1)) | $LIVES lives remaining!"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((RANDOM%12+1))
				ANS=$((OPERAND1+OPERAND2))
				echo "$OPERAND1 + $OPERAND2 = ?"
				;;
			2)	#echo "Subtraction"
				clear
				echo "Question $(($CURR_QUESTION+1)) | $LIVES lives remaining!"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((OPERAND2+(RANDOM%12+1))) #the random number here has to be +12 on the number so we never get a negative value!
				ANS=$((OPERAND1-OPERAND2))
				echo "$OPERAND1 - $OPERAND2 = ?"
				;;
			3)	#echo "Multiplication"
				clear
				echo "Question $(($CURR_QUESTION+1)) | $LIVES lives remaining!"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((RANDOM%12+1))
				ANS=$((OPERAND1*OPERAND2))
				echo "$OPERAND1 * $OPERAND2 = ?"
				;;
			4) 	#echo "Division"
				clear
				echo "Question $(($CURR_QUESTION+1)) | $LIVES lives remaining!"
				OPERAND2=$((RANDOM%12+1))
				OPERAND1=$((OPERAND2*(RANDOM%12+1)))
				ANS=$((OPERAND1/OPERAND2))
				echo "$OPERAND1 / $OPERAND2 = ?"
				;;
		esac

		echo -n "Input an Answer: "
		read USR_ANS

		if [ $USR_ANS -eq $ANS ]
		then
			#echo "CORRECT!"
			CORRECT=1
		else
			LIVES=$(($LIVES-1))
		fi

		#this will naturally be delayed until after the user answers the question, giving them the ability to answer the question even if they go over the time!
		local END=$(date +%s%N)
		ELAPSED=$(($END-$START)) #our elapsed time in nanoseconds! Need to reduce it
		ELAPSED_MIL=$(($ELAPSED/1000000))

		CURR_QUESTION=$(($CURR_QUESTION+1))

		#Put our values into our pseudo 2D array!
		STORE_RESULTS[$i,0]=$OPERAND1
		STORE_RESULTS[$i,1]=$ARITH_OP
		STORE_RESULTS[$i,2]=$OPERAND2
		STORE_RESULTS[$i,3]=$ANS
		STORE_RESULTS[$i,4]=$USR_ANS
		STORE_RESULTS[$i,5]=$CORRECT

		if [ ! $LIVES -gt 0 ]
		then
			echo -n "You ran out of lives, Game Over! [Enter to Finish]"
			read
		elif [ ! $MAXTIME -gt $ELAPSED_MIL ]
		then
			echo -n "You ran out of time, Game Over! [Enter to Finish]"
			read
		elif [ $CURR_QUESTION -eq $NUM_QUESTIONS]
		then
			echo -n "Congratulations! You completed the challenge with $LIVES lives left and $(($MAXTIME-$ELAPSED_MIL)) milliseconds remaining! [Enter to Finish]"
			read
		fi
	done
	writeToFile
}

login()
{
	#create local variables so we only set them global if we gte a match below
	local UNAME=""
	local PWORD=""

	#until the user details is not empty!
	until [ ${#USERDETAILS[@]} -ne 0 ]
	do
		#read in username and password in here!
		until [[ $UNAME =~ $USRRE ]]
		do
			read -p "Enter a Username: " UNAME

			if ! [[ $UNAME =~ $USRRE ]]
			then
				clear
				echo "This username is invalid"
			fi
		done

		until [[ $PWORD =~ $PWDRE ]]
		do
			read -s -p "Enter the Password: " PWORD

			if ! [[ $PWORD =~ $PWDRE ]]
			then
				clear
				echo "This password is invalid"
			fi
		done

		while read LINE #reads each line
		do
			USERLINE="$LINE"
		done < <(grep $UNAME login.txt | grep $PWORD) #process substitution, pass the file/line into grep to find a matching UNAME and PASS using a pipe to check rows!

		USERDETAILS=($USERLINE) #explode USERLINE details into USERDETAILS array (extract or split), the dollar sign outisde the brackets is for finding the specific var!

		if [ ${#USERDETAILS[@]} -eq 0 ] #if length of array is equal to zero
		then
			clear
			echo "Username and Password not recognised. Try Again!"
			#reset the username and password for retry!
			UNAME=""
			PWORD=""
		else
			FNAME=${USERDETAILS[0]}
			USR=${USERDETAILS[1]}
			PASS=${USERDETAILS[2]}
			LEVEL=${USERDETAILS[3]}
			AGE_GROUP=${USERDETAILS[4]}
			CURR_USER=$USR
		fi
	done
}

#create a new user account!
createAccount()
{
	clear
	local FILE="login.txt"
	local FNME=""
	local UNAME=""
	local PWORD=""
	local LVL=""
	local AGEGRP=""

	if [ ! -f "$FILE" ] #if the file doesn't exist
	then
		touch "$FILE" #make the file
	fi

	#check if each input is valid!
	until [[ $FNME =~ $FNMRE ]]
	do
		echo -n "Enter a first name: "
		read FNME
		clear
		if ! [[ $FNME =~ $FNMRE ]]
		then
			echo "Invalid first name: $FNME"
		fi
	done

	until [[ $UNAME =~ $USRRE ]]
	do
		echo -n "Enter an account username: "
		read UNAME
		clear
		if ! [[ $UNAME =~ $USRRE ]]
		then
			echo "Invalid account username: $UNAME"
		fi
	done

	until [[ $PWORD =~ $PWDRE ]]
	do
		echo -n "Enter a Password: "
		read -s PWORD
		clear
		if ! [[ $PWORD =~ $PWDRE ]]
		then
			echo "Invalid Password, Please try again!"
		fi
	done

	until [[ $LVL =~ $NUMRE && $LVL > 0 && $LVL < 3 ]] #need the regex comparison first!
	do
		echo -n "Enter a Level [1 - Teacher | 2 - Student]: "
		read LVL
		clear
		if ! [ $LVL -ge 1 -a $LVL -le 2 ]
		then
			echo "Invalid Level!"
		fi
	done

	until [[ $AGEGRP =~ $NUMRE && $AGEGRP > 0 && $AGEGRP < 4 ]]
	do
		if ! [ $LVL -eq 1 ]
		then
			echo -n "Enter an Age Group [1 - Young | 2 - Middle | 3 - Old]: "
			read AGEGRP
			clear
		else
			AGEGRP=0
		fi
	done

	echo -ne "$FNME\t$UNAME\t$PWORD\t$LVL\t$AGEGRP\n" >> "$FILE"
}

#THIS WORKS GREAT!!!
readResults()
{
	clear
	CHOICE=-1 #reset the choice variable
	local NUM=0
	local USR=""

	#take in a student name
	echo -n "Enter a Student Username: "
	read USR

	local OUT=$(ls -1 results | grep $USR) #get the output of the search!
	local OUT_DELIM=$(echo $OUT | tr " " "\n") #split the output into lines we can use for selection!

	clear

	if ! [ -z "$OUT" ] #if there is no output we just skip this part!
	then
		echo -n "> " #echo a cursor for the user

		until [ $CHOICE -ge 0 -a $CHOICE -lt $NUM ] #until we get a valid input!
		do
			NUM=0
			echo "Please make a choice from the list below: "

			for LINE in $OUT_DELIM #print each line and a corresponding index!
			do
				echo "[$NUM]: $LINE"
				NUM=$(($NUM+1)) #count up
			done

			echo -n "> "

			local NUMTEMP=0
			read CHOICE
			if [ $CHOICE -ge 0 -a $CHOICE -lt $NUM ]
			then
				for LINE in $OUT_DELIM
				do
					if [ $CHOICE -eq $NUMTEMP ]
					then
						clear
						local FILENAME=$LINE #store the filename for use later
						echo "[$NUMTEMP]: $LINE (Enter to Exit)" #print the current file
						cat "results/$FILENAME" #print the results directly from the file
					fi
					NUMTEMP=$(($NUMTEMP+1))
				done
			else
				clear
				echo "Out of range, Please try again!"
				NUMTEMP=0 #reset this so we don't keep looping the values!
			fi
		done
	else
		echo "No results under the name: $USR (Enter to Exit)"
	fi
	read #this read is to halt the program until the user hits enter to continue!
}

modifyDeleteUser()
{
	clear
	CHOICE=-1
	local USR=""
	local USERLINE=""
	local USRDETAILS=()
	local FILE="login.txt"

	while [ ${#USRDETAILS[@]} -eq 0 ] #if the array of user details is empty
	do
		echo -n "Enter a student name for modification/deletion: "
		read USR

		while read LINE #reads each line
		do
			USERLINE="$LINE"
			echo $USERLINE
		done < <(grep $USR $FILE)

		USRDETAILS=($USERLINE)

		if [ ${#USRDETAILS[@]} -gt 0 ] #if we find a user
		then
			CHOICE=-1 #reset choice
			clear
			until [ $CHOICE -ge 1 -a $CHOICE -le 2 ]
			do
				echo "Currently Selected User: $USR"
				echo "Please choose one of the options below:"
				echo "1 : Modify User"
				echo "2 : Delete User"
				echo -n "> "
				read CHOICE

				case $CHOICE in
					1)
						#easiest option here is just to delete the user and recreate the account from scratch!
						grep -v $USR $FILE > temp.txt
						cat temp.txt > $FILE
						rm temp.txt
						createAccount
						;;
					2)
						#use an inverted GREP to remove the line containing the string!
						grep -v $USR $FILE > temp.txt
						cat temp.txt > $FILE
						rm temp.txt
						echo "User Deleted!"
						;;
					*)
						clear
						echo "Invalid Option"
						;;
				esac
			done
		else
			clear
			echo "None Found, Please try again!"
		fi
	done
}

main #run our main method to begin the script!
