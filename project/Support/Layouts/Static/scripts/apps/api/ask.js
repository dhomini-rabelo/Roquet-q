import {asyncPost} from './base.js'
//* MAIN Web Element
let sendButton = document.querySelector('button.send')


//* EVENT

sendButton.addEventListener('click', registerQuestion)
document.addEventListener('DOMContentLoaded', renderQuestions)



//* Main Functions

function renderQuestions() {
    let myQuestions = localStorage.getItem('myQuestions')
    if (myQuestions === null){
        let questions = []
        localStorage.setItem('myQuestions', JSON.stringify(questions))
    }else{
        let questions = clearQuestions(JSON.parse(myQuestions))
        localStorage.setItem('myQuestions', JSON.stringify(questions))
        renderApp1(questions)
        renderApp2(questions)
        let deleteButtons = document.querySelectorAll('form')
        deleteButtons.forEach((button) => {
            button.addEventListener('submit', deleteQuestion)
        })        
    }
}


function deleteQuestion(event){
    let form = event.currentTarget
    let button = form.children[5].children[0]
    button.disabled = true
    let index = Number.parseInt(button.getAttribute('index'))
    let myQuestions = JSON.parse(localStorage.getItem('myQuestions'))
    let questions = clearQuestions(myQuestions)
    questions.splice(index, 1)
    localStorage.setItem('myQuestions', JSON.stringify(questions))
}


function clearQuestions(questions){
    let optionsTheme = document.querySelectorAll('select.select-main option')
    let activeThemes = []
    optionsTheme.forEach((option) => (activeThemes.push(option.innerHTML)))
    let activeQuestions = questions.filter((questionsData) => (In(questionsData[1], activeThemes)))
    return activeQuestions
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

function getHorary(){
    let now = new Date()
    let hours = now.getHours()
    let minutes = now.getMinutes()

    if (hours>=10 && minutes>=10){
        return `${hours}:${minutes}`
    }else if (hours>=10 && minutes<10){
        return `${hours}:0${minutes}`
    }else if (hours<10 && minutes>=10){
        return `0${hours}:${minutes}`
    }else if (hours<10 && minutes<10){
        return `0${hours}:0${minutes}`
    }
}



function addQuestionToMyQuestions(newQuestion, themeId){
    let myQuestionsSaved = JSON.parse(localStorage.getItem('myQuestions'))
    let themeName = document.querySelector(`option[value="${themeId}"]`).innerHTML
    let horary = getHorary()
    myQuestionsSaved.unshift([newQuestion, themeName, horary])
    let newSave = myQuestionsSaved
    localStorage.setItem('myQuestions', JSON.stringify(newSave))
}



async function registerQuestion() {
    sendButton.disabled = true
    let creator = document.querySelector('#id_username').value
    let text = document.querySelector('#id_question').value
    let themeId = Number.parseInt(document.querySelector('#id_theme').value)
    let validation = validateQuestion(text, themeId)
    if (validation === 'valid'){
        sendButton.innerHTML = '<div class="send-loader" style="display: block;"></div>'
        let process = await createQuestions(creator, text, themeId)
        sendButton.innerHTML = 'Enviar<div class="send-loader" style="display: none;"></div>'
        if (process['status'] === 'valid') {
            showMessage('Pergunta enviada com sucesso', 'success')
            addQuestionToMyQuestions(text, themeId)
            renderQuestions()
            let textAreaUsed = document.querySelector('textarea')
            textAreaUsed.value = ''
        }else{
            if ('text' in process['errors']) {
                showMessage(process['errors']['text'].replace('Este campo', 'Pergunta'), 'error')
            } else if ('theme' in process['errors']) {
                let messageForError = process['errors']['theme'].replace('Este campo', 'Tema')
                if (messageForError === 'Tema não foi encontrado'){
                    showMessage('Tema inexistente ou inativo', 'error')
                } else{
                    showMessage(process['errors']['theme'].replace('Este campo', 'Tema'), 'error')
                }
            } else if ('creator' in process['errors'].replace('Este campo', 'Tema')) {
                showMessage(process['errors']['creator'].replace('Este campo', 'Username'), 'error')
            }
        }
    } else {
        showMessage(validation, 'warning')
    }
    sendButton.disabled = false
}

//  salvar no storage e na hora de validar se o texto já existe


async function createQuestions(creator, text, themeId) {
    let url = 'http://localhost:8000/api/123465/criar-perguntas'
    let body = {
        'creator': creator,
        'text': text,
        'theme': themeId
    }
    let response = await asyncPost(url, body)
    return response
}

function In(obj, array) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] === obj) {
            return true
        }
    }
    return false
}


function validateQuestion(text, theme_id){
    let myQuestionsCreated = JSON.parse(localStorage.getItem('myQuestions'))
    let myQuestionsCreatedOnlyText = []
    myQuestionsCreated.forEach((questionData) => {myQuestionsCreatedOnlyText.push(questionData[0])})
    if (text.length === 0){
        return 'Envie uma pergunta'
    } else if (theme_id === 0){
        return 'Selecione um tema'
    } else if (In(text, myQuestionsCreatedOnlyText)) {
        return 'Você já fez está pergunta'
    } else {
        return 'valid'
    }
}


function showMessage(message, status){
    let borderTextArea = document.querySelector('div.question.text-area')
    borderTextArea.classList.add(`${status}-send-question`)


    let messageForUser = document.querySelector('div.message')
    let imgMessage = document.querySelector('div.message > img')
    let textMessage = document.querySelector('div.message > span')
    let messageSpace = document.querySelector('.sheets')


    let getImg = {'success': 'yes', 'error': 'no', 'warning': 'alert'}
    
    messageSpace.style.display = 'none'
    messageForUser.style.display = 'block'
    imgMessage.setAttribute('src', `/static/admin/img/icon-${getImg[status]}.svg`)
    textMessage.innerHTML = message

    setTimeout(() => {
        clearMessage(message)
    }, 3000)
}

function clearMessage(message){
    let textSpanMessage = document.querySelector('div.message > span')
    let borderTextAreaForClear = document.querySelector('div.question.text-area')
    let messageSpace = document.querySelector('.sheets')
    let checkMessage = document.querySelector('div.message')
    if (textSpanMessage.innerHTML === message) {
        checkMessage.style.display = 'none'
        messageSpace.style.display = 'block'
        borderTextAreaForClear.setAttribute('class', 'question text-area')
    }
}

