## Surakshit Marg - Road Safety Advisor

This is for my school. Since my school is participating in an external competition, they had asked me to create something based off of it so yaa.

Essentially, it kinda acts like an interactive app for students to learn road safety from. Planning on adding image classification later on, but for now it's simple python stuff.
            It tells you the level of risk a certain road condition has, and who or what is the main priority and how to mitigate the risks with precautions.

## Features
Users have 2 choices:
                    1. Click the chech boxes on the condition of the scenario to get safety score
                    2. Enter the situation as a sentence in the textbox to get safety score

You get:
        I. The range of risk
        II. The safety score
        III. Whether 'No','Low','Medium',or'High'risk
        IV. Who or what is top priority
        V. How to manage the situation

Another feature is that you can save the scenario for later use. And, you can also add your or your team's name for submission.

# Future
Trying to get image classification for smaller students in primary and kinder
An interactive game to make it better

# Tech stack
- Python (Flask)
- HTML, CSS, JavaScript


# Project structure
`app.py` - Python-Flask backend for scenario scoring 
`wsgi.py` - WSGI entrypoint for deployment
`templates/index.html` - Main UI
`static/styles.css` - UI styling
`static/app.js` - UI
`render.yaml` - Render
`Procfile` - Process start command
