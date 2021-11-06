import {In} from './support.js'

export function validateQuestion(text, theme_id){
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