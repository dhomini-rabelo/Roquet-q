export function adaptTheTime(day, month){
    if (day>=10&&month>=10){
        return `${month+1}-${day}`
    }else if (day>=10&&month<10){
        return `0${month+1}-${day}`
    }else if (day<10&&month>=10){
        return `${month+1}-0${day}`
    }else if (day<10&&month<10){
        return `0${month+1}-0${day}`
    }
}
    

export function strDate(){
    let date = new Date()
    let year = date.getFullYear()
    let month = date.getMonth()
    let day = date.getDate()
    let formattedDate = adaptTheTime(day, month)
    return `${year}-${formattedDate}`
}