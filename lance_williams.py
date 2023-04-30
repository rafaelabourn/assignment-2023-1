import sys


def intify(inf):
    res = []
    for i in inf:
        res.append(int(i))
    return res

def read_input():
    with open(sys.argv[2],'r') as i:
        inf = i.readline()
        inf = inf.split()
        inf = intify(inf)
    inf.sort()
    return inf


def init_dist(inf):
    diff = []
    for i in range(len(inf)):
        diff.append([])
        for j in range(len(inf)):
            if i != j:
                diff[i].append(abs(inf[j]-inf[i]))
            else:
                diff[i].append(100)
    return diff


def findmin(diff):
    minimum = 100
    s=-1
    t=-1
    for i in range(len(diff)):
        for j in range(len(diff[i])):
            if minimum > diff[i][j]:
                minimum = diff[i][j]
                s = i
                t = j
    return minimum,s,t


def single_calc(s,t,v,diff,inf):
    # print(s,t,v)
    res = 1/2*diff[inf.index(s)][inf.index(v)]
    res += 1/2*diff[inf.index(t)][inf.index(v)]
    res += -1/2*abs(diff[inf.index(s)][inf.index(v)]-diff[inf.index(t)][inf.index(v)])
    return res


def complete_calc(s,t,v,diff,inf):
    res = 1/2*diff[inf.index(s)][inf.index(v)]
    res += 1/2*diff[inf.index(t)][inf.index(v)]
    res += 1/2*abs(diff[inf.index(s)][inf.index(v)]-diff[inf.index(t)][inf.index(v)])
    return res


def average_calc(s,t,v,diff,inf):
    res = (len(s)/(len(s)+len(t)))*diff[inf.index(s)][inf.index(v)]
    res += (len(t)/(len(s)+len(t)))*diff[inf.index(t)][inf.index(v)]
    return res


def ward_calc(s,t,v,diff,inf):
    res = ((len(s)+len(v))/(len(s)+len(t)+len(v)))*diff[inf.index(s)][inf.index(v)]
    res += ((len(s)+len(v))/(len(s)+len(t)+len(v)))*diff[inf.index(t)][inf.index(v)]
    res += -(len(v)/(len(s)+len(t)+len(v)))*diff[inf.index(s)][inf.index(t)]
    return res


def calc(s,t,v,diff,inf):
    if sys.argv[1] == 'single':
        return single_calc(s,t,v,diff,inf)
    elif sys.argv[1] == 'complete':
        return complete_calc(s,t,v,diff,inf)
    elif sys.argv[1] == 'average':
        return average_calc(s,t,v,diff,inf)
    elif sys.argv[1] == 'ward':
        return ward_calc(s,t,v,diff,inf)
    else:
        return "error"


def update_diff(s,t,diff,inf):
    nd = []
    for i in range(len(diff)):
        if i != s and i != t:
            nd.append([])
            for j in range(len(diff[i])):
                if j != s and j != t:
                    nd[-1].append(diff[i][j])
                elif j == s:
                    nd[-1].append(calc(inf[s],inf[t],inf[i],diff,inf))
        elif i == s:
            nd.append([])
            for j in range(len(diff[i])):
                if j != s and j != t:
                    # print(len(diff),len(inf),len(diff[i]))
                    nd[-1].append(calc(inf[s],inf[t],inf[j],diff,inf))
                elif not (i == s and j == t):
                    nd[-1].append(100)
    
    return nd


def mkprt(f,s,minimum):
    res = ''
    res += str(f).replace('[','(').replace(']',')').replace(',','') + ' '
    res += str(s).replace('[','(').replace(']',')').replace(',','') + ' '
    res += f'{minimum:.2f} '
    res += str(len(f)+len(s))
    return res


def solve(inf,diff):
    for i in range(len(inf)):
        inf[i] = [inf[i]]

    res = []
    while True:
        minimum,s,t = findmin(diff)
        diff = update_diff(s,t,diff,inf)
        res.append(mkprt(inf[s],inf[t],minimum))
        inf[s].extend(inf[t])
        inf.remove(inf[t])
        # print(inf,diff)
        if len(inf) == 1:
            break
    
    return res
        

def printIt(res):
    for i in res:
        print(i)

inf = read_input()
diff = init_dist(inf)
res = solve(inf,diff)
printIt(res)

