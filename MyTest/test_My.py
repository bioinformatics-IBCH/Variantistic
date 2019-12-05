import os
import pytest
from hist.lib import hist, makeHist, prepare_meta, inverse
from hist.valid import validation, Check_meta
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
[[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[99.0, 0.0, 0.0], [99.0, 0.0, 198.0], [0.0, 0.0, 0.0]], [[198.0, 495.0, 0.0], [99.0, 198.0, 297.0], [0.0, 198.0, 0.0]], [[99.0, 297.0, 99.0], [0.0, 198.0, 99.0], [0.0, 0.0, 0.0]]] ),
])

def test_DPhist(DPM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,DPM)
    A = Var[0]
    assert A.tolist() == expected

@pytest.mark.parametrize('DPM, meta, expected', [
    ([99, 99, 99, 0, 0, 99, 99, 0, 99, 99, 0, 99, 99, 0, 99, 99, 99, 0, 0, 99, 0, 99, 0, 0, 99, 99, 99, 99, 99, 99, 0, 0, 0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]]),
    (
    [99, 990, 99, 10, 0, 919, 199, 10, 919, 99, 0, 99, 99, 10, 99, 99, 99, 10, 0, 99, 0, 99, 0, 0, 99, 99, 99, 99, 99, 99, 0, 0,
     0, 99, 99, 0, 99, 99, 0, 0, 99, 99, 99, 0],
    "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0],
     [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]])
])

def test_DPedges(DPM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,DPM)
    A = Var[1]
    assert A == expected

@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
[[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]], [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 6.0, 0.0]], [[2.0, 6.0, 4.0], [0.0, 4.0, 2.0], [0.0, 0.0, 0.0]]])])
def test_ANhist(ANM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,ANM)
    A = Var[0]
    assert A.tolist() == expected



@pytest.mark.parametrize('ANM, meta, expected', [
    ([2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0],
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
     [[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]])])


def test_ANedges(ANM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,ANM)
    A = Var[1]
    assert A == expected


@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
[[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]], [[2.0, 0.0, 0.0], [2.0, 0.0, 4.0], [0.0, 0.0, 0.0]], [[4.0, 10.0, 0.0], [2.0, 4.0, 6.0], [0.0, 2.0, 0.0]], [[2.0, 6.0, 3.0], [0.0, 3.0, 2.0], [0.0, 0.0, 0.0]]] )])
def test_AChist(ACM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,ACM)
    A = Var[0]
    assert A.tolist() == expected



@pytest.mark.parametrize('ACM, meta, expected', [
    ([1, 0, 2, 0, 0, 2, 2, 0, 2, 2, 1, 2, 2, 0, 2, 2, 2, 0, 0, 2, 0, 2, 0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 2, 2, 0, 2, 2, 0, 0, 2, 2, 2, 0] ,
     "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv",
    [[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]])
])


def test_ACedges(ACM, meta, expected):
    result = prepare_meta(meta)
    Var = makeHist(result,ACM)
    A = Var[1]
    assert A == expected

@pytest.mark.parametrize('MasBin, expected', [
    ([[-10000, 1, 25, 66, 10000], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0], [0.0, 0.6666666666666666, 1.3333333333333333, 2.0]],
    [[-10000, 1, 25, 66, 10000], ["M", "F", "U"], ["Diseased", "Healthy", "Unknown"]])
])


def test_inversion(MasBin, expected):
    NewMasBin = inverse(MasBin)
    assert NewMasBin == expected

@pytest.mark.parametrize('meta', ["/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv","/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv","/home/Welekie/newworkspace/variantics/MyTest/subdir/testic1.csv"] )


def test_validation(meta):
    csv = prepare_meta(meta)

    assert not validation(csv)



@pytest.mark.parametrize('meta', ["/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv","/home/Welekie/newworkspace/variantics/MyTest/subdir/testic1.csv"])
def test_Check_meta(meta):
    csv = pandas.read_csv(meta)
    miss,column = Check_meta(csv)
    assert miss == 0 and column == 0