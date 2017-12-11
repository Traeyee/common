# -*- coding: utf-8 -*-


from compatitator import strdecode
from collections import deque


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


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        exit(1)

    list_db = list()
    with open(sys.argv[1], "r") as fin:
        for line in fin:
            list_db.append(line.strip().split()[0])
    fin.close()

    ac = ACAutomaton(list_db)

    print "Input:"
    for line in sys.stdin:
        # while True:
        # line = "你有钙化斑块吗"
        rst = ac.search(line.strip())
        hit = False
        for item in rst:
            print item
            hit = True
        if not hit:
            print "No substring"
        print "Input:"
