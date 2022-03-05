# Edited from:
#https://github.com/fxsjy/jieba/blob/master/jieba/analyse/textrank.py

from __future__ import absolute_import, unicode_literals
import sys
from operator import itemgetter
from collections import defaultdict


class UndirectWeightedGraph:
    d = 0.85

    def __init__(self):
        self.graph = defaultdict(list)

    def addEdge(self, start, end, weight):
        self.graph[start].append((start, end, weight))
        self.graph[end].append((end, start, weight))

    def rank(self):
        ws = defaultdict(float)
        outSum = defaultdict(float)

        wsdef = 1.0 / (len(self.graph) or 1.0)
        for n, out in self.graph.items():
            ws[n] = wsdef
            outSum[n] = sum((e[2] for e in out), 0.0)

        sorted_keys = sorted(self.graph.keys())
        for _ in range(10):  # 10 iters
            for n in sorted_keys:
                s = 0
                for e in self.graph[n]:
                    s += e[2] / outSum[e[1]] * ws[e[1]]
                ws[n] = (1 - self.d) + self.d * s

        (min_rank, max_rank) = (sys.float_info[0], sys.float_info[3])

        for w in ws.values():
            if w < min_rank:
                min_rank = w
            if w > max_rank:
                max_rank = w

        for n, w in ws.items():
            ws[n] = (w - min_rank / 10.0) / (max_rank - min_rank / 10.0)

        return ws


class TextRank:

    def __init__(self):
        self.span = 5

    def getKeywords(self, tokens):
        g = UndirectWeightedGraph()
        cm = defaultdict(int)
        for i, token in enumerate(tokens):
            for j in range(i + 1, i + self.span):
                if j >= len(tokens):
                    break
                cm[(token, tokens[j])] += 1

        for terms, w in cm.items():
            g.addEdge(terms[0], terms[1], w)
        nodes_rank = g.rank()

        tags = sorted(nodes_rank.items(), key=itemgetter(1), reverse=True)
        
        return {key:value for (key,value) in tags[:10]}