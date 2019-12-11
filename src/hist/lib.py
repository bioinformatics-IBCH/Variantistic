import pandas
import numpy as np
from cyvcf2 import VCF, Writer
import json
from sklearn.preprocessing import OrdinalEncoder
from hist.Const import bins

def hist(vhod,meta,vihod):
	vcf_in = reading(vhod)
	vcf_out = Writer(vihod, vcf_in)
	result = prepare_meta(meta)
	for rec in vcf_in:
		DPM = prepare_DP(rec)
		A = makeHist(result,DPM)
		ANM = prepare_AN(rec)
		B = makeHist(result, ANM)
		ACM = prepare_AC(rec)
		C = makeHist(result, ACM)
		VARIANTICS_HIST = json.dumps(
			{
				'DP_HIST': {
					'hist': A[0].tolist(),
					'edges': A[1]
				},
				'AN_HIST': {
					'hist': B[0].tolist(),
					'edges': B[1]
				},
				'AC_HIST': {
					'hist': C[0].tolist(),
					'edges': C[1]
				}
			}
		)
		rec.INFO["VARIANTICS_HIST"] = VARIANTICS_HIST
		vcf_out.write_record(rec)
	vcf_in.close()
	vcf_out.close()
	return vihod


def reading(vhod):
	vcf_in = VCF(vhod)
	vcf_in.add_info_to_header(
		{
			'ID': 'VARIANTICS_HIST',
			'Description': '...',
			'Type': 'String',
			'Number': 1
		}
	)
	return vcf_in


def prepare_meta(meta):
	csv = pandas.read_csv(meta, sep=',')
	enc = OrdinalEncoder()
	X = csv.loc[:, ("Sex", "Phenotype")]
	enc.fit(X)
	Y = enc.transform(X)
	sex = []
	Phen = []
	for i in Y:
		sex.append(i[0])
		Phen.append(i[1])
	result = pandas.DataFrame({
		"Age": csv.Age.tolist(),
		"Phenotype": Phen,
		"DiseaseId": csv.DiseaseId.tolist(),
		"Relativeness": csv.Relativeness.tolist(),
		"Sex": sex
	}, index=csv["Sample name"])
	result = np.array(result)
	return result


def prepare_DP(rec):
	DPM1 = rec.format('DP')
	DPM = []
	for i in range(len(DPM1)):
		if DPM1[i][0] >= 0:
			DPM.append(DPM1[i][0])
		else:
			DPM.append(0)
	return DPM


def prepare_AN(rec):
	GT = rec.gt_types
	ANM = []
	for sample in GT:
		AN = 0
		if sample == 0:
			AN += 2
		elif sample == 1:
			AN += 2
		elif sample == 3:
			AN += 2
		ANM.append(AN)
	return ANM


def prepare_AC(rec):
	GT = rec.gt_types
	ACM = []
	for sample in GT:
		AC = 0
		if sample == 1:
			AC += 1
		elif sample == 3:
			AC += 2
		ACM.append(AC)
	return ACM


def makeHist(result,weight):
	A = np.histogramdd(result, bins=bins, weights=weight)
	for j in range(len(A[1])):
		A[1][j] = A[1][j].tolist()
	return A
def writing():
	return 0