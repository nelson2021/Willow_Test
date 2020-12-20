
# import Python unittest library.
import unittest
import csv
from datetime import datetime, timedelta

from dateutil.parser import parse as dateparse
from dateutil import tz

PACIFIC = tz.gettz('America/Los_Angeles')
EASTERN = tz.gettz('America/New_York')
seconds = 0.0


from normalizer import convert_timestamp
from normalizer import verify_zipcode
from normalizer import parse_name
from normalizer import parse_address
from normalizer import parse_duration

input_file = 'test_worksheet.csv'


def convert_PST_to_EST(datetime_str):
	parsed = dateparse(datetime_str)
	as_gmt = parsed.replace(tzinfo=PACIFIC)
	as_pacific = as_gmt.astimezone(tz=EASTERN)
	return as_pacific.isoformat()

########################################################################
### class NormalizerTestCase implements the unit test cases for the
### functions in normalizer.py script
#########################################################################
class NormalizerTestCase(unittest.TestCase):

	#################################################################
	## Unit test on the function convert_timestamp()
	##
	##################################################################
	def test_convert_timestamp(self):
		with open(input_file, newline='', encoding='utf-8') as csvfile:
			rows = list(csv.DictReader(csvfile))

		i = 1
		for row in rows:
			print("testing timestamp row ", i)
			timestamp = row['Timestamp']
			timestr_EST = convert_PST_to_EST(timestamp)
			converted = convert_timestamp(timestamp)
			print('test case output:', timestr_EST, ', script output: ', converted)
			self.assertEqual(converted, timestr_EST)
			i += 1
		csvfile.close()
	#################################################################
 	## Unit test on the function verify_zipcode()
	##
	##################################################################
		
	def test_verify_zipcode(self):
		with open(input_file, newline='', encoding='utf-8') as csvfile:
			rows = list(csv.DictReader(csvfile))
		i = 1
		for row in rows:
			print("testing zipcode row ", i)
			zipcode_in = row['ZIP']
			zipcode_out = verify_zipcode(zipcode_in)
			print('zipcode in:',zipcode_in , ', zipcode out: ', zipcode_out)
			self.assertEqual(len(zipcode_out), 5)
			i += 1
		csvfile.close()
#################################################################
## Unit test on the function parse_name()
##
##################################################################

	def test_parse_name(self):
		with open(input_file, newline='', encoding='utf-8') as csvfile:
			rows = list(csv.DictReader(csvfile))
		i = 1
		for row in rows:
			print("testing parse_name() row ", i)
			full_name = row['FullName']
			Upper_name = full_name.upper()
			name_out = parse_name(full_name)
			print('full name in:', full_name, ', full name out: ', name_out)
			self.assertEqual(name_out, Upper_name)
			i += 1
		csvfile.close()
#################################################################
## Unit test on the function parse_address()
##
##################################################################

	def test_parse_address(self):
		with open(input_file, newline='', encoding='utf-8') as csvfile:
			rows = list(csv.DictReader(csvfile))
		i = 1
		for row in rows:
			print("testing parse_address() row ", i)
			address_in = row['Address']
			address_out = parse_address(address_in)
			print('address in:', address_in, ', address out: ', address_out)
			self.assertEqual(address_out, address_in)
			i += 1
		csvfile.close()



if __name__ == '__main__':

	unittest.main()
