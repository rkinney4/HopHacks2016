from __future__ import print_function

import sys
import string
from git_requests import *

# --------------- Helpers that build all of the responses ----------------------

def_user = "nodejs"
def_repo = "node"
default_branch = "master"

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
    

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def get_branch_from_attributes(session_attributes):
    if 'currentBranch' in session_attributes:
        return session_attributes['currentBranch']
    else:
        return default_branch

# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa git interface. "
    """
    Currently you can \
    specify the following three commands: get the last commit, get the last \
    N commits, or get all branches"
    """
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please say something like : get the last commit, or \
        list all branches."
            
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Goodbye and remember to commit early and often"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


def get_last_n_commits_from_session(intent, session):
    global def_user, def_repo

    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"


    branch = get_branch_from_attributes(session_attributes)

    if 'Num' in intent['slots']:
        num = int(intent['slots']['Num']['value'])
        speech_output = last_n_commits(def_user, def_repo, branch=branch, n=num)
    else :
        speech_output = "I'm not sure how many commits you want. " \
                        "Please try again."

    
    
    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_last_commit_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"


    branch = get_branch_from_attributes(session_attributes)

    speech_output = last_n_commits(def_user, def_repo, branch=branch, n=1)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def get_branches_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"

    speech_output = list_branches(def_user, def_repo)

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))

def switch_branches_from_session(intent, session):
    session_attributes = session.get('attributes', {})

    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"
    speech_output = "bla bla "

    if 'Num' in intent['slots']:
        num = int(intent['slots']['Num']['value'])
        (new_branch, speech_output) = switch_branch(def_user, def_repo, num)

        if new_branch != "":
            session_attributes['currentBranch'] = new_branch
    else :
        speech_output = "I'm not sure which branch you want to switch to. " \
                        "Please try again."

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))
    

def get_current_branch_from_session(intent, session):
    session_attributes = session.get('attributes', {})
    card_title = intent['name']
    should_end_session = False
    reprompt_text = "I didn't quite git that"


    branch = get_branch_from_attributes(session_attributes)

    speech_output = "The current branch is " + branch

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
    elif intent_name == "GetCurrentBranchIntent":
        return get_current_branch_from_session(intent, session)
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
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
