# -*- coding: utf-8 -*-

import unittest
from openprocurement.schemas.dgf.schemas_store import SchemaStore
from jsonschema.exceptions import ValidationError


class TestSchema(unittest.TestCase):

    def setUp(self):
        classification_id = u"34621100-7"
        version = '001'

        store = SchemaStore()
        store.load()
        schema_tuple = store.get_schema(classification_id, version)
        self.schema_tuple = schema_tuple
        self.schema = schema_tuple.schema

    def test_properties_blank(self):
        properties = {}

        assert_error = self.assertRaises(ValidationError)
        with assert_error:
            self.schema.validate(properties)

    def test_properties_minimal_data(self):
        properties = {'rollingStock': 'test rollingStock'}

        self.schema.validate(properties)

    def test_properties_full_data(self):
        properties = {'rollingStock': 'test rollingStock',
                      'loadingRestriction': 'test loadingRestriction'}

        self.schema.validate(properties)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite())
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
