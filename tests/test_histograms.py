import os

from variantics.lib import hist, make_hist, prepare_meta, inverse
from variantics.validation import validation, check_meta

import pandas
import pytest

dpm_input = [
    99, 99, 99, 0, 0, 99, 99, 0, 99, 99, 0, 99, 99, 0, 99, 99, 99, 0, 0, 99, 0, 99,
    0, 0, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0
]

an_input = [
    2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2,
    0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0
]

ac_input = [
    1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2,
    0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0
]


@pytest.mark.parametrize('input, meta, expected', [
    ('tests/resources/A.vcf',
     'tests/resources/testik.csv',
     'tests/resources/A.exam.vcf'),
])
def test_output(input, meta, expected):
    vihod = os.path.abspath('tests/resources/A.processed.vcf')
    file = open(hist(input, meta, vihod))
    f = open(expected)
    for line in f:
        line1 = file.readline()
        assert line1 == line


@pytest.mark.parametrize(
    'input, meta, expected_hist, expected_edges',
    [
        (
            dpm_input,
            'tests/resources/testik.csv',
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[99.0, 0.0, 0.0], [99.0, 0.0, 198.0], [0.0, 0.0, 0.0]],
                [[198.0, 495.0, 0.0], [99.0, 198.0, 297.0], [0.0, 198.0, 0.0]],
                [[99.0, 297.0, 99.0], [0.0, 198.0, 99.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0],
                [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]
            ]
        ),
        (
            an_input,
            'tests/resources/testik.csv',
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]],
                [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 6.0, 0.0]],
                [[2.0, 6.0, 4.0], [0.0, 4.0, 2.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0],
                [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]
            ]
        ),
        (
            ac_input,
            'tests/resources/testik.csv',
            [
                [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]],
                [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]],
                [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 2.0, 0.0]],
                [[2.0, 6.0, 3.0], [0.0, 3.0, 2.0], [0.0, 0.0, 0.0]]
            ],
            [
                [-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0],
                [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]
            ]
        )
    ]
)
def test_hist(input, meta, expected_hist, expected_edges):
    result = prepare_meta(meta)
    hist = make_hist(result, input)
    assert hist[0].tolist() == expected_hist
    assert hist[1] == expected_edges


@pytest.mark.parametrize('mas_bin, expected', [
    ([[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0],
      [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]],
     [[-10000, 1, 25, 66, 10000], ['M', 'F', 'U'], ['Diseased', 'Healthy', 'Unknown']])
])
def test_inversion(mas_bin, expected):
    new_mas_bin = inverse(mas_bin)
    assert new_mas_bin == expected


@pytest.mark.parametrize('meta', ['tests/resources/testik.csv'])
def test_validation(meta):
    csv = prepare_meta(meta)

    assert not validation(csv)


@pytest.mark.parametrize('meta', ['tests/resources/testik.csv'])
def test_check_meta(meta):
    csv = pandas.read_csv(meta)
    miss, column = check_meta(csv)
    assert miss == 0 and column == 0
