"""
Supervisory Control under Local Mean Payoff Constraints

Weighted Finite-state Automaton
"""
import random
from string import ascii_lowercase
import itertools
from itertools import combinations
from transitions_gui import WebMachine
import time
# from transitions.extensions import GraphMachine as Machine


# naive automaton
def iter_all_strings():
    for size in itertools.count(1):
        for s in itertools.product(ascii_lowercase, repeat=size):
            yield "".join(s)


def createState(num=random.randint(1, 100)):
    # number version
    # return [s for s in range(num)]
    # letter version
    return [e.upper() for e in itertools.islice(iter_all_strings(), num)]


def createEvent(num=random.randint(1, 100)):
    return [e for e in itertools.islice(iter_all_strings(), num)]


def transitionFunction(states, events, num=random.randint(1, 100)):
    f = []
    while len(f) < num:
        tran = [events[random.randint(0, len(events) - 1)], states[random.randint(
            0, len(states) - 1)], states[random.randint(0, len(states) - 1)]]
        if tran not in f:
            f.append(tran)
    return f


def weightFunction(num=random.randint(1, 100)):
    return [random.randint(-100, 100) for w in range(num)]


# print("******* naive automaton *******")
numState = 10
numEvent = 12
numTrans = 20
states = createState(numState)
events = createEvent(numEvent)
transi = transitionFunction(states, events, numTrans)
weight = weightFunction(numEvent)
# print(states)
# print(events)
# print(transi)
# print(weight)


# visualization tool
def visualizeMachine(states, transitions, initial, name, ordered_transitions=False, ignore_invalid_triggers=True, auto_transitions=False):
    machine = WebMachine(states=states, transitions=transitions, initial=initial, name=name,
                         ordered_transitions=ordered_transitions,
                         ignore_invalid_triggers=ignore_invalid_triggers,
                         auto_transitions=auto_transitions)
    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        machine.stop_server()


# test 0
# states = ['A', 'B', 'C', 'D', 'E', 'F']
# # initializing the machine will also start the server (default port is 8080)
# machine = WebMachine(states=states, initial='A', name="Simple Machine",
#                      ordered_transitions=True,
#                      ignore_invalid_triggers=True,
#                      auto_transitions=False)
# try:
#     while True:
#         time.sleep(5)
#         machine.next_state()
# except KeyboardInterrupt:  # Ctrl + C will shutdown the machine
#     machine.stop_server()


# test 1
# states = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# transitions = [
#     ['u1', 'A', 'B'],
#     ['a', 'B', 'C'],
#     ['b', 'B', 'D'],
#     ['u2', 'B', 'G'],
#     ['d', 'C', 'B'],
#     ['c', 'D', 'E'],
#     ['u4', 'E', 'F'],
#     ['u6', 'F', 'B'],
#     ['e', 'G', 'H'],
#     ['u3', 'H', 'B'],
#     ['f', 'H', 'I'],
#     ['u5', 'I', 'B'],
#     ['del', 'A', 'J']
# ]
# machine = WebMachine(states=states, transitions=transitions, initial='A', name="test 1",
#                      ordered_transitions=False,
#                      ignore_invalid_triggers=True,
#                      auto_transitions=False)
# try:
#     while True:
#         time.sleep(5)
# except KeyboardInterrupt:
#     machine.stop_server()


