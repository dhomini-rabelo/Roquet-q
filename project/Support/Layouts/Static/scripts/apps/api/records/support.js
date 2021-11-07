export function getThemesById(){
    let themes = document.querySelectorAll('.select-main option')
    let themeObject = {}
    themes.forEach((theme) => {
        themeObject[Number.parseInt(theme.value)] = theme.innerHTML
    })
    return themeObject
}

export function getHoraryByString(horaryString) {
    let now = new Date(horaryString)
    let hours = now.getHours()
    let minutes = now.getMinutes()

    if (hours>=10 && minutes>=10){
        return `${hours}:${minutes}`
    }else if (hours>=10 && minutes<10){
        return `${hours}:0${minutes}`
    }else if (hours<10 && minutes>=10){
        return `0${hours}:${minutes}`
    }else if (hours<10 && minutes<10){
        return `0${hours}:0${minutes}`
    }
}

export function disableSelects(){
    let selects = document.querySelectorAll('select')
    selects.forEach((select) => {
        select.disabled = true
    })
}

export function activeSelects(){
    let selects = document.querySelectorAll('select')
    selects.forEach((select) => {
        select.disabled = false
    })
}