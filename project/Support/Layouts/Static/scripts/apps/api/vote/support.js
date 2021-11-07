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
    let selects = document.querySelectorAll('select.select-main')
    selects.forEach((select) => {
        select.disabled = true
    })
}

export function activeSelects(){
    let selects = document.querySelectorAll('select.select-main')
    selects.forEach((select) => {
        select.disabled = false
    })
}



export function shuffle(baseArray) {
    let array = baseArray.slice()
    array.sort(() => .5 - Math.random())
    return array
}


export function In(obj, array) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] === obj) {
            return true
        }
    }
    return false
}

