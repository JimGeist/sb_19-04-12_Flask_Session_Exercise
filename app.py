from flask import Flask, request, render_template, redirect, flash, session, make_response, jsonify
from datetime import datetime

# # debug toolbar
# from flask_debugtoolbar import DebugToolbarExtension

from surveys import Question, Survey, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "the password is 'password'"

# # debug toolbar
# debug = DebugToolbarExtension(app)
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

# Establish the session name for the survey. session[SURVEY_SESSION] holds the responses
#  to each question as the respondent moved through the survey.
SURVEY_SESSION = "survey_session"

# Cookie Constants
COOKIE_NAME = "Survey_CustSat"
COOKIE_DELIM = "<!>"
COOKIE_EXPIRY = 5184000  # 5,184,000 seconds (60 days) = cookie expiration date

# Debug session controls whether session details (the survey answer storage) appear on
#  the bottom of each page.
# Do not remove DEBUG_DISPLAY_SESSION. Just set it to False when no longer needed.
DEBUG_DISPLAY_SESSION = True

# survey title
title = satisfaction_survey.title


def bake_cookie(title, is_survey_complete):
    """ Creates a cookie for the survey with the latest responses.
        The cookie data consists of the survey responses, the current date,
        and whether the survey is complete. The list is converted to a string
        with <!> separating each field.
        When using this cookie, the string is converted to a list by splitting
        it at <!>, the True/False text is popped off, followed by the date
        string. The remaining bit is a string with the responses.
    """

    responses = list(session[SURVEY_SESSION])
    responses.append(str(datetime.now()))
    responses.append(str(is_survey_complete))

    return (COOKIE_DELIM).join(responses)


def get_cookie_data():
    """ function reads the cookie COOKIE_NAME and returns the following object
        with the data from the cookie:
        {
            cookie_data: cookie data string with all fields concatenated together.
            responses: [list containing the answers to each survey question]
            date_last_activity: date of last activity in 2021-02-17 22:53:57.423475 format
            completed: True / False indicator as to whether the survey was completed.
                        completed indicator is not used in code at this time.

        }

    """

    cookie_data = request.cookies.get(COOKIE_NAME, "")
    cookie_data_out = {"cookie_data_string": cookie_data}

    if (len(cookie_data) > 0):
        # we have cookie data
        try:
            responses = cookie_data.split(COOKIE_DELIM)
            cookie_data_out["completed"] = bool(responses.pop())
            cookie_data_out["date_last_activity"] = responses.pop()
            date_obj = datetime.strptime(
                cookie_data_out["date_last_activity"], "%Y-%m-%d %H:%M:%S.%f")
            cookie_data_out["responses"] = responses
        except:
            # Most likely a ValueError
            # debug needs a value because it controls whether session and cookie data appears on the
            #  page for debugging purposes
            cookie_data_out["responses"] = []
    else:
        cookie_data_out["responses"] = []
    print(
        f"get_cookie_data: cookie_data={cookie_data}\n\ncookie_data_out={cookie_data_out}", flush=True)
    return cookie_data_out


