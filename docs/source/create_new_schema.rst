.. index:: Create_new_schema

.. _Create_new_schema:

Create new schema
=================


For creating new schema first create template on `SchemaOnline
<http://jsonschema.net/>`_.


Create schema.
~~~~~~~~~~~~~~

Pattern for new schema 06******-\*, it's means that all items with CAV
classification which start with 06 and have't more specific schema will use it.

Fields for new schema:

 - Region = Kyiv
 - City = Kyiv
 - Availability_owners = True/False


So, open service and write your fields, and then get template.

.. image:: static/tutorial/example_schema_data.png

Example setup for service.

.. image:: static/tutorial/jsonschema_settings.png


Generate schema template and save it in file,
with name `schema_XXX.json` where XXX - is number of version.

.. code:: json

    {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "definitions": {},
        "id": "http://example.com/example.json",
        "properties": {
            "Availability_owners": {
                "id": "/properties/Availability_owners",
                "type": "boolean"
            },
            "City": {
                "id": "/properties/City",
                "type": "string"
            },
            "Region": {
                "id": "/properties/Region",
                "type": "string"
            }
        },
        "type": "object"
    }


Edit schema template
####################

Edit template which we create before.
Open file with schema and edit fields `title`, and `description`.

Validation
~~~~~~~~~~

For every field we can add basic validation, like `maxlength` -  max length for text field or `minlength`.
For more validation you can read `this <http://json-schema.org/latest/json-schema-validation.html#rfc.section.5/>`_.

Change ID for schema
~~~~~~~~~~~~~~~~~~~~

For editing main ID in schema get real number from schema pattern and then insert after every number '/', exception is only first two symbols.

**001** - Number schema version, set real number.

Examples:

========== ========================================
 Pattern                Schema ID
---------- ----------------------------------------
06******-*   file:///schemas/06/schema_001.json
061*****-*   file:///schemas/06/1/schema_001.json
0613****-*   file:///schemas/06/1/2/schema_001.json
========== ========================================
