import requests

def lineNotifyMessage(token, msg):

    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg }
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code




books = "123"
token = 'dH7Do0NdzY2QSbSFltMu4iAAGDnK4pY4xD3qGFGyyWq'

lineNotifyMessage(token,books)