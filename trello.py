def solve(code, start):
    import json
    import datetime
    import requests
    url = "https://api.trello.com/1/boards/"
    # unpack api and token
    with open('trelloapi.txt', 'r') as f:
        data = f.read()
    api_key = json.loads(data)
    # create board
    name = "Pymi {} timetable".format(code)
    query = {
        'name': name,
        'prefs_permissionLevel': 'public'
    }
    query.update(api_key)

    response = requests.request("POST", url, params=query)

    board_id = response.json()['id']
    # create thursday list
    url = "https://api.trello.com/1/boards/{}/lists".format(board_id)
    query = {'name': 'Thursday'}
    query.update(api_key)
    response = requests.request("POST", url, params=query)
    # get list_id
    thurs_id = response.json()['id']
    # create tuesday list
    query = {'name': 'Tuesday'}
    query.update(api_key)
    response = requests.request("POST", url, params=query)
    # create list_id
    tues_id = response.json()['id']
    # converse time format
    due_time = datetime.datetime.strptime(start, '%d/%m/%Y').date()
    count = 0
    while count <= 12:
        # tuesday
        if due_time.isoweekday() == 2:
            count += 1
            url = "https://api.trello.com/1/cards"
            name = "Lession {}".format(count)
            query = {'idList': tues_id, 'due': due_time, 'name': name}
            query.update(api_key)
            response = requests.request("POST", url, params=query)
            due_time += datetime.timedelta(days=2)
        if count == 12:
            break
        # thursday
        elif due_time.isoweekday() == 4:
            count += 1
            url = "https://api.trello.com/1/cards"
            name = "Lession {}".format(count)
            query = {'idList': thurs_id, 'due': due_time, 'name': name}
            query.update(api_key)
            response = requests.request("POST", url, params=query)
            due_time += datetime.timedelta(days=5)


def main():
    import sys
    course_code, input_start = sys.argv[1], sys.argv[2]
    solve(course_code, input_start)


if __name__ == "__main__":
    main()
