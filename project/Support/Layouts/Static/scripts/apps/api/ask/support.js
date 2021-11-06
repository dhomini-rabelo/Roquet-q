export function In(obj, array) {
    for (let i = 0; i < array.length; i++) {
        if (array[i] === obj) {
            return true
        }
    }
    return false
}

export function getHorary(){
    let now = new Date()
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

