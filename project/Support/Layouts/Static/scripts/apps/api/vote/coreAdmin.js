import {vote} from "./apiAdmin.js"

export function sendVotes(event) {
    let button = event.currentTarget
    let questionId = button.getAttribute('questionId')
    let action = button.getAttribute('action')
    let index = button.getAttribute('index')
    let page = button.getAttribute('page')
    updateQuestion(index, page)
    setTimeout(() => {
        vote(questionId, action)
    }, 3500)
}

function updateQuestion(index, page){
    let question = document.querySelector(`div.question.my-questions[index="${index}"]`)
    let questionText = question.children[0]
    addQuestionInSavedQuestions(questionText.innerHTML)
    question.remove()
    let local = page === '1' ? 'questions-for-vote' : 'questions-for-ranking'

    let questionsWithEqualTheme = document.querySelectorAll(`.${local} div.question.my-questions.invisible.visible`)


    try{
        questionsWithEqualTheme[0].setAttribute('class', ' question my-questions visible')
    }catch(e){
    }
}

function addQuestionInSavedQuestions(question){
    let savedQuestions = localStorage.getItem('savedQuestions')
    if (savedQuestions === null){
        let array = [question]
        localStorage.setItem('savedQuestions', JSON.stringify(array))
    }else{
        let array = JSON.parse(savedQuestions)
        array.push(question)
        localStorage.setItem('savedQuestions', JSON.stringify(array))
    }
}
