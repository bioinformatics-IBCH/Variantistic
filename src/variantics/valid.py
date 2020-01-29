from variantics.constants import METADATA_VALID_VALUES
from variantics.lib import make_hist


def validation(csv):
    check_weight = [1] * len(csv)
    check_hist = make_hist(csv, check_weight)
    return 1 not in check_hist[0].ravel()


def check_meta(csv):
    for column in METADATA_VALID_VALUES.keys():
        for i in csv[column]:
            if i not in METADATA_VALID_VALUES[column]:
                return i, column
    return 0, 0