def determine_start_via_cookie():
    """ read the "Survey_CustSat cookie. The cookie is broken down into the
        previous responses, last activity date, and completion flag when
        cookie data exists.
    """

    cookie_data = get_cookie_data()
    starting_info = {"cookie_data": cookie_data["cookie_data_string"]}

    # look at the data and determine messaging.
    # 1 - 3 responses: Survey was started on dddd. Let's resume where we left off.
    #   (button is resume Survey)
    # 4 responses: Survey was completed on dddd. Click View Results to see your responses.
    #   (button is View Results)

    print(
        f"determine_start_via_cookie: cookie_data: {cookie_data}, \n ", flush=True)

    if (len(cookie_data.get("responses", [])) > 0):

        session[SURVEY_SESSION] = cookie_data["responses"]
        # date_obj = datetime.strptime("2021-02-17 22:53:57.423475",
        #     "%Y-%m-%d %H:%M:%S.%f")
        # datetime_object.strftime("%B %d, %Y at %I:%M %p")
        date_obj = datetime.strptime(
            cookie_data["date_last_activity"], "%Y-%m-%d %H:%M:%S.%f")
        date_str = date_obj.strftime("%B %d, %Y at %I:%M %p")
        if (len(cookie_data["responses"]) == 4):
            starting_info["message"] = f"Survey was completed on {date_str}. Click 'View Results' to see your responses. "
            starting_info["button_text"] = "View Results"
            starting_info["has_message"] = True
        else:
            starting_info["message"] = f"Survey was started on {date_str}. Let's resume where we left off. "
            starting_info["button_text"] = "Resume Survey"
            starting_info["has_message"] = True

    else:
        starting_info["has_message"] = False
        starting_info["button_text"] = "Start Survey"

    return starting_info

    # cookie_data = request.cookies.get(COOKIE_NAME, "")
    # starting_info = {"cookie_data": cookie_data}

    # if (len(cookie_data) > 0):
    #     # we have cookie data
    #     responses = cookie_data.split(COOKIE_DELIM)
    #     completed = responses.pop()
    #     date_last_activity = responses.pop()
    #     session[SURVEY_SESSION] = responses

    #     # look at the data and determine messaging.
    #     # 1 - 3 responses: Survey was started on dddd. Let's resume where we left off.
    #     #   (button is resume Survey)
    #     # 4 responses: Survey was completed on dddd. Click View Results to see your responses.
    #     #   (button is View Results)
    #     if (len(responses) > 0):
    #         # date_obj = datetime.strptime("2021-02-17 22:53:57.423475",
    #         #     "%Y-%m-%d %H:%M:%S.%f")
    #         # datetime_object.strftime("%B %d, %Y at %I:%M %p")
    #         date_obj = datetime.strptime(
    #             date_last_activity, "%Y-%m-%d %H:%M:%S.%f")
    #         date_str = date_obj.strftime("%B %d, %Y at %I:%M %p")
    #         if (len(responses) == 4):
    #             starting_info["message"] = f"Survey was completed on {date_str}. Click 'View Results' to see your responses. "
    #             starting_info["button_text"] = "View Results"
    #             starting_info["has_message"] = True
    #         else:
    #             starting_info["message"] = f"Survey was started on {date_str}. Let's resume where we left off. "
    #             starting_info["button_text"] = "Resume Survey"
    #             starting_info["has_message"] = True

    # else:
    #     starting_info["has_message"] = False
    #     starting_info["button_text"] = "Start Survey"

    # return starting_info


def get_question_idx():
    """ get the index for the next question based on number of saved responses """

    return len(session[SURVEY_SESSION])


@ app.route("/")
def survey_welcome():
    """ Renders a welcome page with the title of the survey, the instructions,
        and a button to start the survey.

        The button issues a post command to the /session route which sets up
        responses structure in session storage. The /session route then calls
        /questions

    """

    show_debug_info = request.args.get("debug", False)
    show_debug_info = True if (show_debug_info == "") else False

    print(f"show_debug_info: {show_debug_info}", flush=True)

    instructions = satisfaction_survey.instructions

    # retrieve the cookie, if any
    start_info = determine_start_via_cookie()
    if start_info.get("has_message", False):
        flash(start_info["message"], "okay")

    return render_template("welcome.html", survey_title=title,
                           survey_instructions=instructions,
                           button_text=start_info["button_text"],
                           debug=show_debug_info,
                           session_name=SURVEY_SESSION,
                           cookie=start_info)


@ app.route("/session", methods=["POST"])
def session_setup():
    """ Checks whether survey_responses session exists and creates
        survey_responses when survey_responses does not exist.

        Route redirects to /questions which will either start with
        question 0, start where the last session ended, or immediately
        place the visitor on the thank you page when the survey was
        completed.

    """

    try:
        responses = session[SURVEY_SESSION]

    except KeyError:
        # session does not exist for SURVEY_SESSION
        responses = []
        session[SURVEY_SESSION] = responses

    # the number of responses in session must be less than the number
    #  of questions in order to ask a question. Otherwise, the survey has
    #  already ended.
    print(f"/session: responses={responses}", flush=True)
    if (len(responses) < len(satisfaction_survey.questions)):
        return redirect("/questions")
    else:
        flash(
            f"You have already completed our {title}. Your responses are provided below.", "warning")
        return redirect("/thankyou")


