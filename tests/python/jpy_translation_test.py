# This file was modified by Illumon.
import unittest
from os import path # <AK> added

from jt import jpyutil

from . import test_dir  # <AK> added
jpyutil.init_jvm(jvm_maxmem='512M', jvm_classpath=[path.join(test_dir,"java","classes")])
import jpy

class DummyWrapper:
    def __init__(self, theThing):
        self.theThing = theThing

    def getValue(self):
        return 2 * self.theThing.getValue()

def make_wrapper(type, thing):
    return DummyWrapper(thing)
     

class TestTypeTranslation(unittest.TestCase):
    def setUp(self):
        self.Fixture = jpy.get_type('org.jpy.fixtures.TypeTranslationTestFixture')
        self.assertIsNotNone(self.Fixture)

    def test_Translation(self):
        fixture = self.Fixture()
        thing = fixture.makeThing(7)
        self.assertEqual(thing.getValue(), 7)
        self.assertEquals(repr(type(thing)), "<type 'org.jpy.fixtures.Thing'>")

        jpy.type_translations['org.jpy.fixtures.Thing'] = make_wrapper
        thing = fixture.makeThing(8)
        self.assertEqual(thing.getValue(), 16)
        self.assertEqual(type(thing), type(DummyWrapper(None)))

        jpy.type_translations['org.jpy.fixtures.Thing'] = None
        self.assertEqual(fixture.makeThing(9).getValue(), 9)


if __name__ == '__main__':
    print('\nRunning ' + __file__)
    unittest.main()
