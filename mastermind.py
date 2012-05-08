# mastermind.py
# Author: Chris Corea
#
# Commandline implementation of Mastermind

from google.appengine.ext import db
from random import randint
def printInstructions():
	print "\n\nThis is a game of wits and luck! " \
          "Try to guess the right colors! \n" \
          "The computer will automatically generate a random color code made up of six colors, \n" \
          "you're job is to figure out that secret code. " \
          "You will be asked to insert a color to try to match the secret code. \n" \
          "Remember, the code that you generate must be exactly like the secret code, " \
          "the order of the colors does matter,\n" \
          "but don't worry, you will be able to see all" \
          " of the combinations that you enter while getting feedback from the game.\nYou will first be" \
          "asked to enter the number of how many colors you would like to have in play; you can choose up \n" \
          "to 6 colors and they will be used in the order that they are listed in below. \n" \
          "\nThe colors you will use for this game are listed below. Good luck!\n\n"

class Scores(db.Model):
	user = db.UserProperty()
	numberGuesses = db.IntegerProperty()
	name = db.StringProperty()

def generateSecret():
  colors = getColors()
  return [colors[randint(0,5)] for x in xrange(4)]

def getGuess():
	colors = getColors()
	print "enter 4 colors from:"+str(colors)
	i = 0
	guess = []
	while i < 4:
		color=raw_input('enter a color: ')
		guess.append(color)
		i += 1
	return guess

def getColors():
	return  ['red','green','blue','purple','orange','yellow']

def computeExacts(guess,secretCopy):
	i = 0
	match = 0
	while i < 4:
		if guess[i] == secretCopy[i]:
			match += 1
			# cross out
			guess[i] = 'chris'
			secretCopy[i] = 'david'
		i += 1
	return match

def computePartials(guess, secretCopy):
	i = 0
	partial_matches = 0
	while i < 4:
		j = 0
		while j < 4:
			if guess[i] == secretCopy[j]:
				partial_matches += 1
				# "cross out" finds
				guess[i] = ''
				secretCopy[j] = ''
			j += 1
		i += 1
	return partial_matches


# main
if __name__=='__main__':
	printInstructions()
	secretCode = generateSecret()
	
	matches = 0
	while matches != 4:
		secretCopy = secretCode[:]
		guess = getGuess()
		print guess
		matches = computeExacts(guess, secretCopy)
		partial_matches = computePartials(guess,secretCopy)
		print 'Exact matches:' + str(matches)
		print 'Partial matches:' + str(partial_matches)

	print 'Congratulations!! You have beaten Mastermind!'



