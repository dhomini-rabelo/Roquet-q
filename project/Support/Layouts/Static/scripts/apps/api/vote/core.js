import {vote} from "./api.js"

export function sendVotes(event) {
    let button = event.currentTarget
    let questionId = button.getAttribute('questionId')
    let action = button.getAttribute('action')
    let index = button.getAttribute('index')
    updateQuestion(index)
    setTimeout(() => {
        vote(questionId, action)
    }, 2000)
}

function updateQuestion(index){
    let question = document.querySelector(`div.question.my-questions[index="${index}"]`)
    let theme = question.getAttribute('theme')
    let questionText = question.children[0]
    addQuestionInSavedQuestions(questionText.innerHTML)
    question.remove()
    let questionsWithEqualTheme = document.querySelectorAll(`.questions-for-vote div.question.my-questions.invisible.visible`)
    try{
        questionsWithEqualTheme[0].setAttribute('class', ' question my-questions visible')
    }catch(e){
        let lastQuestions = document.querySelectorAll(`.questions-for-vote div.question.my-questions.visible`)
        if (lastQuestions.length === 0){
            let renderLocal = document.querySelector('.questions-for-vote')
            let alert = document.createElement('div')
            alert.setAttribute('class', ' question my-questions visible')
            alert.setAttribute('theme', `${theme}`)
            alert.innerHTML = 'Recarregue a página para mais perguntas'
            renderLocal.append(alert)
        }
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


