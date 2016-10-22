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