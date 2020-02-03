import os

from variantics.exceptions import InvalidMetadataValueException, AbsentObligatoryMetadataColumnException
from variantics.lib import HistogramCreator, read_vcf, read_metadata
from variantics.validation import is_impersonal, validate_metadata

import pandas
import pytest

TEST_VCF_PATH = 'tests/resources/A.vcf'
TEST_METADATA_VCF_PATH = 'tests/resources/testik.csv'
TEST_PROCESSED_VCF_PATH = 'tests/resources/A.exam.vcf'


@pytest.mark.parametrize(
    'input, meta, expected',
    [
        (
            TEST_VCF_PATH,
            TEST_METADATA_VCF_PATH,
            TEST_PROCESSED_VCF_PATH
        ),
    ]
)
def test_output(input, meta, expected):
    vihod = os.path.abspath('tests/resources/A.processed.vcf')
    file = open(HistogramCreator(input, meta, vihod)())
    f = open(expected)
    for line in f:
        line1 = file.readline()
        assert line1 == line


@pytest.mark.parametrize(
    'vcf, metadata, configuration, expected_hist, expected_edges',
    [
        (
            TEST_VCF_PATH,
            TEST_METADATA_VCF_PATH,
            HistogramCreator.PARAMETER_CONFIG['DP'],
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[99.0, 0.0, 0.0], [99.0, 0.0, 198.0], [0.0, 0.0, 0.0]],
                [[198.0, 495.0, 0.0], [99.0, 198.0, 297.0], [0.0, 198.0, 0.0]],
                [[99.0, 297.0, 99.0], [0.0, 198.0, 99.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], ['F', 'M', 'U'], ['Diseased', 'Healthy', 'Unknown']
            ]
        ),
        (
            TEST_VCF_PATH,
            TEST_METADATA_VCF_PATH,
            HistogramCreator.PARAMETER_CONFIG['AN'],
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]],
                [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 6.0, 0.0]],
                [[2.0, 6.0, 4.0], [0.0, 4.0, 2.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], ['F', 'M', 'U'], ['Diseased', 'Healthy', 'Unknown']
            ]
        ),
        (
            TEST_VCF_PATH,
            TEST_METADATA_VCF_PATH,
            HistogramCreator.PARAMETER_CONFIG['AC'],
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]],
                [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 2.0, 0.0]],
                [[2.0, 6.0, 3.0], [0.0, 3.0, 2.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], ['F', 'M', 'U'], ['Diseased', 'Healthy', 'Unknown']
            ]
        )
    ]
)
def test_hist(vcf, metadata, configuration, expected_hist, expected_edges):
    vcf_in = read_vcf(vcf)
    bins, edges = HistogramCreator(
        multisample_vcf=None,
        metadata=metadata,
        output_path=None
    ).process_record(next(vcf_in), configuration)

    assert bins == expected_hist
    assert edges == expected_edges


@pytest.mark.parametrize('meta', [TEST_METADATA_VCF_PATH])
def test_validation(meta):
    assert not is_impersonal(meta)


@pytest.mark.parametrize('meta', [
    pandas.DataFrame(
        {
            'Sex': ['M', 'M'],
            'Age': [10, 15],
            'Diseased': ['Diseased', 'Diseased'],
            'Sample name': ['S1', 'S2']
        }
    )
])
def test_check_meta(meta):
    csv = read_metadata(meta)
    assert validate_metadata(csv)


@pytest.mark.parametrize('metadata', [
    pandas.DataFrame(
        {
            'Sex': ['M', 'F', 'Inv'],
            'Age': [1, 2, 3],
            'Diseased': ['Diseased', 'Diseased', 'Inv']
        }
    )
])
def test_invalid_metadata(metadata):
    with pytest.raises(InvalidMetadataValueException):
        validate_metadata(metadata)


@pytest.mark.parametrize('metadata', [
    pandas.DataFrame(
        {
            'Sex': ['M', 'F', 'Inv']
        }
    )
])
def test_absent_metadata(metadata):
    with pytest.raises(AbsentObligatoryMetadataColumnException):
        validate_metadata(metadata)
