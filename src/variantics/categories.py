from dataclasses import dataclass, field

import numpy as np
from sklearn.preprocessing import LabelEncoder

from variantics.constants import SAMPLE_NAME_COLUMN


@dataclass
class Category:
    name: str
    bins: list = field(default_factory=list)
    categorical: bool = False
    encoder: LabelEncoder = None
    possible_values: list = field(default_factory=list)

    def __post_init__(self):
        if not self.bins:
            return

        self.possible_values = self.bins if self.categorical else range(min(self.bins), max(self.bins))
        if self.categorical:
            self.encoder = LabelEncoder()
            self.encoder.fit(self.bins)
            self.encoded_bins = self.encoder.transform(self.bins)
            # Bin edges should include left edge of first bin and right edge of last bin
            self.encoded_bins = np.append(self.encoded_bins, max(self.encoded_bins) + 1)
        else:
            self.encoded_bins = self.bins

    def is_value_allowed(self, value):
        if self.possible_values:
            return value in self.possible_values
        return True


CATEGORIES = [
    Category(
        name='Age',
        bins=[-10000, 1, 25, 66, 10000],
        categorical=False
    ),
    Category(
        name='Sex',
        bins=['M', 'F', 'U'],
        categorical=True
    ),
    Category(
        name='Diseased',
        bins=['Diseased', 'Healthy', 'Unknown'],
        categorical=True
    )
]

ACCESSORIAL_CATEGORIES = [
    Category(
        name=SAMPLE_NAME_COLUMN
    )
]

# bins for numpy.histogramdd
# i.e. [[-10000, 1, 25, 66, 10000], [1,2,3], [1,2,3]]
BINS = [
    sorted(category.encoded_bins)
    for category in CATEGORIES
]
