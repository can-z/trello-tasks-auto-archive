from trello import Boards, Members
import requests
import ConfigParser


def main():
    config = ConfigParser.ConfigParser()
    config.read('settings.cfg')
    api_key = config.get('credentials', 'apikey')
    # print api.get_token_url("cz app", expires="never", write_access=True)
    token = config.get('credentials', 'token')
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
