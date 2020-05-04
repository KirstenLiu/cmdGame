import sys
from os import system, name
from random import seed
from random import randint
import datetime
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

rand_seed = 1

#4 balls, 6 colours
class Colour:
	colours = ['Red', 'Green', 'Blue', 'Yellow', 'Black', 'White']
	colour_list = list(enumerate(colours))

class Ball:
	def __init__(self, colour_num):	
		self.colour = Colour.colour_list[colour_num][1]

	def __str__(self):
		return self.colour


# answer ball set, 4 balls in whatever colour
class Answer:
	row = []
	random = []

	def __init__(self, num_of_balls, num_of_colours):
		self.num_of_balls = num_of_balls
		self.num_of_colours = num_of_colours
		self.random = []
		self.row = []

	def create_random_balls(self):
		for _ in range(self.num_of_balls):
			self.random.append(randint(0, self.num_of_colours-1))
		
		for r in self.random:
			ball = Ball(r)
			self.row.append(ball)

class Screen:
	def __init__(self):
		self.os_name = name

	def clear_screen(self):
		if self.os_name == 'posix':
			_ = system('clear')
		else:
			_ = system('cls')
	def print_hints(self, hints) -> str:
		hints_str = "Red: " + str(hints[0]) + " White: " + str(hints[1])
		print(hints_str)
		return hints_str

	def ask_input(self, info):
		return input(info)


class Game:
	num_of_balls = 4
	chances_of_guess = 6
	board = []
	another_game = False

	def __init__(self):
		# assign 4 random ball from colour set and saved as answer
		self.ans = Answer(self.num_of_balls, len(Colour.colours))
		self.ans.create_random_balls()
		logging.debug("for ans:")
		for r in self.ans.row:
			logging.debug(str(r))

		self.screen = Screen()

	def game_loop(self) -> bool:
		#self.screen.clear_screen()		
		for _ in range(self.chances_of_guess):
			#row of 4 balls as input
			k_input = []
			for guess in range(self.num_of_balls):
				info = "please enter " +str(4-guess) + " guess" + str(Colour.colours) + ": "
				input_c = self.screen.ask_input(info)
				#logging.debug(input_c)
				if input_c not in Colour.colours:
					errMsg = ("please enter the guess that is in " + str(Colour.colours) + ": " )
					input_c = self.screen.ask_input(errMsg)
				
				k_input.append(input_c)

			#compare the input with answer
			#output 4 hints: [red: int, white: int]
			hints = [0, 0]

			rest, inputs = [], []
			self.copy_array(self.ans.row, rest)
			self.copy_array(k_input, inputs)

			red_hints = self.find_red_hint(k_input, rest, inputs)
			hints[0] = red_hints

			check = self.right_guess_checker(hints)
			if check == 1:
				self.another_game = True
				break
			elif check == 0:
				pass
			else:
				#logging.debug(check)
				self.another_game = False
				break

			white_hints = self.find_white_hint(rest, inputs)
			hints[1] = white_hints
			hints_str = self.screen.print_hints(hints)

			self.board.append((k_input, hints_str))
			#self.board.append((hints_str))
			print(self.board)

		return self.another_game
	
	def right_guess_checker(self, hints) -> int:
		if(hints[0] == self.num_of_balls):
			another_info = "you made the right guess! Another turn? Y/N:"
			another = self.screen.ask_input(another_info)
			print(another)
			return self.yes_or_no(another)
		else:
			return 0

	def yes_or_no(self, keyboard_input) -> int:
		if keyboard_input == 'Y':
			return 1
		elif keyboard_input == 'N':
			logging.debug("NNNNNNN")
			return -1
		else:
			info = "please enter Y or N:"
			again = self.screen.ask_input(info)
			return self.yes_or_no(again)


	def find_red_hint(self, k_input, rest, inputs) -> int:
		r_count = 0
		for i, r in enumerate(self.ans.row, start = 0):
				if k_input[i] == r.colour:
					r_count += 1
					rest.remove(str(k_input[i]))
					inputs.remove(k_input[i])
		return r_count

	def find_white_hint(self, answer, inputs) -> int:
		colour_sets = []
		for colour in Colour.colour_list:
			colour_sets.append([colour[1],0])

		for ans in answer:
			for colour_count in colour_sets:
				for colour in inputs:
					if colour == ans and ans == colour_count[0]:
						#logging.debug(ans)
						#logging.debug(colour_count[0])
						#logging.debug(colour)
						colour_count[1] += 1
						break

		#logging.debug(colour_sets)
		white = 0
		for colour_set in colour_sets:
			if colour_set[1] >= 1:
				white += colour_set[1]
		colour_sets = []
		return white

	def copy_array(self, source, destination):
		for item in source:
			destination.append(str(item))



if __name__ == "__main__":
	print("welcome to mastermind.")
	#logging.debug(play_again)
	while play_again:
		rand_seed = int(datetime.datetime.strftime(datetime.datetime.now(), '%m%d%H%M%S'))
		#logging.debug(rand_seed)
		seed(rand_seed)
		new_game = Game()
		play_again = new_game.game_loop()


