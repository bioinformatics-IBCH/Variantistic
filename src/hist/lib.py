import pandas
import numpy as np
from cyvcf2 import VCF, Writer
import os
import subprocess
import json
import pytest


def writing(vhod,meta,vihod):
	csv = pandas.read_csv(meta, sep=',')
	vcf_in = VCF(vhod)
	vcf_in.add_info_to_header(
		{
			'ID': 'VARIANTICS_HIST',
			'Description': '...',
			'Type': 'String',
			'Number': 1
		}
	)

	vcf_out = Writer(os.path.abspath(vihod), vcf_in)
	for rec in vcf_in:
		ANM = []
		ACM = []
		DPM = []
		DPM1 = rec.format('DP')
		for i in range(len(DPM1)):
			if DPM1[i][0] >= 0:
				DPM.append(DPM1[i][0])
			else:
				DPM.append(0)

		GT = rec.gt_types

		for sample in GT:
			AC = 0
			AN = 0
			if sample == 0:

				AN += 2
			elif sample == 1:
				AC += 1
				AN += 2
			elif sample == 3:
				AN += 2
				AC += 2
			ACM.append(AC)
			ANM.append(AN)

		result = pandas.DataFrame({
			"Age": csv.Age.tolist(),
			"DiseaseId": csv.DiseaseId.tolist(),
			#         "Relativeness": csv.Relativeness,
		}, index=csv["Sample name"])
		result = np.array(result)
		bins = np.asarray([4, 4])
		try:
			A = np.histogramdd(result, bins=bins, weights=DPM)
		except:
			#         print('Don't find DP in format)
			A = [np.array([]), []]

		try:
			B = np.histogramdd(result, bins=bins, weights=ANM)
			C = np.histogramdd(result, bins=bins, weights=ACM)
		except:
			#       print('Don't find GT in format)
			B = [[], []]
			C = [[], []]

		list = [A, B, C]
		for i in list:
			for j in range(len(i[1])):
				i[1][j] = i[1][j].tolist()

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

	return os.path.abspath(vihod)