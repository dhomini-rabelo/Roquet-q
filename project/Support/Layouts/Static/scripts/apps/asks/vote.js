let options = document.querySelectorAll('.survey-option')

options.forEach((option)=>{
    option.addEventListener('click', registerVote)
})


function registerVote(event){
    options.forEach((option) => {
        option.classList.add('option-normal-border')
    })
    
    for(let option of options){
        if(option.classList.contains('option-border')){
            return
        }
    }

    event.currentTarget.classList.add('option-border')
}

