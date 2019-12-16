
from hist.Const import Bins


def validation(csv):
    b = 1
    for i in Bins:
        b = b * i
    if len(csv.index) < b:
        return False
    check = [1 for i in csv.index]
    Check = makeHist(csv, check)
    flag = proverka(Check[0])
    if flag > 0:
        return False
    else:
        return True



def proverka(check):
    flag =0
    if str(type(check[0])) == "<class 'numpy.ndarray'>":
        for i in check:
            flag = flag + proverka(i)
    else:
        if int(sum(check)) == 1:
            flag = 1
    return flag