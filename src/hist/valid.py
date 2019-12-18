
from hist.Const import Bins


def validation(csv):
    checkWeight = [1]*len(csv)
    CheckHist = makeHist(csv, checkWeight)
	TrueSize = []
	Dart = CheckHist[0]
	TrueCheck = [[0] * len(Dart), [0] * len(Dart[0]), [0] * len(Dart[0][0]), [0] * len(Dart[0][0][0]), [0] * len(Dart[0][0][0][0])]
	for i1 in range(len(Dart)):
		CheckNow1 = []
		for i2 in range(len(Dart[i1])):
			CheckNow2 = []
			for i3 in range(len(Dart[i1][i2])):
				CheckNow3 = []
				for i4 in range(len(Dart[i1][i2][i3])):
					TrueCheck[3][i4] += sum(Dart[i1][i2][i3][i4])
					CheckNow3.append(sum(Dart[i1][i2][i3][i4]))
					for i5 in range(len(Dart[i1][i2][i3][i4])):
						TrueCheck[4][i5] += Dart[i1][i2][i3][i4][i5]
				TrueCheck[2][i3] += sum(CheckNow3)
				CheckNow2.append(sum(CheckNow3))
			TrueCheck[1][i2] += sum(CheckNow2)
			CheckNow1.append(sum(CheckNow2))
		TrueCheck[0][i1] += sum(CheckNow1)
	for i in TrueCheck:
		flag = 0
		for j in i:
			if j > 0:
				flag += 1
		TrueSize.append(flag)
	b = 1
	for i in TrueSize:
		b = b * i
	if len(csv.index) < b:
		return False
	return check_has_single_sample(np.array(checkWeight))



def check_has_single_sample(hist_values):
    return 1 in hist_values.ravel()