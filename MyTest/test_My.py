import os
import pytest
from hist.lib import hist, makeHist, prepare_meta, inverse

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
[[[[[0.0, 0.0], [0.0, 0.0], [99.0, 0.0], [0.0, 99.0]], [[0.0, 99.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 198.0], [99.0, 0.0], [99.0, 99.0]], [[99.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 99.0], [0.0, 0.0], [0.0, 0.0], [0.0, 99.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 198.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [99.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 99.0]], [[0.0, 99.0], [198.0, 0.0], [0.0, 198.0], [0.0, 0.0]], [[99.0, 0.0], [99.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [0.0, 99.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [99.0, 0.0]], [[99.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [99.0, 99.0], [0.0, 0.0], [0.0, 0.0]]]]]
   ),
])

def test_DPhist(DPM, meta, expected):
    result,catalog = prepare_meta(meta)
    Var = makeHist(result,DPM)
    A = Var[0]
    assert A.tolist() == expected

@pytest.mark.parametrize('DPM, meta, expected', [
    ([99, 99, 99, 0, 0, 99, 99, 0, 99, 99, 0, 99, 99, 0, 99, 99, 99, 0, 0, 99, 0, 99, 0, 0, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[10.0, 33.0, 56.0, 79.0, 102.0], [0.0, 2.0], [1.0, 3.5, 6.0, 8.5, 11.0], [0.01, 0.255, 0.5, 0.745, 0.99], [0.0, 0.5, 1.0]])])


def test_DPedges(DPM, meta, expected):
    result, catalog = prepare_meta(meta)
    Var = makeHist(result,DPM)
    A = Var[1]
    assert A == expected

@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[[[[0.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 2.0]], [[0.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 4.0], [2.0, 0.0], [2.0, 2.0]], [[2.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 4.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]], [[0.0, 2.0], [4.0, 0.0], [0.0, 4.0], [0.0, 0.0]], [[2.0, 0.0], [2.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [0.0, 2.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [2.0, 0.0]], [[2.0, 0.0], [2.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [2.0, 2.0], [0.0, 0.0], [0.0, 0.0]]]]])])


def test_ANhist(ANM, meta, expected):
    result, catalog = prepare_meta(meta)
    Var = makeHist(result,ANM)
    A = Var[0]
    assert A.tolist() == expected



@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[10.0, 33.0, 56.0, 79.0, 102.0], [0.0, 2.0], [1.0, 3.5, 6.0, 8.5, 11.0], [0.01, 0.255, 0.5, 0.745, 0.99], [0.0, 0.5, 1.0]])
])


def test_ANedges(ANM, meta, expected):
    result, catalog = prepare_meta(meta)
    Var = makeHist(result,ANM)
    A = Var[1]
    assert A == expected


@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[[[[0.0, 0.0], [0.0, 0.0], [2.0, 0.0], [0.0, 2.0]], [[0.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 4.0], [2.0, 0.0], [2.0, 2.0]], [[2.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 2.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 4.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [0.0, 2.0]], [[0.0, 2.0], [4.0, 0.0], [0.0, 4.0], [0.0, 0.0]], [[2.0, 0.0], [2.0, 0.0], [0.0, 0.0], [0.0, 0.0]]]], [[[[0.0, 0.0], [0.0, 0.0], [0.0, 1.0], [0.0, 0.0]], [[0.0, 0.0], [0.0, 0.0], [0.0, 0.0], [2.0, 0.0]], [[2.0, 0.0], [1.0, 0.0], [0.0, 0.0], [0.0, 0.0]], [[0.0, 0.0], [2.0, 2.0], [0.0, 0.0], [0.0, 0.0]]]]])])


def test_AChist(ACM, meta, expected):
    result, catalog = prepare_meta(meta)
    Var = makeHist(result,ACM)
    A = Var[0]
    assert A.tolist() == expected



@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[10.0, 33.0, 56.0, 79.0, 102.0], [0.0, 2.0], [1.0, 3.5, 6.0, 8.5, 11.0], [0.01, 0.255, 0.5, 0.745, 0.99], [0.0, 0.5, 1.0]])
])


def test_ACedges(ACM, meta, expected):
    result, catalog = prepare_meta(meta)
    Var = makeHist(result,ACM)
    A = Var[1]
    assert A == expected

@pytest.mark.parametrize('MasBin, Categories, expected', [
    ([[10.0, 33.0, 56.0, 79.0, 102.0], [0.0, 2.0], [1.0, 3.5, 6.0, 8.5, 11.0], [0.01, 0.255, 0.5, 0.745, 0.99], [0.0, 0.5, 1.0]] ,
     [['F', 'M'],['In', 'N', 'O']],
    [[10.0, 33.0, 56.0, 79.0, 102.0], ["F", "M"], [1.0, 3.5, 6.0, 8.5, 11.0], [0.01, 0.255, 0.5, 0.745, 0.99], ["In", "N", "O"]])
])


def test_inversion(MasBin, Categories, expected):
    NewMasBin = inverse(MasBin, Categories)
    assert NewMasBin == expected