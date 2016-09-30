import sys
import re

class Picker(object):	
	def __init__(self):
		self.line_reg_ex = '(.*\d\d)( ET | AM )(At)?(.*)'
	
	def help(self):
		print "usage: python picker.py filename.txt"
	
	def pick(self, filename):
		f = open(filename, 'r')
		for line in f:
			match = re.search(self.line_reg_ex, line)
			if match == None:
				continue
			cities = self.get_cities(match.group(4).split())
			print cities
	
	def get_cities(self, spread_line_list):
		cities = []
		for word in spread_line_list:
			if not word.startswith('-') and word != 'At':
				cities.append(word)
		return cities

if __name__ == "__main__":
	picker = Picker()
	if len(sys.argv) < 1:
		print picker.help()
	picker.pick(sys.argv[1])
