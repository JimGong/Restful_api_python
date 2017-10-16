import unittest
import requests
import random
import string
import datetime
from datetime import date
import json

# local host address. Change only if this is not the address server running on.
url = 'http://127.0.0.1:5000'

# unique id for every new project created
idNumber = 1

# Generate a valid JSON with all necessary fields
def create_valid_project():
	global idNumber

	countries = ["","USA", "CANADA", "MEXICO", "BRAZIL","CHINA", "Korea", "Japan", "Britain", "France", "Italy", "Germany"]
	enable = [True, False]

	# Creates an array of countries in random order
	selected_countries = []
	for x in range (random.randint(0, len(countries))):
		selected_countries.append(random.choice(countries))

	# set fields for project
	project = {
		"projectUrl": "www." + str(idNumber) + ".com/",
		"projectName": "proj " + str(idNumber),
		"enabled": random.choice(enable),
		"expiryDate": datetime.datetime(random.randint(2005, 2020), random.randint(1,12), random.randint(1,28),0,0,0).strftime("%m%d%Y %H:%M:%S"),
		"creationDate": datetime.datetime(random.randint(2005, 2020), random.randint(1,12), random.randint(1,28),0,0,0).strftime("%m%d%Y %H:%M:%S"),
		"projectCost": random.randint(1,1000),
		"targetCountries": selected_countries,
		"targetKeys":[{"number": random.randint(1,100),"keyword": ''.join(random.choice(string.ascii_lowercase) for i in range (random.randint(0,20)))}],
		"id": idNumber
	}

	project = json.dumps(project)
	idNumber += 1

	return project

class RequestTestCase(unittest.TestCase):
	def testWithNoParameters0(self):
		response = requests.get(url + "/requestproject")
		self.assertEqual(response.status_code, 200)
	def testWithOneParameter1(self):
		response = requests.get(url + "/requestproject?projectid=1")
		self.assertEqual(response.status_code, 200)		
	def testWithOneParameter2(self):
		response = requests.get(url + "/requestproject?number=1")
		self.assertEqual(response.status_code, 200)
	def testWithOneParameter3(self):
		response = requests.get(url + "/requestproject?keyword=hiking")
		self.assertEqual(response.status_code, 200)
	def testWithOneParameter4(self):
		response = requests.get(url + "/requestproject?country=china")
		self.assertEqual(response.status_code, 200)
	def testWithMutipleParameters0(self):
		response = requests.get(url + "/requestproject?projectid=1&country=china")
		self.assertEqual(response.status_code, 200)
	def testWithMutipleParameters1(self):
		response = requests.get(url + "/requestproject?country=china&number=7")
		self.assertEqual(response.status_code, 200)
	def testWithMutipleParameters2(self):
		response = requests.get(url + "/requestproject?country=brazil&&keyword=sports")
		self.assertEqual(response.status_code, 200)
	def testWithMutipleParameters3(self):
		response = requests.get(url + "/requestproject?country=china")
		self.assertEqual(response.status_code, 200)
	def testWithMutipleParameters4(self):
		response = requests.get(url + "/requestproject?country=china&country=japan")
		self.assertEqual(response.status_code, 200)
	def testWithParamFlag(self):
		response = requests.get(url + "/requestproject?")
		self.assertEqual(response.status_code, 200)
	def testInvalidParameter(self):
		response = requests.get(url + "/requestproject?id=1")
		self.assertEqual(response.status_code, 400)
	def testInvalidParameterValue0(self):
		response = requests.get(url + "/requestproject?id=1abc")
		self.assertEqual(response.status_code, 400)
	def testInvalidParameterValue1(self):
		response = requests.get(url + "/requestproject?number=1abc")
		self.assertEqual(response.status_code, 400)


class CreateTestCase(unittest.TestCase):
	def testWithNoData(self):
		response = requests.get(url + "/create_project")
		self.assertEqual(response.status_code, 404)
	def testInvalidURL(self):
		response = requests.post(url + "/create_project/createoneproject")
		self.assertEqual(response.status_code, 404)
	def testValidJSON(self):
		new_project = create_valid_project()
		headers = {'content_type': 'application/json'}
		response = requests.post(url + "/createproject", data = new_project, headers = headers)
		self.assertEqual(response.status_code, 200)
	def testInvalidJSON(self):
		new_project = {"id": 1}
		response = requests.post(url + "/createproject", data = new_project)
		print response
		self.assertEqual(response.status_code, 400)
	def testInvalidHeader(self):
		new_project = create_valid_project()
		headers = {'content_type': 'text/html'}
		response = requests.post(url + "/createproject", data = new_project, headers = headers)
		self.assertEqual(response.status_code, 400)
	def testMultiplePOST(self):
		for x in range(0, 100):
			new_project = create_valid_project()
			headers = {'content_type': 'application/json'}
			response = requests.post(url+"/createproject", data = new_project,headers = headers)
			self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
	unittest.main()