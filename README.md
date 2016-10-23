# HopHacks 2016: Teaching Amazon Alexa to use GitHub
#### Rachel Kinney and Edmund Duhaime

We have created a skill for Amazon Alexa that alows Alexa to interface with GitHub's API.

#### You can ask Alexa to:

  - Get the current branch
  - List all branches
  - Switch branches
  - Get the most recent commit
  - Get the last `n` commits
  - List all contributors
  - List the top three contributors

#### Public APIs and Services used:

  - [GitHub]
  - [Alexa Skills Kit]
  - [AWS Lambda]

#### Building our Hack
  1) Clone or download the repositor
  2) Run the script `./build.sh` this creates a zip file to be uploaded to AWS Lambda
  3) Upload the generated zip to AWS Lambda, creating a new function. Be sure to save the ARN in the upper right corner.
  4) On the Alexa Developer Console create a new skill. Upload the intent model and sample utterances to the new skill.
  5) Copy over the ARN from AWS Lambda into the new skill.
  6) Ask Alexa to open the newly created skill with "Alexa, open $YOUR_SKILL_NAME"

[//]: #

   [GitHub]: <https://developer.github.com/v3/>
   [Alexa Skills Kit]: <https://developer.amazon.com/alexa-skills-kit>
   [AWS Lambda]: <https://aws.amazon.com/lambda/>