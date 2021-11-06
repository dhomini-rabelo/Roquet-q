
export function asyncGet(url) {
    return fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        }
    }).then((data)=>data.json())
}

export function asyncPost(url, body) {
    return fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    }).then((data)=>data.json())
}

export function asyncPut(url, body) {
    return fetch(url, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(body)
    }).then((data)=>data.json())
}
