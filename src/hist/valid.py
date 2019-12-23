from hist.lib import makeHist
from hist.Const import imp_meta, imp_meta_border


def validation(csv):
    checkWeight = [1]*len(csv)
    CheckHist = makeHist(csv, checkWeight)
    return not 1 in CheckHist[0].ravel()

def Check_meta(csv):
	for j in imp_meta:
		if j == 'Age':
			for i in csv[j]:
				if i < imp_meta_border[j][0] or i > imp_meta_border[j][1]:
					return i,j
		else:
			for i in csv[j]:
				if not i in imp_meta_border[j]:
					return i,j
	return 0,0