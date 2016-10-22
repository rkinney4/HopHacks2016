#!/usr/bin/env python
# HopHacks 2016
# Rachel Kinney
# Edmund Duhaime

import sys
import urllib2
import json

base = "http://api.github.com"
headers = headers = {"Accept": "application/vnd.github.v3+json"}
    
def last_n_commits(owner, repo, branch='master', n=3):
    global base, headers
    
    output = ""
    
    url = base + "/repos/{0}/{1}/commits?sha={2}".format(owner, repo, branch)
    
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, I couldn't find any commits."
        
    commits = json.loads(response.read())
    
    if len(commits) < n:
        output += "I only found {0} commits. ".format(len(commits))
        n = len(commits)
    else:
        output += "Here are the last {0} commits. ".format(n)
    
    for i in range(n):
        commit = commits[i]['commit']
        
        author = commit['author']['name']
        date = commit['author']['date']
        message = commit['message']
        
        commit_out = "Commit {0} by {1} at {2}: {3}.".format(i+1, author, date, message)
        output += commit_out
    
    return output
        
#def date_to_speech(format, date):

def list_branches(owner, repo):
    global base, headers
    
    output = ""

    url = base + "/repos/{0}/{1}/branches".format(owner, repo)
    
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, there was an error getting the branches."

    branches = json.loads(response.read())
    n = len(branches)

    if n == 1:
        output += "I found 1 branch. "
    else:
        output += "I found {0} branches. ".format(n)

    for i in range(n):
        branch_name = branches[i]['name']
        output += "Branch {0} : {1} .".format(i+1, branch_name)

    return output