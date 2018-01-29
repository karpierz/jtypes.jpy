import unittest
import os

testd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
import jt.jpyutil as jpyutil
jpyutil.init_jvm(jvm_maxmem='512M', jvm_classpath=[os.path.join(testd,"java","classes")])
import jt.jpy as jpy


class TestConstructorOverloads(unittest.TestCase):

    def setUp(self):
        self.Fixture = jpy.get_type('org.jpy.fixtures.ConstructorOverloadTestFixture')
        self.assertIsNotNone(self.Fixture)

    def test_FloatConstructors(self):
        fixture = self.Fixture()
        self.assertEqual(fixture.getState(), '')

        fixture = self.Fixture(12)
        self.assertEqual(fixture.getState(), 'Integer(12)')

        fixture = self.Fixture(12, 34)
        self.assertEqual(fixture.getState(), 'Integer(12),Integer(34)')

        fixture = self.Fixture(0.12)
        self.assertEqual(fixture.getState(), 'Float(0.12)')

        fixture = self.Fixture(0.12, 0.34)
        self.assertEqual(fixture.getState(), 'Float(0.12),Float(0.34)')

        fixture = self.Fixture(0.12, 34)
        self.assertEqual(fixture.getState(), 'Float(0.12),Integer(34)')

        fixture = self.Fixture(12, 0.34)
        self.assertEqual(fixture.getState(), 'Integer(12),Float(0.34)')

        with self.assertRaises(RuntimeError, msg='RuntimeError expected') as e:
            fixture = self.Fixture(12, '34')
        self.assertEqual(str(e.exception), 'no matching Java method overloads found')


class TestMethodOverloads(unittest.TestCase):

    def setUp(self):
        self.Fixture = jpy.get_type('org.jpy.fixtures.MethodOverloadTestFixture')
        self.assertIsNotNone(self.Fixture)

    def test_2ArgOverloadsWithVaryingTypes(self):
        fixture = self.Fixture()

        self.assertEqual(fixture.join(12, 32), 'Integer(12),Integer(32)')
        self.assertEqual(fixture.join(12, 3.2), 'Integer(12),Double(3.2)')
        self.assertEqual(fixture.join(12, 'abc'), 'Integer(12),String(abc)')
        self.assertEqual(fixture.join(1.2, 32), 'Double(1.2),Integer(32)')
        self.assertEqual(fixture.join(1.2, 3.2), 'Double(1.2),Double(3.2)')
        self.assertEqual(fixture.join(1.2, 'abc'), 'Double(1.2),String(abc)')
        self.assertEqual(fixture.join('efg', 32), 'String(efg),Integer(32)')
        self.assertEqual(fixture.join('efg', 3.2), 'String(efg),Double(3.2)')
        self.assertEqual(fixture.join('efg', 'abc'), 'String(efg),String(abc)')

        with self.assertRaises(RuntimeError, msg='RuntimeError expected') as e:
            fixture.join(object(), 32)
        self.assertEqual(str(e.exception), 'no matching Java method overloads found')

    def test_nArgOverloads(self):
        fixture = self.Fixture()

        self.assertEqual(fixture.join('x'), 'String(x)')
        self.assertEqual(fixture.join('x', 'y'), 'String(x),String(y)')
        self.assertEqual(fixture.join('x', 'y', 'z'), 'String(x),String(y),String(z)')

        with self.assertRaises(RuntimeError, msg='RuntimeError expected') as e:
            fixture.join('x', 'y', 'z', 'u')
        self.assertEqual(str(e.exception), 'no matching Java method overloads found')

    def test_nArgOverloadsAreFoundInBaseClass(self):
        Fixture = jpy.get_type('org.jpy.fixtures.MethodOverloadTestFixture$MethodOverloadTestFixture2')
        fixture = Fixture()

        self.assertEqual(fixture.join('x'), 'String(x)')
        self.assertEqual(fixture.join('x', 'y'), 'String(x),String(y)')
        self.assertEqual(fixture.join('x', 'y', 'z'), 'String(x),String(y),String(z)')
        self.assertEqual(fixture.join('x', 'y', 'z', 'u'), 'String(x),String(y),String(z),String(u)')

        with self.assertRaises(RuntimeError, msg='RuntimeError expected') as e:
            fixture.join('x', 'y', 'z', 'u', 'v')
        self.assertEqual(str(e.exception), 'no matching Java method overloads found')


class TestOtherMethodResolutionCases(unittest.TestCase):

    # see https://github.com/bcdev/jpy/issues/55
    def test_toReproduceAndFixIssue55(self):
        Paths = jpy.get_type('java.nio.file.Paths')
        # The following outcommented statement is will end in a Python error
        # RuntimeError: no matching Java method overloads found
        #p = Paths.get('testfile')
        # This is the embarrassing workaround
        p = Paths.get('testfile', [])

    # see https://github.com/bcdev/jpy/issues/56
    def test_toReproduceAndFixIssue56(self):
        Paths = jpy.get_type('java.nio.file.Paths')
        p = Paths.get('testfile', [])
        s = str(p)
        self.assertEqual(s, 'testfile')
        # The following call crashed the Python interpreter with JDK/JRE 1.8.0 < update 60.
        s = p.toString()
        self.assertEqual(s, 'testfile')

    # see https://github.com/bcdev/jpy/issues/57
    def test_toReproduceAndFixIssue57(self):
        HashMap = jpy.get_type('java.util.HashMap')
        Map = jpy.get_type('java.util.Map')
        m = HashMap()
        c = m.getClass()
        self.assertEqual(c.getName(), 'java.util.HashMap')
        m = jpy.cast(m, Map)
        # without the fix, we get "AttributeError: 'java.util.Map' object has no attribute 'getClass'"
        c = m.getClass()
        self.assertEqual(c.getName(), 'java.util.HashMap')

    # see https://github.com/bcdev/jpy/issues/54
    def test_toReproduceAndFixIssue54(self):
        String = jpy.get_type('java.lang.String')
        Arrays = jpy.get_type('java.util.Arrays')
        a = jpy.array(String, ['A', 'B', 'C'])
        # jpy.diag.flags = jpy.diag.F_METH
        s = Arrays.toString(a)
        # jpy.diag.flags = 0
        # without the fix, we get str(s) = "java.lang.String@xxxxxx"
        self.assertEqual(str(s), '[A, B, C]')


class TestDefaultMethods(unittest.TestCase):

    def setUp(self):
        self.Fixture = jpy.get_type('org.jpy.fixtures.DefaultInterfaceImplTestFixture')
        self.assertIsNotNone(self.Fixture)

    # see https://github.com/bcdev/jpy/issues/102
    def test_defaultedInterfaces(self):
	fixture = self.Fixture()
        self.assertEqual(fixture.doItPlusOne(), 3)


if __name__ == '__main__':
    print('\nRunning ' + __file__)
    unittest.main()
