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
        plural = '' if n == 1 else 's'
        output += "I only found {0} commit{1}. ".format(len(commits), plural)
        n = len(commits)
    elif n > 1:
        output += "Here are the last {0} commits. ".format(n)
    
    for i in range(n):
        c = parse_commit(commits[i]['commit'])
        plural = '' if n == 1 else i+1
        
        output += "Commit {0} by {1}, on {2}: {3}. ".format(
            plural, c['author'],
            date_to_speech(c['date']),
            c['message'])
    
    return output


def get_branches(owner, repo):
    url = base + "/repos/{0}/{1}/branches".format(owner, repo)
    
    req = urllib2.Request(url, headers=headers)
    try:
        response = urllib2.urlopen(req)
    except:
        return "Sorry, there was an error getting the branches."

    branches = json.loads(response.read())

    return branches

def list_branches(owner, repo):
    global base, headers
    
    output = ""

    branches = get_branches(owner, repo)
    n = len(branches)

    if n == 1:
        output += "I found 1 branch. "
    else:
        output += "I found {0} branches. ".format(n)

    for i in range(n):
        branch_name = branches[i]['name']
        output += "Branch {0} : {1} .".format(i+1, branch_name)

    return output

def switch_branch(owner, repo, branch_num):
    branch_num = branch_num - 1
    output = ""
    branches = get_branches(owner, repo)
    n = len(branches)

    new_branch = ""
    if (branch_num < 0) or (branch_num >= n):
        output = "Could not switch to requested branch"
    else:
        new_branch = str(branches[branch_num]['name'])
        output = "Switched to branch " + new_branch
    
    return (new_branch, output)

# ----------------- Helper Functions -----------------
    
def parse_commit(commit):
    output = {}
    output['author'] = commit['author']['name']
    output['date'] = commit['author']['date']
    output['message'] = commit['message']
    return output

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
