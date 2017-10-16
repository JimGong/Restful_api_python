# RESTful Web Service

This is a RESTful API that uses Python 2.7.8 and Python's Flask and requests libraries.

## Getting Started

In order to run the app_projects.py, you must have Python and FLASK installed on you system.

```
$ virtualenv flask
$ flask/bin/pip install flask
```

In order to run the test.py, you must have requests installed on your system.
```
$ pip install requests
```

## Running the tests

After you `cd` to your cloned GitHub repo, execute `./app_projects.py` to start server.

If terminal shows such error: "./app_projects.py: flask/bin/python: bad interpreter: Operation not permitted", run this command line:
```
$ xattr -d com.apple.quarantine app_projects.py
```

Execute the test suite using `python test.py`.

If you want to run a specific test, execute `python test.py testClass.testName`

Ex:
```
python test.py CreateTestCase.test_1
```

### Break down into end to end tests

GET COMMAND: 

```
$ curl -i http://127.0.0.1:5000/requestproject
```
This command will return the projects on the server.
You can add custom filter at the end.
Notes: url paramaters are case insensitive.
```
$ curl -i 'http://127.0.0.1:5000/requestproject?projectid=1&country=usa&keyword=cars'
```
Notes:
`requestproject` will never return a project that is not enabled, doesn't have valid projectUrl or expired.

As long as the projectid keyword exists, all other url parameters are ignored, and it will return the first project with same id.

Example Input #1
```
$ curl -i 'http://127.0.0.1:5000/requestproject
```
This will return the project with the highest cost. (If there are multiple project with the same highest cost, return the FIRST project with the highest cost)

Example Input #2
```
$ curl -i 'http://127.0.0.1:5000/requestproject?country=brazil
```
This will return the FIRST project with the highest cost where the country is brazil.

Example Input #3
```
$ curl -i 'http://127.0.0.1:5000/requestproject?country=usa&number=20
```
This will return the FIRST project with the highest cost where the country is usa and number is 20.

Example Input #4
```
$ curl -i 'http://127.0.0.1:5000/requestproject?country=usa&number=20&keyword=sports
```
This will return the FIRST project with the highest cost where the country is usa and number is 20 and keyword is sports.

POST COMMAND: 

```
$ curl -i -H "Content-Type: application/json" -X POST -d '{"id": 1, "projectName":"test project 1","creationDate": "05112017 00:00:00","expiryDate ": "05202017 00:00:00","enabled": true,"targetCountries": ["USA", "CANADA", "MEXICO", "BRAZIL"],"projectCost": 5.5,"projectUrl": "http://www.unity3d.com","targetKeys": [{"number": 25,"keyword": "movie"}, {"number": 30,"keyword": "sports"}]}' 'http://127.0.0.1:5000/createproject'
```
This command will send a project as a valid JSON object to server.
Notes: JSON object must contain the keys listed above.


