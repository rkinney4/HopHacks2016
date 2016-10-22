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
        plural = '' if n = 1 else 's'
        output += "I only found {0} commit{1}. ".format(len(commits), plural)
        n = len(commits)
    elif n > 1:
        output += "Here are the last {0} commits. ".format(n)
    
    for i in range(n):
        c = parse_commit(commits[i]['commit'])
        plural = '' if n == 1 else i+1
        
        output += "Commit {0} by {1} at {2}: {3}.".format(plural, author, date, message)
    
    return output

def parse_commit(commit)
    output = {}
    output['author'] = commit['author']['name']
    output['date'] = commit['author']['date']
    output['message'] = commit['message']
    return output

#def date_to_speech(format, date):