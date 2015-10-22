from trello import Boards, Members
import requests


def main():
    api_key = "7dcfa320a1cf6348fa4d7ca8ea8e3c07"
    # print api.get_token_url("cz app", expires="never", write_access=True)
    token = "d04c70b412973cd9a4b309119f9000e7afd79c57c360362817cd1ef63ff672e7"
    members = Members(apikey=api_key, token=token)
    boards = Boards(apikey=api_key, token=token)
    all_boards = members.get_board('canzhang3')
    task_board = filter(lambda x: x['name'] == 'Tasks', all_boards)[0]
    task_lists = boards.get_list(task_board['id'])
    done_list = filter(lambda x: x['name'] == 'Done', task_lists)[0]
    yesterday_list = filter(lambda x: x['name'] == 'Yesterday', task_lists)[0]
    r = requests.post("https://trello.com/1/lists/{}/archiveAllCards?key={}&token={}".format(yesterday_list["id"], api_key, token))
    print "archive yesterday: ", r
    r = requests.post("https://trello.com/1/lists/{}/moveAllCards?key={}&token={}".format(done_list["id"], api_key, token), {"idBoard": task_board["id"], "idList": yesterday_list["id"]})
    print "move done: ", r

if __name__ == "__main__":
    main()
