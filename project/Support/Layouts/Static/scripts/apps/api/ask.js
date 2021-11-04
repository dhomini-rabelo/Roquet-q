import {asyncPost} from './base.js'
//* MAIN Web Element
let sendButton = document.querySelector('button.send')

//* EVENT

sendButton.addEventListener('click', registerQuestion)

//* Main Functions


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
        }else{
            if ('text' in process['errors']) {
                showMessage(process['errors']['text'].replace('Este campo', 'Pergunta'), 'error')
            } else if ('theme' in process['errors']) {
                showMessage(process['errors']['theme'], 'error')
            } else if ('creator' in process['errors'].replace('Este campo', 'Tema')) {
                showMessage(process['errors']['creator'].replace('Este campo', 'Username'), 'error')
            }
        }
    } else {
        showMessage(validation, 'warning')
    }
    sendButton.disabled = false
}

//  criar animções e exibir respostas com estilo, salvar no storage e na hora de validar se o texto já existe


async function createQuestions(creator, text, themeId) {
    let url = 'http://localhost:8000/api/123465/criar-perguntas'
    let body = {
        'creator': creator,
        'text': text,
        'theme': themeId
    }
    let response = await asyncPost(url, body)
    response = JSON.parse(response)
    return response
}


function validateQuestion(text, theme_id){
    if (text.length === 0){
        return 'Envie uma pergunta'
    } else if (theme_id === 0){
        return 'Selecione um tema'
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


    let getImg = {'success': 'yes', 'error': 'no', 'warning': 'alert'}
    
    
    messageForUser.style.display = 'block'
    imgMessage.setAttribute('src', `/static/admin/img/icon-${getImg[status]}.svg`)
    textMessage.innerHTML = message


    setTimeout(() => {
        messageForUser.style.display = 'none'
        borderTextArea.classList.remove(`${status}-send-question`)
    }, 3500)
}

