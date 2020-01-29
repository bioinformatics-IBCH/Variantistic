import numpy as np

BINS = np.asarray([[-10000, 1, 25, 66, 10000], 3, 3])
CATEGORY_BINS = [[-10000, 1, 25, 66, 10000], ['M', 'F', 'U'], ['Diseased', 'Healthy', 'Unknown']]
CATEGORIAL_METADATA = ('Sex', 'Phenotype', 'Diseased')
SAMPLE_NAME_COLUMN = 'Sample name'
METADATA_VALID_VALUES = {
    'Age': range(-10000, 10000, 1),
    'Sex': {'M', 'F', 'U'},
    'Diseased': {'Diseased', 'Healthy', 'Unknown'}
}
