let selectsMain = document.querySelectorAll('.select-main')
let selectedsDefaultOption = document.querySelectorAll('option[selected=""]')

selectsMain.forEach((selectMain) => {
    selectMain.addEventListener('change', showThemeQuestion)
})
document.addEventListener('DOMContentLoaded', getInitialThemeQuestion)



function showThemeQuestion() {
    let questions = document.querySelectorAll('div.app.select.visible  .my-questions')
    let currentMainTheme = this.selectedOptions[0].innerHTML
    questions.forEach((question) => {
        let questionTheme = question.getAttribute('theme')

        if (questionTheme === currentMainTheme){
            if(!question.classList.contains('visible')){
                question.classList.add('visible')
            }
        } else {
            if(question.classList.contains('visible')){    
                question.classList.remove('visible')
            }
        }
    })    
}


export function getInitialThemeQuestion(){
    selectedsDefaultOption.forEach((selectedDefaultOption) => {
        if (selectedDefaultOption){
            let questions = document.querySelectorAll('div.app.select  .my-questions')
            let currentMainTheme = selectedDefaultOption.innerHTML
            questions.forEach((question) => {
            let questionTheme = question.getAttribute('theme')
    
            if (questionTheme === currentMainTheme){
                if(!question.classList.contains('visible')){
                    question.classList.add('visible')
                }
            } else {
                if(question.classList.contains('visible')){    
                    question.classList.remove('visible')
                }
            }
            })  
        }
    })

}