from __future__ import print_function

import sys
import string
from git_requests import *

# --------------- Helpers that build all of the responses ----------------------

default_user = "rails"
default_repo = "rails"
#default_user = "rkinney4"
#default_repo = "HopHacks2016"
default_branch = "master"

# Provided function to create speechlet responses to send to Alexa
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }
    
# Function to create responses to send to Alexa
def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }

# Get the branch from the attributes, or return the default branch
def get_branch_from_attributes(session_attributes):
    if 'currentBranch' in session_attributes:
        return session_attributes['currentBranch']
    else:
        return default_branch

# --------------- Functions that control the skill's behavior ------------------

# Welcome message for the skill
def get_welcome_response():

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa git interface. "

    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say something like : get the last commit, or \
        list all branches."
            
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

# End the session
def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Goodbye and remember to commit early and often"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# Get the last n commits and say them
def get_last_n_commits_from_session(intent, session):
    global default_user, default_repo

    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"


    branch = get_branch_from_attributes(session_attributes)

    if 'Num' in intent['slots']:
        num = int(intent['slots']['Num']['value'])
        speech_output = last_n_commits(default_user, default_repo, branch=branch, n=num)
    else :
        speech_output = "I'm not sure how many commits you want. " \
                        "Please try again."
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Get the last commit and say it
def get_last_commit_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    branch = get_branch_from_attributes(session_attributes)

    speech_output = last_n_commits(default_user, default_repo, branch=branch,n=1)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# List all the branches of the repository
def get_branches_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    speech_output = list_branches(default_user, default_repo)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Switch to the specified branch number
def switch_branches_from_session(intent, session):
    session_attributes = session.get('attributes', {})

    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    if 'Num' in intent['slots']:
        num = int(intent['slots']['Num']['value'])
        (new_branch, speech_output) = switch_branch(default_user, default_repo, num)

        if new_branch != "":
            session_attributes['currentBranch'] = new_branch
    else :
        speech_output = "I'm not sure which branch you want to switch to. " \
                        "Please try again."

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Switch to branch master
def switch_to_master_from_session(intent, session):
    session_attributes = session.get('attributes', {})

    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    session_attributes['currentBranch'] = default_branch

    speech_output = "Switched to branch master"

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    
# Say the current branch
def get_current_branch_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"


    branch = get_branch_from_attributes(session_attributes)

    speech_output = "The current branch is " + branch

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Get contributors for a repository, may say all or simply the number
# if there are too many
def get_contributors_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    speech_output = get_contributors(default_user, default_repo)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# Get the top contributors to the repository
def get_top_contributors_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    speech_output = get_top_three_contributors(default_user, default_repo)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "GetNCommitsIntent":
        return get_last_n_commits_from_session(intent, session)
    elif intent_name == "GetLastCommitIntent":
        return get_last_commit_from_session(intent, session)
    elif intent_name == "GetBranchesIntent":
        return get_branches_from_session(intent, session)
    elif intent_name == "SwitchBranchIntent":
        return switch_branches_from_session(intent, session)
    elif intent_name == "SwitchToMasterIntent":
        return switch_to_master_from_session(intent, session)
    elif intent_name == "GetCurrentBranchIntent":
        return get_current_branch_from_session(intent, session)
    elif intent_name == "GetContributorsIntent":
        return get_contributors_from_session(intent, session)
    elif intent_name == "GetTopContributorsIntent":
        return get_top_contributors_from_session(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])


    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
