# -*- coding: utf-8 -*-


from collections import deque


def strdecode(sentence):
    if not isinstance(sentence, unicode):
        try:
            sentence = sentence.decode('utf-8')
        except UnicodeDecodeError:
            sentence = sentence.decode('gbk', 'ignore')
    return sentence


class ACAutomaton(object):
    def __init__(self, list_pattern):
        self.trie = dict()
        for pattern in list_pattern:
            self.insert(pattern)
        self.set_fail()

    def insert(self, string):
        u_string = strdecode(string)
        tree = self.trie
        for w in u_string:
            if w not in tree:
                tree[w] = dict()
            tree = tree[w]
        tree["string"] = u_string

    def set_fail(self):
        root = self.trie
        root["fail"] = None
        queue = deque()
        queue.append(root)
        while len(queue) > 0:
            for key in queue[0]:
                if key == "string" or key == "fail":
                    continue

                p = queue[0]["fail"]
                while p and key not in p:
                    p = p["fail"]

                if p:
                    queue[0][key]["fail"] = p
                else:
                    queue[0][key]["fail"] = root

                queue.append(queue[0][key])
            queue.popleft()

    def search(self, string):
        u_string = strdecode(string)
        tree = self.trie
        for w in u_string:
            if w in tree:
                tree = tree[w]
                if "string" in tree:
                    yield tree["string"]
            else:
                while tree and w not in tree:
                    tree = tree["fail"]
                if not tree:
                    tree = self.trie
                else:
                    tree = tree[w]


class QueryRater(object):
    def __init__(self, list_tuple):
        self.trie = dict()
        for item_weight in list_tuple:
            self.insert(item_weight)
        self.set_fail()

    def insert(self, item_weight):
        string, weight = item_weight
        u_string = strdecode(string)
        tree = self.trie
        for w in u_string:
            if w not in tree:
                tree[w] = dict()
            tree = tree[w]
        tree["weight"] = int(weight)

    def set_fail(self):
        root = self.trie
        root["fail"] = None
        queue = deque()
        queue.append(root)
        while len(queue) > 0:
            for key in queue[0]:
                if key == "weight" or key == "fail":
                    continue

                p = queue[0]["fail"]
                while p and key not in p:
                    p = p["fail"]

                if p:
                    queue[0][key]["fail"] = p
                else:
                    queue[0][key]["fail"] = root

                queue.append(queue[0][key])
            queue.popleft()

    def search(self, string):
        list_rt = list()

        u_string = strdecode(string)
        for pos1, w1 in enumerate(u_string):
            tree = self.trie
            for pos2, w2 in enumerate(u_string[pos1:]):
                if w2 in tree:
                    tree = tree[w2]
                    if "weight" in tree:
                        list_rt.append((u_string[pos1: pos1 + pos2 + 1], tree["weight"]))
                else:
                    while tree and w2 not in tree:
                        tree = tree["fail"]
                    if not tree:
                        # tree = self.trie
                        break
                    else:
                        tree = tree[w2]
        return list_rt


if __name__ == "__main__":
    # import sys
    # if len(sys.argv) < 2:
    #     exit(1)

    # list_db = list()
    # with open(sys.argv[1], "r") as fin:
    #     for line in fin:
    #         list_db.append(line.strip().split()[0])
    # fin.close()

    # ac = ACAutomaton(list_db)

    list_db = [(u"钙化斑", 1), (u"钙化", 2), (u"斑块", 3), (u"太阳穴", 4)]

    qr = QueryRater(list_db)
    rst = qr.search(u"你有钙化斑块和太阳穴吗")
    db = "db"
    # print "Input:"
    # for line in sys.stdin:
    #     # while True:
    #     # line = "你有钙化斑块和太阳穴吗"
    #     rst = ac.search(line.strip())
    #     hit = False
    #     for item in rst:
    #         print item
    #         hit = True
    #     if not hit:
    #         print "No substring"
    #     print "Input:"
