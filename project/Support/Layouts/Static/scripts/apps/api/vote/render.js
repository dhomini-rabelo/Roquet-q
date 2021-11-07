import {getThemesById, getHoraryByString, shuffle, In} from './support.js'

export function renderQuestions(questions){
    renderQuestionsForVote(questions)
}


function renderQuestionsForVote(questions){
    let renderArea = document.querySelector('.questions-for-vote')
    let themes = getThemesById()
    let themeCounter = {}
    let savedQuestions = localStorage.getItem('savedQuestions') === null ? [] : JSON.parse(localStorage.getItem('savedQuestions'))
    Object.values(themes).forEach((theme) => {
        themeCounter[theme] = 0
    })
    let shuffleQuestions = shuffle(questions)
    shuffleQuestions.forEach((question, index) => {
        if (In(question.text, savedQuestions)){ return }
        let theme = themes[question.theme]
        themeCounter[theme] += 1
        let visibility = themeCounter[theme] > 5 ? ' invisible': '' 
        renderArea.innerHTML += `
        <div class="question my-questions${visibility}" theme="${theme}" index="${index}">
            <p class="question-text">${question.text}</p>
            <div class="question-footer">
                <div class="clock icon-text">
                    <img src="/static/assets/apps/asks/global/clock.png" alt="clock-img">
                    <span>${getHoraryByString(question.creation)}</span>
                </div>
                <div class="edit-question icon-text">
                    <button class="icon-text action" questionId="${question.id}" action="down" index="${index}">
                        <span>DOWN</span>
                        <img src="/static/assets/apps/asks/vote/deslike.png" alt="deslike">
                    </button>
                    <button class="icon-text action" questionId="${question.id}" action="up" index="${index}">
                        <span>UP</span>
                        <img src="/static/assets/apps/asks/vote/like.png" alt="like">
                    </button>
                    <button class="icon-text action seta-last" questionId="${question.id}" action="pass" index="${index}">
                        <span>PASS</span>
                        <img src="/static/assets/apps/asks/vote/seta.png" alt="seta">
                    </button>
                </div>
            </div>
        </div>
        `        
    })
}