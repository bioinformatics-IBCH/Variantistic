import numpy as np
from variantics.categories import CATEGORIES, ACCESSORIAL_CATEGORIES
from variantics.exceptions import (
    InvalidMetadataValueException,
    AbsentObligatoryMetadataColumnException,
    ImpersonationValidationException)
from variantics.lib import HistogramCreator, read_metadata


def is_impersonal(csv):
    """
    Checks whether any collected slice with a single sample exists.
    Args:
        csv:

    Returns:

    """
    creator = HistogramCreator(multisample_vcf=None, metadata=csv, output_path=None)
    t_size = len(creator.processor.encoded_csv)
    bins, edges = creator.process_record(
        record=None,
        configuration={
            # each sample gets a weight of 1
            'callable': lambda x: [1] * t_size
        }
    )

    return 1 not in np.array(bins).ravel()


def validate_metadata(csv):
    metadata = read_metadata(csv)
    for category in CATEGORIES + ACCESSORIAL_CATEGORIES:
        if category.name not in metadata.columns:
            raise AbsentObligatoryMetadataColumnException(category)

        all_valid_values = all([category.is_value_allowed(value) for value in metadata[category.name].unique()])

        if not all_valid_values:
            raise InvalidMetadataValueException(category)

    if not is_impersonal(metadata):
        raise ImpersonationValidationException()

    return True
