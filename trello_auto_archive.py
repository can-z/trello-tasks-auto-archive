import os
import requests
import ConfigParser
import json


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_token_url(name, expires='never', write_access=True):
    '''
    '''
    return 'https://trello.com/1/authorize?key=%s&name=%s&expiration=%s&response_type=token&scope=%s' % ('9172d343955dac4e200163fcae965088', name, expires, 'read,write' if write_access else 'read')


def main():
    config = ConfigParser.ConfigParser()
    config.read(os.path.join(__location__, 'settings.cfg'))
    username = config.get('credentials', 'username')
    api_key = config.get('credentials', 'apikey')
    token = config.get('credentials', 'token')

    resp = requests.get("https://trello.com/1/members/%s/boards" %
                        username,
                        params=dict(key=api_key,
                                    token=token,
                                    filter=None,
                                    fields=None,
                                    actions=None,
                                    action_fields=None,
                                    action_limit=None),
                        data=None)

    all_boards = json.loads(resp.content)
    resp = requests.get("https://trello.com/1/members/%s/boards" %
                        username,
                        params=dict(key=api_key,
                                    token=token),
                        data=None)
    all_boards = json.loads(resp.content)
    task_board = filter(lambda x: x['name'] == 'Tasks', all_boards)[0]
    resp = requests.get("https://trello.com/1/boards/%s/lists" %
                        (task_board['id']),
                        params=dict(key=api_key,
                                    token=token),
                        data=None)
    task_lists = json.loads(resp.content)
    done_list = filter(lambda x: x['name'] == 'Done', task_lists)[0]
    yesterday_list = filter(lambda x: x['name'] == 'Yesterday', task_lists)[0]
    r = requests.post("https://trello.com/1/lists/{}/archiveAllCards?key={}&token={}".format(yesterday_list["id"], api_key, token))
    print "archive yesterday: ", r
    r = requests.post("https://trello.com/1/lists/{}/moveAllCards?key={}&token={}".format(done_list["id"], api_key, token), {"idBoard": task_board["id"], "idList": yesterday_list["id"]})
    print "move done: ", r

if __name__ == "__main__":
    main()
