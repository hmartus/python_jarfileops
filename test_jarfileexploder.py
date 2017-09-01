import unittest
from jarfileexploder import read_zipfile, search_zipfile, to_json

JARFILE='sample.jar'
EXTNAME='.java'
VALUE1 = {1: 'asdas ads dsa dsa dsa dsa dsa dsa version asd adas', 6: 'sda asd a version'}
VALUE2 = {2: 'asdsa versions', 4: 'asd asda sda  versionsad'}
JSONVALUE = '[{"sample2.java": {"1": "asdas ads dsa dsa dsa dsa dsa dsa version asd adas", ' \
            '"6": "sda asd a version"}}, {"sample.java": {"2": "asdsa versions", "4": ' \
            '"asd asda sda  versionsad"}}]'

class Read_ZipfileTestCase(unittest.TestCase):
    """ tests for read_zipfile """

    def test_getFiles(self):
        tmp = [i for i in read_zipfile(JARFILE, EXTNAME)]
        self.assertEqual(tmp[0], 'sample2.java')
        self.assertEqual(tmp[1], 'sample.java')

    def test_raises_Exceptions(self):
        with self.assertRaises(StopIteration):
            self.assertTrue( next(read_zipfile(JARFILE,'javac')))
        with self.assertRaises(FileNotFoundError):
            self.assertTrue( next(read_zipfile('asdasda','javac')))

class Search_ZipfileTestCase(unittest.TestCase):

    def test_search(self):
        tmp = [i for i in search_zipfile(JARFILE, EXTNAME, b'version')]
        self.assertDictEqual(tmp[0].get('sample2.java'), VALUE1)
        self.assertDictEqual(tmp[1].get('sample.java'), VALUE2)

class To_JsonTestCase(unittest.TestCase):

    def test_to_json(self):
        tmp = to_json(JARFILE, EXTNAME, b'version')
        self.assertEqual(tmp, JSONVALUE)

if __name__ == '__main__':
    unittest.main()