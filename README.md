# sb_19-03-10_Flask_Tools_Exercise

## Flask Survey  

## Assignment Details
#### ASSIGNMENT INVOLVED ####:
- Build a survey application that asks the visitor to answer questions. The visitor automatically advances through the survey as they answer the questions. A thank you page appears when there are no more questions.


### SURVEY FLOW ###
The site root page, **/** serves as the Welcome page. The only survey available for now is the Customer Satisfaction Survey. The survey name, Customer Satisfaction Survey, appears on the page as well as the page title. The directions for completing the Customer Satisfaction Survey are from the survey declaration in surveys.py. Pressing Start serves up the first survey question.

The **/questions** route displays the survey question and the choices to the visitor. The question number and total number of questions appear with the question so the visitor can guage their progress. The route does NOT include the question number, that is, you cannot change the route to /question/4 to get to the fourth question. "Answering the question should fire off a POST request to /answer with the answer the user selected" was taken quite literally and there is no Next button. A click on an answer advances to the next question (actually to the answer processor which redirects to the next question).

When the final question is answered, the visitor is receives a thank you page accomplished by a redirect that exists on the question page. The thank you page includes the questions and responses provided by the visitor. The questions and answers are filtered through **|safe** to ensure that embedded html is not changed to text.

The **/thankyou** route includes logic to ensure the survey was completed (next question counter equals total number of questions and number of responses equals total number of questions) before displaying the thank you message. The visitor is automatically redirected to the welcome page to restart the survey when the checks indicate an incomplete survey. 

Debugging tool declarations remain in app.py and are commented out. A **/reset** route was added to provides a means of resetting the survey control structures without having to recycle the server. 


**DIFFICULTIES**
I did not realize that global primitives in Python cannot get changed in a function. Unfortunately, it toooook toooooo long to realize this. I thought for sure that was something incorrect with function code and it was odd that it was getting hung up when used in an f-string. 


**ENHANCEMENTS**
- Right from the start, the server logic was set up NOT to use the question number value in the url. That is too easy for the visitor to manipulate and it was quickly dropped . . and then drama because I could not get the counter to advance. The other caveate, for now at least, is the realization that the counter and responses are set up for a single visitor and the assignment directions do indicate that 'sessions' will get impletmented so I hope I am in a good place to retrofit the code to work with sessions.
- Current question number and total number of questions appear on each question.
- light JavaScript added to submit the answer when the visitor clicks on an answer.
- Thank You page includes the questions and the answers provided by the site visitor.
- **/reset** route to reset the survey control variables. 


**TIMING**:
- 9.6 hours (high end for assignment was 8 hours). Again, disappointed because at least 1 - 2 hours were spent trying to figure out why globally declared question_nbr_current was getting rejected when used in an f-string or when altered.  

