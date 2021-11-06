import {clearQuestions, deleteQuestion} from './core.js'

export function renderQuestions() {
    let myQuestions = localStorage.getItem('myQuestions')
    if (myQuestions === null){
        let questions = []
        localStorage.setItem('myQuestions', JSON.stringify(questions))
    }else{
        let questions = clearQuestions(JSON.parse(myQuestions))
        localStorage.setItem('myQuestions', JSON.stringify(questions))
        renderApp1(questions)
        renderApp2(questions)
        let forms = document.querySelectorAll('form')
        forms.forEach((button) => {
            button.addEventListener('submit', deleteQuestion)
        })
    }
}

function renderApp1(questions) {
    let app1 = document.querySelector('div.questions-saved')
    let myUsername = document.querySelector('#id_username').value
    let csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value    
    if (questions.length === 0){
        app1.innerHTML = '<img src="/static/assets/global/questions-representation.png" alt="questions-representation" class="questions-representation">'
        return
    }
    app1.innerHTML = ''
    if(questions.length > 3){
        questions = questions.slice(0,3)
    }
    questions.forEach((questionData, index) => {
        let savedQuestion = document.createElement('div')
        savedQuestion.setAttribute('theme', `${questionData[1]}`)
        savedQuestion.setAttribute('class', 'question my-questions')
        savedQuestion.innerHTML = `
        <p class="question-text">
            ${questionData[0]}
        </p>
        <div class="question-footer">
            <div class="clock icon-text">
                <img src="/static/assets/apps/asks/global/clock.png" alt="clock-img">
                <span>${questionData[2]}</span>
            </div>
            <form method="POST">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
            <input type="hidden" name="creator" id="id_creator" value="${myUsername}">
            <input type="hidden" name="text" id="id_text" value="${questionData[0]}">
            <input type="hidden" name="theme" id="id_theme" value="${questionData[1]}">
            <input type="hidden" name="page" id="id_page" value="1">
            <div class="edit-question icon-text">
                <button type="submit" class="icon-text delete-question" index="${index}">
                    <img src="/static/assets/apps/asks/global/trash.svg" alt="trash-img">
                    <span>Excluir</span>
                </button>
            </div>
            </form>
        </div>
    `
        app1.append(savedQuestion)
    })
}

function renderApp2(questions) {
    let app2 = document.querySelector('div.all-my-questions')
    let myUsername = document.querySelector('#id_username').value
    let csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    app2.innerHTML = ''
    questions.forEach((questionData, index) => {
        let savedQuestion = document.createElement('div')
        savedQuestion.setAttribute('theme', `${questionData[1]}`)
        savedQuestion.setAttribute('class', 'question my-questions')
        savedQuestion.innerHTML = `
            <p class="question-text">
                ${questionData[0]}
            </p>
            <div class="question-footer">
                <div class="clock icon-text">
                    <img src="/static/assets/apps/asks/global/clock.png" alt="clock-img">
                    <span>${questionData[2]}</span>
                </div>
                <form method="POST">
                <input type="hidden" name="csrfmiddlewaretoken" value="${csrf_token}">
                <input type="hidden" name="creator" id="id_creator" value="${myUsername}">
                <input type="hidden" name="text" id="id_text" value="${questionData[0]}">
                <input type="hidden" name="theme" id="id_theme" value="${questionData[1]}">
                <input type="hidden" name="page" id="id_page" value="2">
                <div class="edit-question icon-text">
                    <button type="submit" class="icon-text delete-question" index="${index}">
                        <img src="/static/assets/apps/asks/global/trash.svg" alt="trash-img">
                        <span>Excluir</span>
                    </button>
                </div>
                </form>
            </div>
        `
        app2.append(savedQuestion)
    })
    checkNoneThemes()
}

function checkNoneThemes() {
    let optionThemes = document.querySelectorAll('select.select-main option')
    optionThemes.forEach((option) => {
        let theme = option.innerHTML
        let questionsTheme = document.querySelectorAll(`div.question.my-questions[theme="${theme}"]`)
        if (questionsTheme.length === 0 && theme !== "Selecionar tema"){
            let myApp2 = document.querySelector('div.all-my-questions')
            let noneQuestionsImg = document.createElement('div')
            noneQuestionsImg.setAttribute('theme', `${theme}`)
            noneQuestionsImg.setAttribute('class', 'my-questions qr')       
            noneQuestionsImg.innerHTML = '<img src="/static/assets/global/questions-representation.png" alt="questions-representation" class="questions-representation">'     
            myApp2.append(noneQuestionsImg)
        }
    })

}