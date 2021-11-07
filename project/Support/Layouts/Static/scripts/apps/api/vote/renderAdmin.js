import {getThemesById, getHoraryByString, shuffle, In} from './support.js'

export function renderQuestions(questions){
    renderQuestionsForVote(questions)
    renderQuestionsForRanking(questions)
}


function renderQuestionsForVote(questions){
    let renderArea = document.querySelector('.questions-for-vote')
    let themes = getThemesById()
    let themeCounter = {}
    let savedQuestions = localStorage.getItem('savedQuestions') === null ? [] : JSON.parse(localStorage.getItem('savedQuestions'))
    let dataMyQuestions = localStorage.getItem('myQuestions') === null ? [] : JSON.parse(localStorage.getItem('myQuestions'))  
    let myQuestions = []  
    dataMyQuestions.filter((questionsData) => (myQuestions.push(questionsData[0])))

    Object.values(themes).forEach((theme) => {
        themeCounter[theme] = 0
    })
    let shuffleQuestions = shuffle(questions)
    shuffleQuestions.forEach((question, index) => {
        if ((In(question.text, savedQuestions))||(In(question.text, myQuestions))){ return }
        let theme = themes[question.theme]
        if (themeCounter[theme] > 20){return}
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
                    <button class="icon-text action" questionId="${question.id}" action="mark" index="${index}" page="1">
                        <span>Marcar como respondida</span>
                        <img src="/static/assets/global/check.svg" alt="check">
                    </button>
                    <button class="icon-text action" questionId="${question.id}" action="down" index="${index}" page="1">
                        <span>DOWN</span>
                        <img src="/static/assets/apps/asks/vote/deslike.png" alt="deslike">
                    </button>
                    <button class="icon-text action" questionId="${question.id}" action="up" index="${index}" page="1">
                        <span>UP</span>
                        <img src="/static/assets/apps/asks/vote/like.png" alt="like">
                    </button>
                    <button class="icon-text action seta-last" questionId="${question.id}" action="pass" index="${index}" page="1">
                        <span>PASS</span>
                        <img src="/static/assets/apps/asks/vote/seta.png" alt="seta">
                    </button>
                </div>
            </div>
        </div>
        `        
    })
    Object.keys(themeCounter).forEach((theme) => {
        if(themeCounter[theme] === 0 && theme !== 'Selecionar tema'){
            let noneQuestionsImg = document.createElement('div')
            noneQuestionsImg.setAttribute('theme', `${theme}`)
            noneQuestionsImg.setAttribute('class', 'my-questions qr')       
            noneQuestionsImg.innerHTML = '<img src="/static/assets/global/questions-representation.png" alt="questions-representation" class="questions-representation">'     
            renderArea.append(noneQuestionsImg)            
        }
    })
}



function renderQuestionsForRanking(questions){
    let renderArea = document.querySelector('.questions-for-ranking')
    let themes = getThemesById()
    let themeCounter = {}
    Object.values(themes).forEach((theme) => {
        themeCounter[theme] = 0
    })
    questions.forEach((question, index) => {
        let theme = themes[question.theme]
        if (themeCounter[theme] > 20){return}
        themeCounter[theme] += 1
        let visibility = themeCounter[theme] > 5 ? ' invisible': ''
        renderArea.innerHTML += `
        <div class="question my-questions${visibility}" theme="${theme}" index="${index + questions.length}">
        <p class="question-text">${question.text}</p>
        <div class="question-footer">
            <div class="clock icon-text">
                <div class="username">
                    <img src="/static/assets/apps/asks/global/user.svg" alt="user-img">
                    <span>${question.creator}</span>
                </div>
            </div>
            <ul class="edit-question icon-text">
            <button class="icon-text action" questionId="${question.id}" action="mark" index="${index + questions.length}" page="2">
                <span>Marcar como respondida</span>
                <img src="/static/assets/global/check.svg" alt="check">
            </button>            
                <li class="icon-text">
                    <span>${question.down_votes}</span>
                    <img src="/static/assets/apps/asks/vote/deslike.png" alt="deslike">
                </li>
                <li class="icon-text">
                    <span>${question.up_votes}</span>
                    <img src="/static/assets/apps/asks/vote/like.png" alt="like">
                </li>
            </ul>
            </form>
        </div>
    </div>
        `        
    })
    Object.keys(themeCounter).forEach((theme) => {
        if(themeCounter[theme] === 0 && theme !== 'Selecionar tema'){
            let noneQuestionsImg = document.createElement('div')
            noneQuestionsImg.setAttribute('theme', `${theme}`)
            noneQuestionsImg.setAttribute('class', 'my-questions qr')       
            noneQuestionsImg.innerHTML = '<img src="/static/assets/global/questions-representation.png" alt="questions-representation" class="questions-representation">'     
            renderArea.append(noneQuestionsImg)            
        }
    })    
}