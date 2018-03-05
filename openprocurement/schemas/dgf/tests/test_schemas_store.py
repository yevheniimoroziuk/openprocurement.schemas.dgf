#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_schemas_store
----------------------------------

Tests for `schemas_store` module.
"""


import unittest
from itertools import combinations

from jsonschema.exceptions import  ValidationError

from openprocurement.schemas.dgf.schemas_store import SchemaStore

class TestSchemas_store(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_validation(self):
        store = SchemaStore()
        store.load()
        schema_tuple = store.get_schema(u'04000000-8', u'latest')

        exc = None

        test_properties = {}
        try:
            exc = None
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(e.message, '{} is a required property'.format("u'totalArea'"))

        test_properties = {u'totalArea': 200}

        # Test constructionTechnology
        available_value = [u"monolithicFrame", u"panel", u"insulatedPanel", u"brick", u"other"]
        for i in range(len(available_value)):
            for ct in combinations(available_value, i):
                test_properties[u'constructionTechnology'] = list(ct)
                schema_tuple.schema.validate(test_properties)


        try:
            test_properties[u'constructionTechnology'] = [u"wrong_value"]
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'constructionTechnology')
        self.assertEqual(e.message, 'u\'{}\' is not one of {}'.format(u"wrong_value", available_value))

        try:
            exc = None
            test_properties[u'constructionTechnology'] = [u"panel", u"panel"]
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'constructionTechnology')
        self.assertEqual(e.message, '{} has non-unique elements'.format(test_properties[u'constructionTechnology']))

        test_properties[u'totalArea'] = -200
        test_properties[u'constructionTechnology'] = []

        # Test if totalArea less than 0
        try:
            exc = None
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'totalArea')
        self.assertEqual(e.message, '{} is less than the minimum of 0'.format(test_properties[u'totalArea']))

        test_properties[u'totalArea'] = 0
        test_properties[u'livingArea'] = 0
        test_properties[u'kitchenArea'] = 0
        test_properties[u'landArea'] = 0
        schema_tuple.schema.validate(test_properties)

        # Test if livingArea less than 0
        test_properties[u'livingArea'] = -200
        try:
            exc = None
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'livingArea')
        self.assertEqual(e.message, '{} is less than the minimum of 0'.format(test_properties[u'livingArea']))

        # Test if kitchenArea less than 0
        test_properties[u'livingArea'] = 0
        test_properties[u'kitchenArea'] = -200
        try:
            exc = None
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'kitchenArea')
        self.assertEqual(e.message, '{} is less than the minimum of 0'.format(test_properties[u'kitchenArea']))

        # Test if landArea less than 0
        test_properties[u'kitchenArea'] = 0
        test_properties[u'landArea'] = -200
        try:
            exc = None
            schema_tuple.schema.validate(test_properties)
        except ValidationError as e:
            exc = e
        self.assertNotEqual(exc, None)
        self.assertEqual(exc.relative_path[0], u'landArea')
        self.assertEqual(e.message, '{} is less than the minimum of 0'.format(test_properties[u'landArea']))

        # Test if landArea less than 0
        test_properties[u'landArea'] = 0
        test_properties[u'floor'] = -200
        schema_tuple.schema.validate(test_properties)

        test_properties[u'floor'] = 200
        schema_tuple.schema.validate(test_properties)
