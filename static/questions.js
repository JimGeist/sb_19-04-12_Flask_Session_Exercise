const formAllRadioInputs = document.getElementById('answer');

// add event listener to the todo-list div
formAllRadioInputs.addEventListener("click", function (inEvt) {

    if (inEvt.target.tagName === 'LABEL') {
        // the label was clicked on. Set the checked to true on the control element for the label.
        inEvt.target.control.checked = true;
    }

    document.getElementById("answer").submit();

});
