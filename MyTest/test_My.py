import os
import pytest
from hist.lib import hist, makeHist

import numpy as np
import pandas

@pytest.mark.parametrize('vhod, meta, expected', [
    ("/home/Welekie/newworkspace/variantics/MyTest/subdir/A.vcf",
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/A.exam.vcf"),
    
])
def test_zapis(vhod, meta, expected):
    vihod = os.path.abspath('/home/Welekie/newworkspace/variantics/MyTest/subdir/A.processed.vcf')
    file = open(hist(vhod,meta, vihod))
    f = open(expected)
    for line in f:
        line1 = file.readline()
        assert line1 == line


@pytest.mark.parametrize('DPM, meta, expected', [
    ([99, 99, 99, 0, 0, 99, 99, 0, 99, 99, 0, 99, 99, 0, 99, 99, 99, 0, 0, 99, 0, 99, 0, 0, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[198.0, 99.0, 495.0, 99.0], [198.0, 0.0, 0.0, 198.0], [99.0, 99.0, 495.0, 198.0], [99.0, 99.0, 99.0, 198.0]]),
    ([12, 988, 99, 123, 0, 99, 99, 10, 99, 1, 0, 99, 29, 0, 99, 49, 49, 0, 36, 94, 0, 99, 0, 3, 99, 99, 99, 99, 9, 99, 0, 0, 0, 909, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[198.0, 99.0, 440.0, 99.0], [100.0, 123.0, 10.0, 128.0], [988.0, 99.0, 495.0, 1008.0], [12.0, 138.0, 9.0, 148.0]])

])


def test_DP(DPM, meta, expected):
    Var = makeHist(meta,DPM)
    A = Var['DP_HIST']['hist']
    assert A.tolist() == expected

@pytest.mark.parametrize('DPM, meta, expected', [
    ([99, 99, 99, 0, 0, 99, 99, 0, 99, 99, 0, 99, 99, 0, 99, 99, 99, 0, 0, 99, 0, 99, 0, 0, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[10.0, 33.0, 56.0, 79.0, 102.0], [1.0, 3.5, 6.0, 8.5, 11.0]])])


def test_DP(DPM, meta, expected):
    Var = makeHist(meta,DPM)
    A = Var['DP_HIST']['edges']
    assert A.tolist() == expected

@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[4.0, 2.0, 10.0, 2.0], [4.0, 0.0, 2.0, 4.0], [2.0, 2.0, 10.0, 4.0], [2.0, 2.0, 4.0, 4.0]])])


def test_AN(ANM, meta, expected):
    Var = makeHist(meta,ANM)
    A = Var['AN_HIST']['hist']
    assert A.tolist() == expected



@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[10.0, 33.0, 56.0, 79.0, 102.0], [1.0, 3.5, 6.0, 8.5, 11.0]])
])


def test_AN(ANM, meta, expected):
    Var = makeHist(meta,ANM)
    A = Var['AN_HIST']['edges']
    assert A.tolist() == expected


@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[4.0, 2.0, 10.0, 2.0], [4.0, 0.0, 0.0, 4.0], [0.0, 2.0, 10.0, 4.0], [1.0, 2.0, 3.0, 4.0]])])


def test_AC(ACM, meta, expected):
    Var = makeHist(meta,ACM)
    A = Var['AC_HIST']['hist']
    assert A.tolist() == expected



@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[10.0, 33.0, 56.0, 79.0, 102.0], [1.0, 3.5, 6.0, 8.5, 11.0]])
])


def test_AC(ACM, meta, expected):
    Var = makeHist(meta,ACM)
    A = Var['AC_HIST']['hist']
    assert A.tolist() == expected

