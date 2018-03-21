import classify_lib as cll
import unittest
import pytest


def test_load_cutout_list():
    fnames = cll.load_cutout_list('testing/cutoutlist.dat')
    assert len(fnames) == 2
    assert fnames[0] == 'testing/testcutout.fits'
    assert fnames[1] == 'testing/testcutout2.fits'


def test_gals_done():
    fnames = cll.load_cutout_list('testing/cutoutlist.dat')
    fnames = cll.gals_done(fnames, testing='testing/')
    assert len(fnames) == 1
    assert fnames[0] == 'testing/testcutout2.fits'


class TestClassifyGal(unittest.TestCase):
    def test1(self):
        original_raw_input = raw_input
        __builtins__['raw_input'] = lambda _: '1/3'
        self.assertEqual(cll.classify_gal(), '1/3')
        __builtins__['raw_input'] = original_raw_input

    def test2(self):
        original_raw_input = raw_input
        __builtins__['raw_input'] = lambda _: '-2'
        self.assertEqual(cll.classify_gal(), '-2')
        __builtins__['raw_input'] = original_raw_input


class TestAddFlags(unittest.TestCase):
    def test1(self):
        original_raw_input = raw_input
        __builtins__['raw_input'] = lambda _: '123'
        self.assertEqual(cll.set_flags(), '123')
        __builtins__['raw_input'] = original_raw_input

    def test2(self):
        original_raw_input = raw_input
        __builtins__['raw_input'] = lambda _: '6'
        self.assertEqual(cll.set_flags(), '6')
        __builtins__['raw_input'] = original_raw_input

    def test3(self):
        original_raw_input = raw_input
        __builtins__['raw_input'] = lambda _: ''
        self.assertEqual(cll.set_flags(), '')
        __builtins__['raw_input'] = original_raw_input


def test_pipeline():
    original_raw_input = raw_input
    __builtins__['raw_input'] = lambda _: '3'
    cll.run_classify('testing/')

    # Check the output file
    with open('testing/results.dat') as fres:
        res = fres.readlines()
    assert res[0] == 'testing/testcutout.fits 3 3\n'
    assert res[1] == 'testing/testcutout2.fits 3 3\n'

    # Reset the results file
    with open('testing/results.dat', 'w') as fres:
        fres.write('testing/testcutout.fits 3 3\n')

    __builtins__['raw_input'] = original_raw_input


@pytest.mark.skip()
def test_display_gal(capsys):
    cll.display_gal('')
    captured = capsys.readouterr()
    assert not captured[0] == "DISPLAY NOT SET UP\n"
