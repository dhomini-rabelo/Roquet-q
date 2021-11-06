import {getHorary, In} from './support.js'

export function addQuestionToMyQuestions(newQuestion, themeId){
    let myQuestionsSaved = JSON.parse(localStorage.getItem('myQuestions'))
    let themeName = document.querySelector(`option[value="${themeId}"]`).innerHTML
    let horary = getHorary()
    myQuestionsSaved.unshift([newQuestion, themeName, horary])
    let newSave = myQuestionsSaved
    localStorage.setItem('myQuestions', JSON.stringify(newSave))
}

export function deleteQuestion(event){
    let form = event.currentTarget
    let button = form.children[5].children[0]
    button.disabled = true
    let index = Number.parseInt(button.getAttribute('index'))
    let myQuestions = JSON.parse(localStorage.getItem('myQuestions'))
    let questions = clearQuestions(myQuestions)
    questions.splice(index, 1)
    localStorage.setItem('myQuestions', JSON.stringify(questions))
}

export function clearQuestions(questions){
    let optionsTheme = document.querySelectorAll('select.select-main option')
    let activeThemes = []
    optionsTheme.forEach((option) => (activeThemes.push(option.innerHTML)))
    let activeQuestions = questions.filter((questionsData) => (In(questionsData[1], activeThemes)))
    return activeQuestions
}