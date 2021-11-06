import {asyncGet, asyncPut} from './base.js'

let currentRoomCode = document.querySelector('input#the_code').value    



function vote(action) {
    let url = `http://localhost:8000/api/${currentRoomCode}/criar-perguntas`
    let bodyHttp = {"process": action}
    asyncPut(url, bodyHttp)
}


function getQuestions(action) {
    let url = `http://localhost:8000/api/${currentRoomCode}/criar-perguntas`
    asyncPut(url, bodyHttp)
}