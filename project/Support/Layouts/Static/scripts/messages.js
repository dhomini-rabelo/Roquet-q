document.addEventListener('DOMContentLoaded', clearAlert)



function clearAlert() {
    setTimeout(() => {
        let alerts = document.querySelectorAll('.alert')
        alerts.forEach((alert) => {
            alert.style.display = 'none'
        })
    }, 3000)
}
