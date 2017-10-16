#!flask/bin/python
import os
import json
import types
import datetime
import collections
from flask import abort
from flask import Flask
from flask import jsonify
from flask import request
from flask import make_response
from datetime import datetime, date, time

app = Flask(__name__)

# load the json array of projects from the file Projects.txt
if os.path.isfile('./Projects.txt'):
    with open('Projects.txt','r') as json_file:
        projects = json.load(json_file)
else:
    projects = []

# check if a string is int or not.
# ex: s=1234 => True, s=12a3 => False
def representIntOrEmpty(s):
    if s == None:
        return True
    try:
        int(s)
        return True
    except ValueError:
        return False

# given a list of projects, simplify each project with only three fields
def buildReturnProjects(projects):
    resultProjects = []
    for cur_proj in projects:
        return_formatteed_project = buildProject(cur_proj)
        resultProjects.append(return_formatteed_project)
    return resultProjects

# get a project, and return a project with only three fields
def buildProject(project):
    resultProject = {
        'projectid': project['id'],
        'projectName': project['projectName'],
        'projectCost': project['projectCost'],
        'projectUrl': project['projectUrl']
    }
    return resultProject

# create a copy of all valid project that expiryDate is later than today and has valid url and enabled
def getValidProjects(projects):
    # get the date of today when called
    now = datetime.now()

    validProjects = []
    for curProj in projects:
        expDate = curProj['expiryDate']
        parsed_expDate = datetime.strptime(expDate, "%m%d%Y %H:%M:%S")

        if(parsed_expDate > now):
            if(curProj['enabled']):
                if(curProj['projectUrl'] != None):
                    validProjects.append(curProj)
    return validProjects

# given a list of projects, return the highest cost projects
# if multiple project has the same highest cost, return the first project has the same highest cost.
def getHighestCostProject(selectedProjects):
    currHighest = -1
    highestProject = {}
    for currProj in selectedProjects:
        high=currProj['projectCost']
        if(currHighest < high):
            currHighest = high
            highestProject = currProj
    return highestProject

# given a list of projects and the id you want to find
# return the first project with same id
def getProjectWithSameID(selectedProjects, targetID):
    for currProj in selectedProjects:
        if(float(currProj['id']) == float(targetID)):
            return currProj
    return []

# given a list of project, and country, number, keyword
# return all the project that match these searching keywords with only three fields
def getProjectWithFilter(selectedProjects, country, number, keyword):
    filteredProjects = []

    for currProj in selectedProjects:

        # if country is None return true, else return true if the country is found in currProj
        if True if country == None else (country.lower() in [x.lower() for x in currProj['targetCountries']]):
            # if keyword and number are not equal to None, search these
            if(keyword != None) or (number != None):
                targetKeys = currProj['targetKeys']
                for curKey in targetKeys:
                    # if number is None, dont compare, else searching matching project
                	if True if number == None else (float(curKey['number']) == float(number)):
                        # if keyword is None, dont caompare, else search matching keyword
                		if True if keyword == None else (curKey['keyword'].lower() == keyword.lower()):
                			filteredProjects.append(currProj)

            else:
                #both keywork and number is none. Done searching
                filteredProjects.append(currProj)
    
    return filteredProjects

# handle requestproject request, with optional query strings
@app.route('/requestproject', methods = ['GET'])
def getProjects():
    urlParam = ['projectid', 'country', 'number', 'keyword']

    # return 400 status code if user input is an unknown param
    queryString = request.args
    for currString in queryString:
        if not currString in urlParam:
            abort(400)

    validProjects = getValidProjects(projects)

    # get the keyword from url param
    targetID = request.args.get('projectid',None)
    targetCountry = request.args.get('country',None)
    targetNumber = request.args.get('number',None)
    targetKeyword = request.args.get('keyword',None)

    # check type of the id and number, if not string then abort with status code 400
    if not representIntOrEmpty(targetID):
        abort(400)
    if not representIntOrEmpty(targetNumber):
        abort(400)

    # if there is id param, ignore all others. example: projectid=1 or projectid=5&country=brazil&number=20
    if targetID != None:
        result = getProjectWithSameID(validProjects,targetID)
        
        if len(result) == 0:
            return jsonify({'message': 'No project found'})
        else:
            result = buildProject(result) 
            return  jsonify(result)

    # return project of the highest cost if no url param.
    elif(targetID == None and targetCountry == None and targetNumber == None and targetKeyword == None):
        highestProject = getHighestCostProject(validProjects)
        
        if highestProject == {}:
            return jsonify({'message': 'No project found'})
        highestProject = buildProject(highestProject) 
        return jsonify(highestProject)
    
    else:
        # no id. every else situtation goes here
        result = getProjectWithFilter(validProjects, targetCountry, targetNumber, targetKeyword)

        if len(result) == 0:
            return jsonify({'message': 'No project found'})
        else: 
            highestProject = getHighestCostProject(result)
            return jsonify(result)

# handle error message and return 404 status code
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'message': 'No project found'}),404)

# handle createproject request
@app.route('/createproject', methods = ['POST'])
def createProject():
    keys = {'id', 'projectName', 'creationDate', 'expiryDate', 'enabled', 'targetCountries', 'projectCost', 'projectUrl', 'targetKeys'}

    # if not valid JSON object, then abort
    if not request.json:
        print "abort"
        abort(400)

    # if JSON object doesnt have all fields, then abort
    if set(request.json.keys()) != set(keys):
        for neededKey in keys:
            if not neededKey in request.json.keys():
                print "missing: ", neededKey, "abort"
        abort(400)

    project = request.json

    # add new created project into projects list
    projects.append(project)

    # write the array of projects into file "Projects.txt"
    with open('Projects.txt','w') as outfile:
        json.dump(projects, outfile, indent = 2);

    # return the jsonified project list and a status code of 200
    return jsonify({'projects': projects}), 200

# handle index page
def index():
    return "Welcome!"

# main
if __name__ == '__main__':
    app.run(debug=True)
