import {asyncGet} from './../base.js'
import {renderAnsweredQuestions, renderAllQuestions} from './render.js'
import {activeSelects, disableSelects} from './support.js'

document.addEventListener('DOMContentLoaded', getQuestionsAndRender)
let currentRoomCode = document.querySelector('input#code').value    


async function getAllQuestions() {
    let url = `http://localhost:8000/api/${currentRoomCode}/lista-perguntas-finalizadas`
    let allQuestions = await asyncGet(url)
    return allQuestions
}

async function getAnsweredQuestions() {
    let url = `http://localhost:8000/api/${currentRoomCode}/lista-perguntas-respondidas-finalizadas`
    let questions = await asyncGet(url)
    return questions
}


async function getQuestionsAndRender() {
    disableSelects()
    let allQuestionsOfFinalizedTheme = await getAllQuestions()
    let allAnsweredQuestionsOfFinalizedTheme = await getAnsweredQuestions()
    renderAnsweredQuestions(allAnsweredQuestionsOfFinalizedTheme)
    renderAllQuestions(allQuestionsOfFinalizedTheme)
    activeSelects()
}