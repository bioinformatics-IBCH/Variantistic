import os
import pytest
from hist.lib import writing


@pytest.mark.parametrize('vhod, meta, expected', [
    ("/home/Welekie/newworkspace/variantics/MyTest/subdir/A.vcf", "/home/Welekie/newworkspace/variantics/MyTest/subdir/testik.csv","/home/Welekie/newworkspace/variantics/MyTest/subdir/A.exam.vcf"),
    
])
def test_sqrt(vhod, meta, expected):
    vihod = os.path.abspath('/home/Welekie/newworkspace/variantics/MyTest/subdir/A.processed.vcf')
    file = open(writing(vhod,meta, vihod))
    f = open(expected)
    for line in f:
        line1 = file.readline()
        assert line1 == line