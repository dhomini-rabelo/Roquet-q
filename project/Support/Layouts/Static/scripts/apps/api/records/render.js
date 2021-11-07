import {getThemesById, getHoraryByString} from './support.js'

export function renderAnsweredQuestions(questions){
    let renderArea = document.querySelector('.answered-questions')
    let themes = getThemesById()
    questions.forEach((question) => {
        renderArea.innerHTML += `
        <div class="question my-questions" theme="${themes[question.theme]}">
        <p class="question-text">
            ${question.text}
        </p>
        <div class="question-footer">
            <div class="clock icon-text">
                <div class="username">
                    <img src="/static/assets/apps/asks/global/user.svg" alt="user-img">
                    <span>${question.creator}</span>
                </div>
            </div>
            <ul class="edit-question icon-text">
                <li class="icon-text">
                    <span>${getHoraryByString(question.creation)}</span>
                    <img src="/static/assets/apps/asks/global/clock.png" alt="clock-img">
                </li>
            </ul>
        </div>
    </div>
        `
    })
}


export function renderAllQuestions(questions){
    let renderArea = document.querySelector('.questions-for-end-ranking')
    let themes = getThemesById()
    questions.forEach((question) => {
        renderArea.innerHTML += `
        <div class="question my-questions" theme="${themes[question.theme]}">
        <p class="question-text">
            ${question.text}
        </p>
        <div class="question-footer">
            <div class="clock icon-text">
                <div class="username">
                    <img src="/static/assets/apps/asks/global/user.svg" alt="user-img">
                    <span>${question.creator}</span>
                </div>
            </div>
            <ul class="edit-question icon-text">
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
}