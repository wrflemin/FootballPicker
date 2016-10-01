import sys
import re

class Picker(object):	
	def __init__(self):
		self.line_reg_ex = '(.*\d\d)( ET | AM )(At)?(.*)'
		self.at = 'At'
	def help(self):
		print "usage: python picker.py filename.txt"
	
	def pick(self, filename):
		f = open(filename, 'r')
		cities = []
		for line in f:
			match = re.search(self.line_reg_ex, line)
			if match == None:
				continue
			cities.append(self.get_cities(match.group(4).split()))
		f.close()
		for favorite, underdog in cities:
			print "fav: ", favorite
			print "und: ", underdog
	
	def get_cities(self, spread_line_list):
		spread_index = self.get_spread_index(spread_line_list)
		favorite = " ".join(self.safe_remove(spread_line_list[:spread_index], self.at))
		underdog = " ".join(self.safe_remove(spread_line_list[spread_index+1:], self.at))
		return (favorite, underdog)
	
	def safe_remove(self, word_list, string_to_remove):
		try:
			word_list.remove(string_to_remove)
		except ValueError:
			pass
		return word_list

	def get_spread_index(self, line):
		for i, word in enumerate(line):
			if word.startswith('-'):
				return i
		raise Exception('No spread line. Example line is: 10/2 1:00 ET At Washington -9 Cleveland')

if __name__ == "__main__":
	picker = Picker()
	if len(sys.argv) < 1:
		print picker.help()
	picker.pick(sys.argv[1])
