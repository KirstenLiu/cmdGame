import sys
from os import system, name
import logging
import datetime
from random import seed
from random import randint

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(funcName)s - %(message)s')

rand_seed = 1

class Setting:
	chances = 10
	quit_key = 'Q'

class Num:
	lower_bound = 0
	upper_bound = 1000
	value = 0

	def __init__(self):
		rand_seed = int(datetime.datetime.strftime(datetime.datetime.now(), '%m%d%H%M%S'))
		seed(rand_seed)

		self.value = randint(self.lower_bound, self.upper_bound)
		#logging.debug(self.value)

class Answer:	
	value = 0

	def __init__(self):
		num = Num()
		#logging.debug(num.value)
		self.value = num.value


class Game:	
	guess = -1
	loop = 0
	def __init__(self, screen, ans):
		# ask for input
		self.screen =screen
		self.guess = int(screen.ask_input('guess'))
		self.ans = ans
		self.loop = 0

	def game_loop(self):
		logging.debug(ans)
		while (self.guess != Setting.quit_key):
			guess = int(self.guess)
			if (self.loop >= Setting.chances - 1):
				screen.print_info('out')
				break
			# compare input with generated ans and return hint if it's bigger or smaller
			if (guess > self.ans):
				self.guess = screen.ask_input('bigger')
			elif (guess < self.ans):
				self.guess = screen.ask_input('smaller')
			else:
				screen.print_info('correct')
				return screen.ask_input('again')

			self.loop += 1

info_array = {'welcome':'welcome to number guessing. You have ' + str(Setting.chances) + ' chances to guess.', 
			  'guess':'please enter a number between ' + str(Num.lower_bound) + ' to ' + str(Num.upper_bound) + ' to guess: ',
			  'bigger':'your guess is bigger than the answer. Please try again or hit ' + Setting.quit_key + ' to stop playing: ',
			  'smaller':'your guess is smaller than the answer. Please try again or hit ' + Setting.quit_key + ' to stop playing: ',
			  'correct':'you make the right guess!',
			  'out':'you run out of guessing chances!',
			  'again':'play another round? Y/any other keys: '
			 }		

class Screen:
	def __init__(self):
		self.os_name = name

	def clean_screen(self):
		if self.os_name == 'posix':
			_ = system('clear')
		else:
			_ = system('cls')
	def print_info(self, info_key):
		print(info_array[info_key])

	def ask_input(self, info_key):
		return input(info_array[info_key])


if __name__ == "__main__":
	another = 'Y'
	# gen a random num btw 0 to 1000 as answer
	while another == 'Y':
		ans = Answer().value
		#logging.debug(ans) 
		
		screen = Screen()
		screen.print_info('welcome')
		game = Game(screen, ans)
		another = game.game_loop()
		#logging.debug(another)
		