import {asyncGet, asyncPut} from './../base.js'
import {renderQuestions} from './render.js'
import {sendVotes} from './core.js'
import {activeSelects, disableSelects} from './support.js'
import {activeChangeVoteImage} from '../../asks/changeVoteImage.js'

document.addEventListener('DOMContentLoaded', getQuestionsAndRender)
let currentRoomCode = document.querySelector('input#code').value    


export function vote(questionId, action) {
    let url = `http://localhost:8000/api/${currentRoomCode}/lista-melhores-perguntas/${questionId}`
    let key = document.querySelector('input#user_key').value
    let bodyHttp = {"process": action, "key": key}
    asyncPut(url, bodyHttp)
}


async function getQuestionsAndRender() {
    let url = `http://localhost:8000/api/${currentRoomCode}/lista-melhores-perguntas`
    disableSelects()
    let questions = await asyncGet(url)
    renderQuestions(questions)
    activeSelects()
    activeChangeVoteImage()
    let voteButtons = document.querySelectorAll('.edit-question button.action')
    voteButtons.forEach((button) => {
        button.addEventListener('click', sendVotes)
    })
}