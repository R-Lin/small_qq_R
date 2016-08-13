# coding:utf8

import ConfigParser


class Broadcast(object):
    """
    Provide the broadcast way for groups to comunicating
    """
    def __init__(self):
        self.config_file = 'config/main.conf'
        self.cf = ConfigParser.ConfigParser()
        self.cf.read(self.config_file)
        self.gids_set = ''

    def get_name(self):
        """
        Return the formatted name sets
        """
        names = [item[1][1:-1].decode('utf8') for item in self.cf.items('GroupName')]
        return names

    def handle_message(self, messages, func):
        """
        Recieve the messages and send to other in gid_set by func
        """
        rece_gids = self.gids_set - set([messages[0]])
        message = map(lambda x: x.encode('utf8') if isinstance(x, unicode) else str(x), messages[1:])
        for gid in rece_gids:
            print gid, '【%s】%s: %s' % (message[0], message[1], message[2])
            # print func(gid, u" ".join(messages[1:]).encode('utf8'))









