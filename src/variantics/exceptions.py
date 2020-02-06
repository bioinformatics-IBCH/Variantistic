class InvalidMetadataValueException(BaseException):
    def __init__(self, category):
        super().__init__(
            f'Not all values from {category.name} column of meta data are allowed.'
            f'Allowed values: {category.possible_values}'
        )


class AbsentObligatoryMetadataColumnException(BaseException):
    def __init__(self, category):
        super().__init__(
            f'Metadata file does not contain {category.name} column.'
            f'Please, specify all of the required meta data and rerun the program.'
        )


class ImpersonationValidationException(BaseException):
    def __init__(self):
        super().__init__(
            f'At least one sample with unique combination of meta data values exist.\n'
            f'We aim to guarantee, that a single sample genotypes could not be reconstructed from collected data.\n'
            f'We recommend to add more samples, so that no single sample had unique combination of meta data values, '
            f'or provide less detailed metadata.'
        )


class UnknownMetadataFormatException(BaseException):
    def __init__(self, metadata):
        super(UnknownMetadataFormatException, self).__init__(
            f'Unknown format of meta data {metadata}. Currently supported: csv, xlsx'
        )
