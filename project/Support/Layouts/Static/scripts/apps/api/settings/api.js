import {asyncGet} from './../base.js'
import {renderData} from './render.js'

document.addEventListener('DOMContentLoaded', getDataAndRender)
let currentRoomCode = document.querySelector('input#code').value   

async function getDataAndRender(){
    let url = `http://localhost:8000/api/${currentRoomCode}/dados-da-sala`
    let data = await asyncGet(url)
    renderData(data)
}