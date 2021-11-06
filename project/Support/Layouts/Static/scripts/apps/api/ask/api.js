import {asyncPost} from './../base.js'
import {renderQuestions} from './render.js'
import {addQuestionToMyQuestions} from './core.js'
import {showMessage} from './feedback.js'
import {validateQuestion} from './validator.js'

let sendButton = document.querySelector('button.send')


sendButton.addEventListener('click', registerQuestion)
document.addEventListener('DOMContentLoaded', renderQuestions)


async function createQuestions(creator, text, themeId) {
    let currentRoomCode = document.querySelector('input#code').value    
    let url = `http://localhost:8000/api/${currentRoomCode}/criar-perguntas`
    let body = {
        'creator': creator,
        'text': text,
        'theme': themeId
    }
    let response = await asyncPost(url, body)
    return response
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