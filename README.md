# sb_19-04-12_Flask_Session_Exercise

## Flask Survey enhanced with Session Storage and Cookies 

## Assignment Details
Build a survey application that asks the visitor to answer questions. The visitor automatically advances through the survey as they answer the questions. A thank you page appears when there are no more questions. The assignment built on the flask server application developed in the [Flask Tooks Exercise](https://github.com/JimGeist/sb_19-03-10_Flask_Tools_Exercise "Build a survey application that asks the visitor to answer survey questions").


### SURVEY FLOW 
The site root page, **/** serves as the Welcome page. The only survey available for now is the Customer Satisfaction Survey. The survey name, Customer Satisfaction Survey, appears on the page as well as the page title. The directions for completing the Customer Satisfaction Survey are from the survey declaration in surveys.py. Pressing Start makes a POST call to **/session** which sets up session storage and depending on the number of answers in session storage, either serves up the appropriate question or renders the thank you page.

The **/questions** route displays the survey question and the choices to the visitor. The question number and total number of questions appear with the question so the visitor can guage their progress. The route does NOT include the question number, that is, you cannot change the route to /question/4 to get to the fourth question. "Answering the question should fire off a POST request to /answer with the answer the user selected" was taken quite literally and there is no 'Next' button. A click on an answer advances to an answer processor which either redirects back to **/questions** or to **/thankyou** when all questions were answered. A redirect to the **/thankyou** route does exist in the **/questions** route to catch the case where the survey is completed, but the visitor changes the url to /questions

The **/thankyou** route thanks the vistor for taking the survey. The answer processor redirects to the thank you page when all survey questions were answered. The thank you page includes the questions and responses provided by the visitor. The questions and answers are filtered through **|safe** to ensure that embedded html elements are not changed to text.

The **/thankyou** route includes logic to ensure the survey was completed (number of responses equals total number of questions) before displaying the thank you message. The visitor is automatically redirected the questions page when the check indicates that all questions were not answered (example - changing /questions to /thankyou when questions still remain). 

Debugging tool declarations remain in app.py and are commented out. A **/reset** route was added to provides a means of resetting the survey control structures without having to recycle the server. 

Movement through the survey is controlled the survey answers that are saved in the session. 


### ENHANCEMENTS 
- Current question number and total number of questions appear on each question.
- Light JavaScript added to submit the answer when the visitor clicks on an answer.
- We are in the midst of a pandamnit and toilet paper, not frisbees is a particulary hottly hoarded commodity (at least it was when the pandamnit started).
- Thank You page includes the questions and the answers provided by the site visitor.
- **/reset** route to reset the session and cookie storage. 
- Survey uses session storage to hold the question responses and the flag that controls the visibility, and a cookie that holds the responses, last active date, and survey title.
- Helpful messaging appears on the welcome page that informs the visitor if they completed the survey or if the survey was started but never completed. The button on the welcome page coupled with the message lets the visitor know how the survey will flow.
- Debugging capabilities while survey is in progress. This was where I should have stopped . . but didn't!
  - adding, **?debug** on the welcome page sets debugging to true for the entire survey session. The cookie and session storage values are added to the bottom of each survey page. 
  - when debugging is not currently active, the ability to add cookie and session storage values to the bottom of the a non-welcome is possible again via **?debug**. The cookie and session details are added just for the active page (**?debug** on the welcome page turns debugging on for survey session as described above).


### DIFFICULTIES 
Got lost overdoing things, making changes, then going back. The debugging pieces consumed a lot of time getting them to work correctly and retrofitting was required since a cookie was used to determine the starting point.


### TIMING 
- 4.3 hours (high end for assignment was 8 hours). And then I ruined it by adding the cookie and destroyed the timeline with debugging statements. Total time with cookie and debugging pieces brings this one in at 14 hours {sigh}.

