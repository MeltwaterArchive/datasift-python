import unittest, sys, os, json
from datetime import datetime
sys.path[0:0] = [os.path.join(os.path.dirname(__file__), ".."),]
import testdata, config, datasift

class TestLiveAPI(unittest.TestCase):

    user = None

    def setUp(self):
        self.user = datasift.User(config.username, config.api_key)

    def test_compile_success(self):
        definition = self.user.create_definition(testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.fail('CompileFailedError: %s' % e)
        except datasift.APIError as (e, c):
            self.fail('APIError: [%s] %s' % (c, e))

        self.assertEqual(definition.get_hash(), testdata.definition_hash, 'Incorrect hash')

    def test_compile_failure(self):
        definition = self.user.create_definition(testdata.invalid_definition)
        self.assertEqual(definition.get(), testdata.invalid_definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
            self.fail('Expected CompileFailedError not thrown')
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            # Expected exception
            pass
        except datasift.APIError as (e, c):
            self.fail('APIError: [%s] %s' % (c, e))

    def test_compile_success_then_failure(self):
        definition = self.user.create_definition(testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            self.fail('CompileFailedError: %s' % e)
        except datasift.APIError as (e, c):
            self.fail('APIError: [%s] %s' % (c, e))

        self.assertEqual(definition.get_hash(), testdata.definition_hash, 'Incorrect hash')

        definition.set(testdata.invalid_definition)
        self.assertEqual(definition.get(), testdata.invalid_definition, 'Definition CSDL not set correctly')

        try:
            definition.compile()
            self.fail('Expected CompileFailedError not thrown')
        except datasift.InvalidDataError as e:
            self.fail('InvalidDataError: %s' % e)
        except datasift.CompileFailedError as e:
            # Expected exception
            pass
        except datasift.APIError as (e, c):
            self.fail('APIError: [%s] %s' % (c, e))

    def test_get_created_at(self):
        definition = self.user.create_definition(testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')
        self.assertTrue(definition.get_created_at() > datetime.strptime('2000-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'), 'The created at date is earlier than Jan 1st, 2000')

    def test_get_total_dpu(self):
        definition = self.user.create_definition(testdata.definition)
        self.assertEqual(definition.get(), testdata.definition, 'Definition CSDL not set correctly')
        self.assertTrue(definition.get_total_dpu() > 0, 'THe total DPU is not positive')

if __name__ == '__main__':
    unittest.main()

















































