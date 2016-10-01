import sys
import re
import urllib2
import json
import time
from geopy.geocoders import Nominatim

class Picker(object):	
	def __init__(self):
		self.line_reg_ex = '(.*\d\d)( ET | AM )(At)?(.*)'
		self.at = 'At'
		self.geolocator = Nominatim()
		self.base_url = 'http://api.wunderground.com/api/{0}/almanac/q/{1},{2}.json'

	def help(self):
		return "usage: python picker.py filename.txt secretApiKeyFile.txt"
	
	def pick(self, filename, api_secret_filename):
		f = open(filename, 'r')
		cities = []
		for line in f:
			match = re.search(self.line_reg_ex, line)
			if match == None:
				continue
			cities.append(self.get_cities(match.group(4).split()))
		f.close()
		choices = []
		for favorite, underdog in cities:
			favorite_avg_high = self.get_average_high(favorite, api_secret_filename)
			underdog_avg_high = self.get_average_high(underdog, api_secret_filename)
			if favorite_avg_high == None or underdog_avg_high == None:
				message = 'Could not find information for cities {0} & {1}'.format(favorite, underdog)
				choices.append(message)
				print message
				continue
			if favorite_avg_high > underdog_avg_high:
				print favorite
				choices.append(favorite)
			else:
				print underdog
				choices.append(underdog)
			time.sleep(10) # So the free api doesn't get mad at us
		print ", ".join(choices)

	def get_average_high(self, city_name, api_secret_filename):
		location = self.geolocator.geocode(city_name)
		if location == None:
			print "Location {0} not found".format(city_name)
			return None
			#raise Exception("Location %s not found" %city_name)
		request_url = self.base_url.format(self.get_api_secret(api_secret_filename), location.latitude, location.longitude)
		json_string = urllib2.urlopen(request_url).read()
		parsed_json = json.loads(json_string)
		return int(parsed_json['almanac']['temp_high']['normal']['C'])

	def get_api_secret(self, filename):
		with open(filename) as f:
			return f.readline().strip('\n')

	def get_cities(self, spread_line_list):
		spread_index = self.get_spread_index(spread_line_list)
		favorite = self.format_city_name(spread_line_list[:spread_index])
		underdog = self.format_city_name(spread_line_list[spread_index+1:])
		return (favorite, underdog)
	
	def format_city_name(self, city_name):
		return " ".join(self.safe_remove(city_name, self.at)).replace('NY', 'New York')

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
	if len(sys.argv) < 3:
		print picker.help()
		exit(0)
	picker.pick(sys.argv[1], sys.argv[2])