# example
# G = (X, E, f, x0, w)
# E = Ec + Euc
X = ['x0', 'x1', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', '!x8']
x0 = 'x0'
Ec = ['a', 'b', 'c', 'd', 'e', 'f']
Euc = ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']
E = Ec + Euc
f = [
    ['u1', 'x0', 'x1'],
    ['a', 'x1', 'x2'],
    ['b', 'x1', 'x3'],
    ['u2', 'x1', 'x6'],
    ['d', 'x2', 'x1'],
    ['c', 'x3', 'x4'],
    ['u4', 'x4', 'x5'],
    ['u6', 'x5', 'x1'],
    ['e', 'x6', 'x7'],
    ['u3', 'x7', 'x1'],
    ['f', 'x7', '!x8'],
    ['u5', '!x8', 'x1']
]
w = {'a': -1, 'b': 1, 'c': 2, 'd': -5, 'e': 3, 'f': 2,
     'u1': -5, 'u2': 1, 'u3': 0, 'u4': 4, 'u5': 1, 'u6': -4}
# fp = f
# for t in fp:
#     t[0] = t[0] + ', ' + str(w[t[0]])
# visualizeMachine(X, fp, x0, "example")


# algorithm 1
# T = (Qy, Qz, E, G, fyz, fzy, w, y0)
def removeUnsafe(states, transitions):
    for s in states:
        if s[0] == '!':
            for t in transitions:
                if t[1] == s or t[2] == s:
                    transitions.remove(t)
            states.remove(s)


def DoDFS(y, X, x0, f, Ec, Euc, w, Qy, Qz, G, fyz, fzy):
    gamma = []
    tEuc = []
    tEc = []
    for t in f:
        if t[1] == y:
            if t[0] in Euc:
                tEuc.append(t[0])
            else:
                tEc.append(t[0])
    if len(tEuc) == 0 and len(tEc) == 0:
        return
    if len(tEuc) != 0 and len(tEc) == 0:
        gamma.append(tEuc)
        G.append(tEuc)
    else:
        if len(tEuc) != 0:
            gamma.append(tEuc)
            G.append(tEuc)
        for i in range(1, len(tEc) + 1):
            l = list(combinations(tEc, i))
            for r in l:
                gamma.append(list(r) + tEuc)
                G.append(list(r) + tEuc)
    for g in gamma:
        z = [y] + g
        fyz.append([g, y, z])
        if z not in Qz:
            Qz.append(z)
            for e in g:
                yn = ''
                for t in f:
                    if t[0] == e and t[1] == y:
                        yn = t[2]
                        break
                if yn[0] == '!':
                    continue
                fzy.append([e, z, yn])
                if yn not in Qy:
                    Qy.append(yn)
                    DoDFS(yn, X, x0, f, Ec, Euc, w, Qy, Qz, G, fyz, fzy)


def removeTerminalState(states, transitions):
    intermediate = []
    for t in transitions:
        intermediate += t[1]
    for t in transitions:
        if t[2] not in intermediate:
            transitions.remove(t)
    for s in states:
        if s not in intermediate:
            states.remove(s)


def cleanState(Qy, Qz, fyz, fzy, x0):
    check = True
    while check:
        for yz in fyz:
            if yz[1] not in Qy or yz[2] not in Qz:
                fyz.remove(yz)
        for zy in fzy:
            if zy[1] not in Qz or zy[2] not in Qy:
                fzy.remove(zy)
        checkPath = {}
        for y in Qy:
            checkPath[y] = 0
        for z in Qz:
            checkPath[str(z)] = 0
        for yz in fyz:
            checkPath[yz[1]] += 1
        for zy in fzy:
            checkPath[str(zy[1])] += 1
        # print(checkPath)
        check = False
        for state in checkPath:
            if checkPath[state] == 0 and state != x0:
                check = True
                if state in Qy:
                    Qy.remove(state)
                else:
                    for z in Qz:
                        if str(z) == state:
                            Qz.remove(z)


y0 = x0
Qy = [y0]
Qz = []
G = []
fyz = []
fzy = []
removeUnsafe(X, f)
DoDFS(y0, X, x0, f, Ec, Euc, w, Qy, Qz, G, fyz, fzy)
# removeTerminalState(Qy + Qz, fyz + fzy)
cleanState(Qy, Qz, fyz, fzy, x0)
Qyp = Qy
Qzp = [str(element) for element in Qz]
fyzp = []
for yz in fyz:
    fyzp.append([str(element) for element in yz])
fzyp = []
for zy in fzy:
    fzyp.append([str(element) for element in zy])
# visualizeMachine(Qyp + Qzp, fyzp + fzyp, y0, "algorithm 1")


# algorithm 2
def StableWindow(Qy, Qz, fyz, fzy, w, N):
    wgr = []
    h = {}
    h[0] = {}
    for q in Qy + Qz:
        h[0][str(q)] = 0
    for i in range(1, N+1):
        h[i] = {}
        for q in Qz:
            ey = [[element[0], element[2]]
                  for element in fzy if element[1] == q and element[2] in Qy]
            if len(ey) != 0:
                ystates = []
                for y in ey:
                    if str(y[1]) in h[i - 1].keys():
                        ystates.append(y)
                if len(ystates) != 0:
                    h[i][str(q)] = min([w[t[0]] + h[i - 1][str(t[1])]
                                        for t in ystates])
                    if h[i][str(q)] >= 0:
                        wgr.append(q)
                # h[i][str(q)] = min([w[t[0]] + h[i - 1][str(t[1])] for t in ey])
                # if h[i][str(q)] >= 0:
                #     wgr.append(q)
        for q in Qy:
            ytz = [element[2]
                   for element in fyz if element[1] == q and element[2] in Qz]
            if len(ytz) != 0:
                zstates = []
                for z in ytz:
                    if str(z) in h[i].keys():
                        zstates.append(z)
                if len(zstates) != 0:
                    h[i][str(q)] = max([h[i][str(z)] for z in zstates])
                    if h[i][str(q)] >= 0:
                        wgr.append(q)
                # h[i][str(q)] = max([h[i][str(z)] for z in ytz])
                # if h[i][str(q)] >= 0:
                #     wgr.append(q)
    wg = []
    [wg.append(q) for q in wgr if not q in wg]
    return wg


def WinLocal(Qy, Qz, fyz, fzy, w, N):
    wg = StableWindow(Qy, Qz, fyz, fzy, w, N)
    wp = []
    if len(wg) == len(Qy + Qz) or len(wg) == 0:
        wp = wg
    else:
        Qyn = []
        for y in Qy:
            if y in wg:
                Qyn.append(y)
        Qzn = []
        for z in Qz:
            if z in wg:
                Qzn.append(z)
        # for y in Qy:
        #     if y not in wg:
        #         Qy.remove(y)
        # for z in Qz:
        #     if z not in wg:
        #         Qz.remove(z)
        # for yz in fyz:
        #     if yz[1] not in wg or yz[2] not in wg:
        #         fyz.remove(yz)
        # for zy in fzy:
        #     if zy[1] not in wg or zy[2] not in wg:
        #         fzy.remove(zy)
        wp = WinLocal(Qyn, Qzn, fyz, fzy, w, N)
    return wp


def attraction(attr, s0, Q, f, wp):
    if s0 in wp:
        return True
    else:
        res = []
        for i in f:
            if i[1] == s0:
                res.append(attraction(attr, i[2], Q, f, wp))
        for i in res:
            if i == False:
                return False
        attr.append(s0)
    return True


def winRegion(Qy, Qz, fyz, fzy, w, N, y0, wl):
    ws = []
    n = 1
    Qyw = [y for y in Qy]
    Qzw = [z for z in Qz]
    while len(ws) != len(Qy + Qz):
        wp = WinLocal(Qyw, Qzw, fyz, fzy, w, N)
        wl += wp
        if len(wp) == 0:
            break
        # attr
        attrr = []
        dump = attraction(attrr, y0, Qy + Qz, fzy + fyz, wp)
        # attr = []
        # for p in wp:
        #     if p in Qz:
        #         for yz in fyz:
        #             if yz[1] not in wp and yz[2] == p:
        #                 count = 1
        #                 for yz2 in fyz:
        #                     if yz2[1] == yz[1] and yz2[2] not in wp:
        #                         count += 1
        #                 if count == 1:
        #                     wp.append(yz[1])
        #     else:
        #         for zy in fzy:
        #             if zy[1] not in wp and zy[2] == p:
        #                 count = 1
        #                 for zy2 in fzy:
        #                     if zy2[1] == zy[1] and zy2[2] not in wp:
        #                         count += 1
        #                 if count == 1:
        #                     wp.append(zy[1])

        # -------
        for p in wp + attrr:
            if p not in ws:
                ws.append(p)
        for y in Qyw:
            if y in ws:
                Qyw.remove(y)
        for z in Qzw:
            if z in ws:
                Qzw.remove(z)
        n += 1
    return ws


N = 3
wl = []
ws = winRegion(Qy, Qz, fyz, fzy, w, N, y0, wl)
wsp = [str(i) for i in ws]
fp = []
for i in fzy + fyz:
    if i[1] in ws and i[2] in ws:
        fp.append([str(i[0]), str(i[1]), str(i[2])])
# visualizeMachine(wsp, fp, y0, "algorithm 2")


# check output of algorithm 2 and clear up Q and f for algorithm 3
Qy = []
Qz = []
for i in ws:
    if type(i) == type(''):
        Qy.append(i)
    else:
        Qz.append(i)
f = []
yz = []
zy = []
for i in fzy + fyz:
    if i[1] in Qy and i[2] in Qz:
        f.append([i[0], i[1], i[2]])
        yz.append([i[0], i[1], i[2]])
    if i[1] in Qz and i[2] in Qy:
        f.append([i[0], i[1], i[2]])
        zy.append([i[0], i[1], i[2]])
fyz = yz
fzy = zy


# algorithm 3
def Unfold(y0u, Qyu, Qzu, fyzu, fzyu, Qy, Qz, fyz, fzy):
    duplicate = {}
    lru = {}
    for i in Qy:
        duplicate[i] = 1
        lru[i] = 0
    state = y0u
    while len(Qzu) < len(Qz):
        # print(state)
        du = False
        sn = ''
        if state in Qyu:
            if duplicate[state] != 1:
                du = True
                sn = '{'+state+'}'+str(lru[state])
                if lru[state] != 0:
                    Qyu.append(sn)
        else:
            Qyu.append(state)
            d = 0
            for i in fyz:
                if i[1] == state:
                    d += 1
            duplicate[state] = d
        lru[state] = (lru[state] + 1) % duplicate[state]
        temp = []
        for i in fyz:
            if i[1] == state and i[2] not in Qzu:
                temp.append(i)
        # print(temp)
        z = ''
        if len(temp) == 1:
            z = temp[0][2]
            Qzu.append(z)
            if du == False:
                fyzu.append(temp[0])
            else:
                fyzu.append([temp[0][0], sn, z])
        else:
            t = [len(i[2]) for i in temp]
            yz = temp[t.index(max(t))]
            z = yz[2]
            Qzu.append(z)
            if du == False:
                fyzu.append(yz)
            else:
                fyzu.append([yz[0], sn, z])
        # print(z)
        y = []
        for i in fzy:
            if i[1] == z:
                if lru[i[2]] == 0:
                    fzyu.append(i)
                else:
                    fzyu.append([i[0], i[1], '{'+i[2]+'}'+str(lru[i[2]])])
                y.append(i[2])
        # print(y)
        if len(y) == 1:
            state = y[0]
        else:
            yin = []
            for i in y:
                if i not in Qyu:
                    yin.append(i)
            num = []
            if len(yin) == 0:
                for i in y:
                    count = 0
                    for j in fzy:
                        if j[2] == i:
                            count += 1
                    num.append(count)
                state = y[num.index(min(num))]
            else:
                for i in yin:
                    count = 0
                    for j in fzy:
                        if j[2] == i:
                            count += 1
                    num.append(count)
                state = y[num.index(min(num))]


y0u = y0
Qyu = []
Qzu = []
fyzu = []
fzyu = []
Unfold(y0u, Qyu, Qzu, fyzu, fzyu, Qy, Qz, fyz, fzy)
# print(y0u)
# print(Qyu)
# print(Qzu)
# print(fyzu)
# print(fzyu)
Qup = [str(i) for i in Qyu+Qzu]
fup = []
for i in fzyu+fyzu:
    fup.append([str(i[0]), str(i[1]), str(i[2])])
# visualizeMachine(Qup, fup, y0u, "algorithm 3-1")


y0 = y0u
Q = Qyu
f = []
for y in Q:
    for yz in fyzu:
        if yz[1] == y:
            z = yz[2]
            for zy in fzyu:
                if zy[1] == z:
                    f.append([zy[0], y, zy[2]])
Qp = [str(i) for i in Q]
fp = []
for i in f:
    fp.append([str(i[0]), str(i[1]), str(i[2])])
# visualizeMachine(Qp, fp, y0, "algorithm 3-2")


# My Example
X = ['x'+str(i) for i in range(25)]
X[14] = '!x14'
X[17] = '!x17'
X[21] = '!x21'
x0 = 'x0'
Ec = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
      'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's']
Euc = ['u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9',
       'u10', 'u11', 'u12', 'u13', 'u14', 'u15', 'u16', 'u17', 'u18']
E = Ec + Euc
f = [
    ['a', 'x0', 'x1'],
    ['u1', 'x0', 'x2'],
    ['b', 'x0', 'x5'],
    ['c', 'x1', 'x3'],
    ['g', 'x2', 'x10'],
    ['u2', 'x3', 'x4'],
    ['u11', 'x3', 'x0'],
    ['u3', 'x4', 'x11'],
    ['d', 'x4', 'x1'],
    ['u12', 'x5', 'x6'],
    ['u8', 'x6', 'x7'],
    ['n', 'x6', 'x8'],
    ['o', 'x6', 'x9'],
    ['j', 'x7', 'x6'],
    ['u18', 'x8', 'x4'],
    ['p', 'x8', 'x18'],
    ['q', 'x9', 'x15'],
    ['u14', 'x9', 'x16'],
    ['u5', 'x10', 'x12'],
    ['h', 'x10', 'x6'],
    ['e', 'x11', '!x14'],
    ['f', 'x11', 'x5'],
    ['u6', 'x12', 'x19'],
    ['i', 'x12', 'x13'],
    ['u9', 'x13', '!x21'],
    ['u16', 'x13', 'x10'],
    ['u4', '!x14', 'x4'],
    ['l', 'x15', 'x0'],
    ['u15', 'x16', '!x17'],
    ['u17', '!x17', 'x20'],
    ['u13', 'x18', 'x24'],
    ['u7', 'x19', 'x12'],
    ['r', 'x20', 'x23'],
    ['k', '!x21', 'x22'],
    ['u10', 'x22', 'x0'],
    ['s', 'x23', 'x20'],
    ['m', 'x24', 'x0']
]
w = {'a': -1, 'b': 1, 'c': 2, 'd': -5, 'e': 3, 'f': 2, 'g': -2, 'h': 1, 'i': 2, 'j': 3, 'k': -1, 'l': 0, 'm': 2, 'n': -2, 'o': -1, 'p': 3, 'q': -1, 'r': 2, 's': -3, 'u1': -5,
     'u2': 1, 'u3': 0, 'u4': 4, 'u5': 1, 'u6': -4, 'u7': -4, 'u8': 3, 'u9': 1, 'u10': -1, 'u11': 2, 'u12': -1, 'u13': -2, 'u14': -3, 'u15': 4, 'u16': 2, 'u17': 1, 'u18': 1}

# show original graph
# fp = f
# for t in fp:
#     t[0] = t[0] + ', ' + str(w[t[0]])
# visualizeMachine(X, fp, x0, "origin")

# algorithm 1
# y0 = x0
# Qy = [y0]
# Qz = []
# G = []
# fyz = []
# fzy = []
# removeUnsafe(X, f)
# DoDFS(y0, X, x0, f, Ec, Euc, w, Qy, Qz, G, fyz, fzy)
# removeTerminalState(Qy + Qz, fyz + fzy)
# manual fix
# Qy.remove('x16')
# for i in fzy:
#     if i[0] == 'u14':
#         fzy.remove(i)
# for i in fyz:
#     if i[0] == 'u14':
#         fyz.remove(i)
# manual fix
# cleanState(Qy,Qz,fyz,fzy,x0)
# Qyp = Qy
# Qzp = [str(element) for element in Qz]
# fyzp = []
# for yz in fyz:
#     fyzp.append([str(element) for element in yz])
# fzyp = []
# for zy in fzy:
#     fzyp.append([str(element) for element in zy])
# visualizeMachine(Qyp + Qzp, fyzp + fzyp, y0, "algorithm 1")

# algorithm 2
# N = 3
# wl = []
# ws = winRegion(Qy, Qz, fyz, fzy, w, N, y0, wl)
# wsp = [str(i) for i in ws]
# fp = []
# for i in fzy + fyz:
#     if i[1] in ws and i[2] in ws:
#         fp.append([str(i[0]), str(i[1]), str(i[2])])
# visualizeMachine(wsp, fp, y0, "algorithm 2")


# Qy = []
# Qz = []
# for i in ws:
#     if type(i) == type(''):
#         Qy.append(i)
#     else:
#         Qz.append(i)
# f = []
# yz = []
# zy = []
# for i in fzy + fyz:
#     if i[1] in Qy and i[2] in Qz:
#         f.append([i[0], i[1], i[2]])
#         yz.append([i[0], i[1], i[2]])
#     if i[1] in Qz and i[2] in Qy:
#         f.append([i[0], i[1], i[2]])
#         zy.append([i[0], i[1], i[2]])
# fyz = yz
# fzy = zy

# y0u = y0
# Qyu = []
# Qzu = []
# fyzu = []
# fzyu = []
# Unfold(y0u, Qyu, Qzu, fyzu, fzyu, Qy, Qz, fyz, fzy)
# Qup = [str(i) for i in Qyu+Qzu]
# fup = []
# for i in fzyu+fyzu:
#     fup.append([str(i[0]), str(i[1]), str(i[2])])
# # visualizeMachine(Qup, fup, y0u, "algorithm 3-1")


# y0 = y0u
# Q = Qyu
# f = []
# for y in Q:
#     for yz in fyzu:
#         if yz[1] == y:
#             z = yz[2]
#             for zy in fzyu:
#                 if zy[1] == z:
#                     f.append([zy[0], y, zy[2]])
# Qp = [str(i) for i in Q]
# fp = []
# for i in f:
#     fp.append([str(i[0]), str(i[1]), str(i[2])])
# # visualizeMachine(Qp, fp, y0, "algorithm 3-2")
