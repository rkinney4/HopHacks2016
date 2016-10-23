#!/usr/bin/env python
# HopHacks 2016
# Rachel Kinney
# Edmund Duhaime

import sys
import urllib2
import json
from datetime import datetime

base = "http://api.github.com"
headers = headers = {"Accept": "application/vnd.github.v3+json"}
    
# Gets the last n commits on the branch specified
def last_n_commits(owner, repo, branch='master', n=3):
    global base, headers
    
    output = ""
    url = base + "/repos/{0}/{1}/commits?sha={2}".format(owner, repo, branch)
    
    # request information from GitHub
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, I couldn't find any commits."
        
    # Parse returned json
    commits = json.loads(response.read())
    
    if len(commits) < n:
        plural = '' if n == 1 else 's'
        output += "I only found {0} commit{1}: \n".format(len(commits), plural)
        n = len(commits)
    elif n > 1:
        output += "Here are the last {0} commits: \n".format(n)
    
    for i in range(n):
        c = parse_commit(commits[i]['commit'])
        plural = '' if n == 1 else i+1
        
        output += "Commit {0} by {1}, on {2}:\n {3}. \n\n".format(
            plural, c['author'],
            date_to_speech(c['date']),
            c['message'])
    
    return output.strip('\n')

# Gets the raw branch info from GitHub
def get_branches(owner, repo):
    url = base + "/repos/{0}/{1}/branches".format(owner, repo)
    
    # request information from GitHub
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, there was an error getting the branches."

    # return json
    branches = json.loads(response.read())

    return branches

# Gets the list of branches in the repository
def list_branches(owner, repo):
    global base, headers
    
    output = ""

    branches = get_branches(owner, repo)
    n = len(branches)

    # Parse branch json
    if n == 1:
        output += "I found 1 branch: \n"
    else:
        output += "I found {0} branches: \n".format(n)

    for i in range(n):
        branch_name = branches[i]['name']
        output += "Branch {0} : {1} \n".format(i+1, branch_name)

    return output

# Switches Alexa's current branch
def switch_branch(owner, repo, branch_num):
    branch_num = branch_num - 1
    output = ""
    branches = get_branches(owner, repo)
    n = len(branches)

    # check that requested branch is valid
    new_branch = ""
    if (branch_num < 0) or (branch_num >= n):
        output = "Could not switch to requested branch"
    else:
        new_branch = str(branches[branch_num]['name'])
        output = "Switched to branch " + new_branch
    
    return (new_branch, output)
    
# Get all contributors to the repository. If the number of contributors is over
# 25, will just output the number of contributors.
def get_contributors(owner, repo):
    global base, headers
    
    output = ""
    url = base + "/repos/{0}/{1}/stats/contributors".format(owner, repo)
    
    # request information from GitHub
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, I couldn't find what you asked for on github."
    
    # GitHub returns 202 if the statistics are not yet cached, and begins to
    # calculate the statistics requested.
    if (response.getcode() == 202):
        return "Github doesn't have this information cached right now. Ask again in a few moments."
    
    # Parse returned json
    contributors = json.loads(response.read())
    numCont = len(contributors)
    
    output += "There are " + str(numCont) + " contributors: \n"
    
    if numCont > 25:
        return output.strip('\n')
    
    for i in range(numCont):
        contributor = contributors[i]['author']['login']
        output += "{0} : {1} ,\n".format(i+1, contributor)
    
    return output.strip('\n')

# Gets the top three contributors to the repo, along with their number of commits
def get_top_three_contributors(owner, repo):
    global base, headers
    
    output = ""
    url = base + "/repos/{0}/{1}/stats/contributors".format(owner, repo)
    
    # request information from GitHub
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, I couldn't find what you asked for on github."
    
    # GitHub returns 202 if the statistics are not yet cached, and begins to
    # calculate the statistics requested.
    if (response.getcode() == 202):
        return "Github doesn't have this information cached right now. Ask again in a few moments."
    
    # Parse returned json
    contributors = json.loads(response.read())
    numCont = len(contributors)
    
    output += "Out of " + str(numCont) + " contributors, the top contributors are: \n"
    
    stats = []
    for i in range(numCont):
        contributor = contributors[i]['author']['login']
        commits = contributors[i]['total']
        stats.append([commits, contributor])
    
    stats.sort()
    stats = stats[-3:]
    for i in range(len(stats)):
        output += "Number {0}. {1}, with {2} commits.\n".format(len(stats)-i, stats[i][1], stats[i][0])
        
    return output

# ----------------- Helper Functions -----------------

# parses json for a commit
def parse_commit(commit):
    output = {}
    output['author'] = commit['author']['name']
    output['date'] = commit['author']['date']
    output['message'] = commit['message']
    return output

# Converts a date returned by GitHub into speech for Alexa.
def date_to_speech(date):
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    day = datetime.strftime(date, "%d").lstrip('0')
    
    if day[-1:] in ['0','4', '5', '6', '7', '8', '9']:
        day += 'th'
    elif day[-1:] == '1':
        day += 'st'
    elif day[-1:] == '2':
        day += 'nd'
    elif day[-1:] == '3':
        day += 'rd'

    return datetime.strftime(date, "%B {0} %Y, %I:%M%p").format(day)