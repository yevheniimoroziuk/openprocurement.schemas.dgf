.. index:: Create_new_schema

.. _Create_new_schema:

Create new schema for 06*****
=============================


Schema fields table.

.. image:: static/tutorial/fields_table.png


For schema with pattern 06***** we need fields:
 - region
 - district
 - cadastral_number
 - area
 - forms_of_land_ownership
 - co_owners
 - availability_of_utilities


Create template using `SchemaOnline <http://jsonschema.net/>`_.
Paste fields, and generate template for schema.

.. image:: static/tutorial/06_fields.png

`Schema 06`_

.. _`Schema 06`: ../../../openprocurement/schemas/dgf/schemas/06/schema_001.json

Edit template
~~~~~~~~~~~~~

Template which we got on previous step

.. include:: static/tutorial/06_template.json
  :code:

Now we can add validation, description, and default value for every field.

We got such a scheme.

.. include:: static/tutorial/06_fields_with_validation.json
   :code:


Add ID
~~~~~~

Pattern for schema is 06******, so ID must look like **urn:cav:06\*\*\*\*\*\*-\*.\*\*\***


Create schema for 061****
=========================

Schema fields table.

.. image:: static/tutorial/fields_table.png

We can see that 061***** template has 1 additional field.


Copy previous schema, edit fields, add one more, and edit ID.

Updated schema:

.. include:: static/tutorial/061_fields_with_validation.json
   :code:

`Schema 061`_

.. _`Schema 061`: ../../../openprocurement/schemas/dgf/schemas/06/1/schema_001.json
