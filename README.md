# sb_19-03-10_Flask_Tools_Exercise

## Flask Survey  

## Assignment Details
Build a survey application that asks the visitor to answer questions. The visitor automatically advances through the survey as they answer the questions. A thank you page appears when there are no more questions.


### SURVEY FLOW ###
The site root page, **/** serves as the Welcome page. The only survey available for now is the Customer Satisfaction Survey. The survey name, Customer Satisfaction Survey, appears on the page as well as the page title. The directions for completing the Customer Satisfaction Survey are from the survey declaration in surveys.py. Pressing Start makes a POST call to **/session** which sets up session storage and depending on the number of answers in session storage, either serves up the appropriate question or renders the thank you page.

The **/questions** route displays the survey question and the choices to the visitor. The question number and total number of questions appear with the question so the visitor can guage their progress. The route does NOT include the question number, that is, you cannot change the route to /question/4 to get to the fourth question. "Answering the question should fire off a POST request to /answer with the answer the user selected" was taken quite literally and there is no Next button. A click on an answer advances to the next question (actually to the answer processor which redirects to the next question).

When the final question is answered, the visitor is receives a thank you page accomplished by a redirect that exists on the question page. The thank you page includes the questions and responses provided by the visitor. The questions and answers are filtered through **|safe** to ensure that embedded html elements are not changed to text.

The **/thankyou** route includes logic to ensure the survey was completed (number of responses equals total number of questions) before displaying the thank you message. The visitor is automatically redirected to the welcome page to restart the survey when the checks indicate an incomplete survey (example - changing /questions to /thankyou when questions still remain). 

Debugging tool declarations remain in app.py and are commented out. A **/reset** route was added to provides a means of resetting the survey control structures without having to recycle the server. 

Movement through the survey is controlled the survey answers that are saved in the session. 


### ENHANCEMENTS ###
- Current question number and total number of questions appear on each question.
- Light JavaScript added to submit the answer when the visitor clicks on an answer.
- Thank You page includes the questions and the answers provided by the site visitor.
- **/reset** route to reset the survey control variables. 


### DIFFICULTIES ###
Not sure why the assignment suggesting changing the Start button to a POST request. Is it because we are establishing / altering the session storage.


### TIMING ###
- 4.3 hours (high end for assignment was 8 hours). 

