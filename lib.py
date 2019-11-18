from pysam import VariantFile
import pandas 
import numpy as np
import matplotlib.pyplot as plt


def hist():

    
    file = open("A.vcf")
    
    f = open("header.vcf",'w')             # костыль, не знаю как по-другому
    flag = 0
    for i in file:
        if i[0] == '#':
            if i[2:6] == 'INFO' and flag == 0:
                f.write('##INFO=<ID=DP_hist,Description="Raw read depth">')
                flag = 1
            f.write(i)
        else:
            pass
    file.close()
    f.close() 
    f = VariantFile("header.vcf")
    vcf = VariantFile("A.vcf", header = f.header)
    csv = pandas.read_csv("testik.csv", sep=',')
#     vcf.header[58] = '##INFO=<ID=DP_hist,Description="Raw read depth">'
    output_vcf = VariantFile('MergeWithHist.vcf', 'w', header = f.header)
           
  
   
    for rec in vcf.fetch():
        for i in rec.info:
        DPM = []
        ACM = []
        ANM = []
        REC = rec.samples.keys()

        for i in REC:
            AC = 0
            AN = 0
            
            if rec.samples[i].get("DP", None) is not None:
                DPM.append(rec.samples[i]["DP"])
            else:
                DPM.append(0)
            GT = rec.samples[i].get("GT",'./.')

            for j in GT:

                if j == 1:
                    AC += 1
                    AN += 1
                elif j == 0:
                    AN += 1
            ACM.append(AC)
            ANM.append(AN)
        result = pandas.DataFrame({
            "Age": csv.Age.tolist(),
            "DiseaseId": csv.DiseaseId.tolist(),
            #         "Relativeness": csv.Relativeness,
            # "DP": DPM,
            # "AN": ANM,
            #         "AC": ACM
        }, index=csv["Sample name"])
        result = np.array(result)

        bins = np.asarray([4, 4])
        try:
            A = np.histogramdd(result, bins=bins, weights=DPM)
        except:
            print("Don't find DP in format",DPM)
            A = []

        try:
            B = np.histogramdd(result, bins=bins, weights=ANM)
            C = np.histogramdd(result, bins=bins, weights=ACM)
        except:
#             print("Don't find GT in format ")
            B = []
            C = []
        rec.info = rec.info + ';' + str(A)     # костыль, не знаю как нормально добавить гистограмы 
        
        output_vcf.write(rec)
        
    output_vcf.close()