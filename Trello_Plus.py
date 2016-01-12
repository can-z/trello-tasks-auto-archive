import webbrowser
import sys
import configparser
import requests
import json
from urllib import parse

USR_NAME = 'yuan119'
SETTING_FILE = "settings.cfg"
COM_NUM = 4
TARGET_BOARD = 'Tasks'

MSG = """
Trello Plus:

Please select one of the following options:
1.Authorization
2.Make A New Day
3.Display Board Names
3.Exit

Enter your choice: """

MSG2 = '''
Your web brower will get you to the authorization page
To authorize this app, you need to press allow on that page and copy the "TOKEN" from the page right after that
Enter OK to continue: 
'''


class Trello_Plus():
    def __init__(self):
        '''(Trello_Plus) -> NoneType
        '''
        self._api_key = None
        self._token = None
        self._boards = None

    def authorize(self):
        '''(Trello_Plus) -> NoneType
        This method will guide you to make an authorization for the program.
        It will pop up a webpage
        '''

        understood = input(MSG2)
        while understood != "OK":
            understood = input(MSG2)
        webbrowser.open(self.get_token_url("New App"))
        self._token = input("Now you need to enter the token: ")

    def get_token_url(self, name, expires='never', write_access=True):
        '''
        '''
        return 'https://trello.com/1/authorize?key=%s&name=%s&expiration=%s&response_type=token&scope=%s' % (self._api_key, parse.quote_plus(name), expires, 'read,write' if write_access else 'read')

    def step_up(self, file_name):
        ''' Read api key and token from a file with name file_name.
        --- Need to be changed to get them from ??? directly.
        '''
        # set up a configparser
        config = configparser.ConfigParser()
        config.read('settings.cfg')
        self._api_key = config.get('credentials', 'api_key')
        self._token = config.get('credentials', 'token')
        self._boards = self.get_boards(USR_NAME)

    def get_boards(self, user_name):
        '''
        '''

        resp = requests.get("https://trello.com/1/members/%s/boards" %
                            (user_name),
                            params=dict(key=self._api_key,
                                        token=self._token,
                                        filter=None,
                                        fields=None,
                                        actions=None,
                                        action_fields=None,
                                        action_limit=None),
                            data=None)
        resp.raise_for_status()
        return resp.json()

    def get_ids_names(self, obj):
        '''Return a dict of board names to board ids.
        '''

        result = {}
        for board_dict in obj:
            name = None
            bid = None
            for k in board_dict.keys():
                if k == 'name':
                    name = board_dict[k]
                elif k == 'id':
                    bid = board_dict[k]
            result[name] = bid

        return result

    def display_board_names(self):

        print('\n'.join(list(self.get_ids_names(self._boards).keys())))

    def get_id_by_name(self, board_name):
        '''Return the id of the board by given its name.'''

        bid_names = self.get_ids_names(self._boards)

        return bid_names[board_name]

    def get_lists(self, bid):
        '''Return a list of "lists" by given a board_name.
        '''

        resp = requests.get("https://trello.com/1/boards/%s/lists" %
                            (bid),
                            params=dict(key=self._api_key,
                                        token=self._token,
                                        cards=None,
                                        card_fields=None,
                                        filter=None,
                                        fields=None),
                            data=None)
        resp.raise_for_status()

        return resp.json()

    def move_list(self, board_name, list1, list2):
        '''Move every cards under list1 into list2.'''

        bid = self.get_id_by_name(board_name)
        lists = self.get_lists(bid)
        lists = self.get_ids_names(lists)
        lid1 = lists[list1]
        lid2 = lists[list2]
        resp1 = requests.post(
            "https://trello.com/1/lists/%s/archiveAllCards?key=%s&token=%s" % (lid2, self._api_key, self._token))
        resp1.raise_for_status()
        resp2 = requests.post("https://trello.com/1/lists/%s/moveAllCards?key=%s&token=%s" %
                              (lid1, self._api_key, self._token), {"idBoard": bid, "idList": lid2})
        resp2.raise_for_status()

    def new_day(self, board_name, list1, list2):
        ''' A new day has come!
        Move everything under "done" into "yesterday"
        '''

        self.move_list(board_name, list1, list2)

    def run(self):
        '''Main function of the program, which provides several options to the 
        users.
        '''
        self.step_up(SETTING_FILE)

        command = int(input(MSG))
        while command > 0 and command <= COM_NUM:
            if command == 1:
                self.authorize()
            elif command == 2:
                self.new_day(TARGET_BOARD, 'done', 'Yesterday')
            elif command == 3:
                self.display_board_names()
            else:
                sys.exit()
            command = int(input(MSG))


if __name__ == '__main__':
    tp = Trello_Plus()
    tp.run()
