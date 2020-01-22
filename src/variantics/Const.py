import numpy as np
Bins = np.asarray([[-10000,1,25,66,10000],3,3])
TrueBins = [[-10000,1,25,66,10000],['M','F','U'],['Diseased','Healthy','Unknown']]
categorial_metadata = ("Sex", "Phenotype","Diseased")
sample_name = 'Sample name'
imp_meta = ["Age","Sex","Diseased"]
imp_meta_border = {
    'Age': [-10000,10000],
    'Sex': {'M','F','U'},
    'Diseased': {'Diseased','Healthy','Unknown'}
}