@ app.route("/questions")
def survey_questions():
    """ Handles asking survey questions.

        The question to ask is based on the number of responses saved
        for the session. Two responses saved means 2 questions were
        asked and answered, next question to ask is idx 2 (since questions
        at idx 0 and idx 1 were already asked).

        The page presents the current survey question and possible
        answer choices as radio buttons.

        Answering the question (no button) generates a post
        request to /answer with the answer selected.

        Answer page will eventually redirect back to questions
        where the next question is asked.

    """

    show_debug_info = request.args.get("debug", False)
    show_debug_info = True if (show_debug_info == "on") else False

    # The survey question number to ask is determined by the number of questions
    #  answered. Function get_question_idx() returns the index of the question to
    #  ask.
    question_nbr = get_question_idx()

    try:
        question_text = satisfaction_survey.questions[question_nbr].question
    except IndexError:
        # An index error will occur when the url is manipulated and changed from
        # /thankyou to /questions. Since all questions were answered, the value returned
        # by get_question_idx() put us beyond the last question. Throw them back to the
        # thank you page.
        flash("This survey is completed. You cannot go back to the questions.", "warning")
        return redirect("/thankyou")

    # the answers for the survey question require processing. We need a value to present
    #  the choice as text on the form and as a non-space internal form value (id) for each answer.
    # Decision to handle ids in this fashion was to increase the readability of the html id tags.
    answers = []
    idx = 0
    for answer in satisfaction_survey.questions[question_nbr].choices:
        answers.append((
            answer, f"{idx}_{answer.replace(' ', '-')}"))
        idx = idx + 1

    print(
        f"/questions: session={session[SURVEY_SESSION]}", flush=True)
    cookie_data = bake_cookie(title, False)

    print(
        f"/questions: cookie_data={cookie_data},\nsession={session[SURVEY_SESSION]}", flush=True)

    # render the questions page. Note that within questions.html, the question number
    #  presented to the respondent is question_nbr + 1. The respondent sees
    #  1 as the first question, not 0.

    html = render_template("questions.html", survey_title=title,
                           question_nbr=question_nbr,
                           question_nbr_max=(
                               len(satisfaction_survey.questions)),
                           question_text=question_text,
                           question_answers=answers,
                           debug=show_debug_info,
                           session_name=SURVEY_SESSION,
                           cookie=cookie_data)

    resp_obj = make_response(html)
    resp_obj.set_cookie(COOKIE_NAME, cookie_data, COOKIE_EXPIRY)
    resp_obj.set_cookie("Survey_Flag", "True", COOKIE_EXPIRY)
    return resp_obj

    # return render_template("questions.html", survey_title=title,
    #                        question_nbr=question_nbr,
    #                        question_nbr_max=(
    #                            len(satisfaction_survey.questions)),
    #                        question_text=question_text,
    #                        question_answers=answers,
    #                        debug=DEBUG_DISPLAY_SESSION,
    #                        session_name=SURVEY_SESSION,
    #                        cookie=cookie_data)


@ app.route("/answer", methods=["POST"])
def survey_answer():
    """ Handles the answer to a survey question. """

    # The number of answers in the survey session is also the index
    #  of the question that was just asked an answered by the respondent.
    # We need to get their answer in order to save it.
    # radio button choices are named q-#-choices where # is the question
    #  number.
    responses = session[SURVEY_SESSION]
    question_nbr = len(responses)

    answer = request.form[f'q-{question_nbr}-choices']

    responses.append(answer)
    session[SURVEY_SESSION] = responses

    # Is there another question? Check the number of responses to find out.
    if (len(responses) < len(satisfaction_survey.questions)):
        return redirect("/questions")
    else:
        return redirect("/thankyou")


@ app.route("/thankyou")
def survey_thankyou():
    """ Handles the thank you page for the survey. """

    # Is this legitimate? Was the survey completed?
    responses = session[SURVEY_SESSION]
    if (len(responses) == len(satisfaction_survey.questions)):
        questions_answers = "Your responses:<br>"
        idx = 0
        for question in satisfaction_survey.questions:
            questions_answers = f"{questions_answers}{idx + 1}. {question.question}  <strong>{responses[idx]}</strong><br><br>"
            idx = idx + 1

        cookie_data = bake_cookie(title, True)

        html = render_template("thank_you.html", survey_title=title,
                               q_and_a=questions_answers,
                               debug=DEBUG_DISPLAY_SESSION,
                               session_name=SURVEY_SESSION,
                               cookie=cookie_data)

        resp_obj = make_response(html)
        resp_obj.set_cookie(COOKIE_NAME, cookie_data, COOKIE_EXPIRY)
        return resp_obj

        # return render_template("thank_you.html", survey_title=title,
        #                        q_and_a=questions_answers,
        #                        debug=DEBUG_DISPLAY_SESSION,
        #                        session_name=SURVEY_SESSION,
        #                        cookie=cookie_data)
    else:
        # restart the survey
        # A lot can happen here. The respondent can also get reset to the next natural question. But for now,
        #  reset the survey to demonstrate the use of a flash message.
        session[SURVEY_SESSION] = []
        flash("Some survey shenanigans were detected. Your survey was reset.", "warning")
        return redirect("/")


@ app.route("/reset")
def survey_reset():
    """ function to reset the survey so there is no need to stop the server for testing """

    session[SURVEY_SESSION] = []

    # clear the cookie
    html = render_template("thank_you.html", survey_title=title,
                           q_and_a="",
                           debug=False,
                           session_name=SURVEY_SESSION,
                           cookie="")

    resp_obj = make_response(html)
    resp_obj.set_cookie(COOKIE_NAME, "", COOKIE_EXPIRY)
    return resp_obj
