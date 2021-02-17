from flask import Flask, request, render_template, redirect, flash, session

# debug toolbar
from flask_debugtoolbar import DebugToolbarExtension

from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "the password is 'password'"

# debug toolbar
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Establish the session name for the survey
SURVEY_SESSION = "survey_session"
DEBUG_SESSION = True

# survey title
title = satisfaction_survey.title
# # A list is used for the question counter instead of a primitive integer because the counter
# #  requires an updates in the answer route to advance to the next question. A global primitive
# #  can get referenced but it cannot change.
# # The work-around is to convert question_nbr_current from a primitive to a list because list
# #  elements ARE alterable -- heck, we can add answers to responses!
# question_nbr_current = [0]

# # responses list to hold the answers to the survey questions.
# responses = []


def get_curr_question_nbr():
    """ get the index for the next question based on number of saved responses """

    return len(session[SURVEY_SESSION])


def survey_reset_controls():
    """ function resets survey control variables """

    # question_nbr_current[0] = 0

    # # responses list to hold the answers to the survey questions.
    # responses.clear()
    session[SURVEY_SESSION] = []


@app.route("/")
def survey_welcome():
    """ Renders a welcome page with the title of the survey, the instructions, 
        and a button to start the survey. 

        The button issues a post command to the /session route which sets up 
        responses structure in session storage. The /session route then calls 
        /questions

    """

    instructions = satisfaction_survey.instructions

    return render_template("welcome.html", survey_title=title,
                           survey_instructions=instructions,
                           debug=DEBUG_SESSION)


@app.route("/session", methods=["POST"])
def session_setup():
    """ Checks whether survey_responses session exists and creates 
        survey_responses when survey_responses does not exist. 

        Route redirects to /questions which will either start with 
        question 0, start where the last session ended, or immediately
        place the visitor on the thank you page when the survey was
        completed. 

    """

    try:
        print(
            f"session_setup: trying to read {SURVEY_SESSION} from session", flush=True)
        responses = session[SURVEY_SESSION]

    except KeyError:
        print(
            f"session_setup: KeyError: need to create {SURVEY_SESSION}.", flush=True)

        # session does not exist for SURVEY_SESSION
        responses = []
        session[SURVEY_SESSION] = responses

    print(
        f"session_setup: {SURVEY_SESSION} exists. {SURVEY_SESSION} = {session[SURVEY_SESSION]}", flush=True)

    if (len(responses) < len(satisfaction_survey.questions)):
        return redirect("/questions")
    else:
        return redirect("/thankyou")


@app.route("/questions")
def survey_questions():
    """ Handles a survey questions. The question number is passed 
        in as a variable name in the route.

        The page presents the current survey question and possible 
        answer choices as radio buttons. 

        Answering the question (no button) generates a post 
        request to /answer with the answer selected. 

        Answer page will eventually redirect back to questions
        where the next question is asked.

    """

    # The survey question number was passed in as a parameter but right from
    #  inception of the code, a global counter was used instead of passing in
    #  a question number.
    # Unfortunately, too much time was lost trying to figure out why the counter
    #  could not get updated and references to typically failed in the answer
    #  route. Not happy . . the time is gone.

    title = satisfaction_survey.title
    question_nbr = get_curr_question_nbr()

    # question_text = satisfaction_survey.questions[question_nbr_current[0]].question
    question_text = satisfaction_survey.questions[question_nbr].question

    # the answers for the survey question require processing. We need a value to present
    #  as text on the form and an internal form value (id) for each answer.
    answers = []
    idx = 0
    # for answer in satisfaction_survey.questions[question_nbr_current[0]].choices:
    for answer in satisfaction_survey.questions[question_nbr].choices:
        answers.append((
            answer, f"{idx}_{answer.replace(' ', '-')}"))
        idx = idx + 1

    # render the questions page. Note that within questions.html, the question number
    #  presented to the respondent is question_nbr_current[0] + 1. The respondent sees
    #  1 as the first question, not 0.
    return render_template("questions.html", survey_title=title,
                           question_nbr=question_nbr,
                           question_nbr_max=(
                               len(satisfaction_survey.questions)),
                           question_text=question_text,
                           question_answers=answers,
                           debug=DEBUG_SESSION)


@app.route("/answer", methods=["POST"])
def survey_answer():
    """ Handles the answer to a survey question. 

    """

    # question_nbr_current[0] holds the number of the current question.
    # radio box choices are named q-#-choices where # is the question
    #  number.
    l_responses = session[SURVEY_SESSION]
    question_nbr = len(l_responses)

    # answer = request.form[f'q-{question_nbr_current[0]}-choices']
    answer = request.form[f'q-{question_nbr}-choices']

    # responses.append(answer)

    l_responses.append(answer)
    session[SURVEY_SESSION] = l_responses

    # # advance to the next question number.
    # question_nbr_current[0] = question_nbr_current[0] + 1

    # Is there another question?
    # if (question_nbr_current[0] < len(satisfaction_survey.questions)):
    if (len(l_responses) < len(satisfaction_survey.questions)):
        return redirect("/questions")
        # return render_template("answer.html", survey_title=title,
        #                     question_nbr=question_nbr_current[0],
        #                     question_answer="temp answer")
    else:
        return redirect("/thankyou")


@app.route("/thankyou")
def survey_thankyou():
    """ Handles the thank you page for the survey. """

    # is this legitimate? Was the survey completed?
    l_responses = session[SURVEY_SESSION]
    question_nbr = get_curr_question_nbr()
    if (len(l_responses) == len(satisfaction_survey.questions)):
        questions_answers = "Your responses:<br>"
        idx = 0
        for question in satisfaction_survey.questions:
            questions_answers = f"{questions_answers}{idx + 1}. {question.question}  <strong>{l_responses[idx]}</strong><br><br>"
            idx = idx + 1

        return render_template("thank_you.html", survey_title=title,
                               q_and_a=questions_answers,
                               debug=DEBUG_SESSION)
    else:
        # restart the survey
        # A lot can happen here. The respondent can also get reset to the next natural question. But for now,
        #  reset the survey.
        survey_reset_controls()
        flash("Some survey shenanigans were detected. Your survey was reset.", "warning")
        return redirect("/")


@app.route("/reset")
def survey_reset():
    """ function to reset the survey so there is no need to stop the server for testing """

    survey_reset_controls()
    # question_nbr_current[0] = 0

    # # responses list to hold the answers to the survey questions.
    # responses.clear()

    return redirect("/")
