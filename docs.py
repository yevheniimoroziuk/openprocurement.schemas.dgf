#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
from re import compile


SCHEMA_PATH = compile(r'dgf/schemas/(?P<path>[a-zA-Z0-9_/]+)$')
VERSION_RE = compile(r'schema_(?P<version>\d+).json')
DIR_PATH = os.path.dirname(os.path.realpath(__file__))

"""

Create tree for json schema in docs

"""

main_schema_template = u"""
.. index:: Schemas

.. _Schemas:

=======
Schemas
=======

All schemas:

.. toctree::
   :maxdepth: 20

   {doctree}

"""

schemas_rst_template = u"""

======================
Schema {schema_number}
======================

Main page :ref:`schemas`


{schemas}


"""

schema_template = u"""

version {version}
-----------

.. jsonschema:: ../../../{static_path}openprocurement/schemas/dgf/schemas/{schema_path}/{file}


`Schema {schema_number}`_

.. _`Schema {schema_number}`: /{schema_path}/{file}
"""


def create_doc_file(path, file_name, rst):
    with io.open(os.path.join(path, file_name), 'w') as f:
        f.write(schemas_rst_template.format(schema_number=file_name[:-4],
                                            schemas=''.join(rst)))


def create_dir(path):
    """ Create directory by path if it not exists """
    if not os.path.exists(path):
        os.makedirs(path)


def create_doctree(path):
    doctree = []
    for path, dirs, files in os.walk(path):
        if not SCHEMA_PATH.search(path):
            continue
        path = SCHEMA_PATH.search(path).groupdict()['path']
        doctree.append("schemas/{}/{}".format(path, path.replace('/', '')))
    return "\n   ".join(doctree)


def create_schemas_docs():
    for index, (path, dirs, files) in enumerate(os.walk('./openprocurement/schemas/dgf/schemas')):
        if not SCHEMA_PATH.search(path):
            continue
        path = SCHEMA_PATH.search(path).groupdict()['path']
        print("Find schemas in {path}".format(path=path))
        schema_number = path.replace('/', '')
        rst = [schema_template.format(
                file=file,
                dir_path=DIR_PATH,
                schema_number=schema_number,
                schema_path=path,
                static_path="../" * index,
                version=VERSION_RE.search(file).groupdict()['version'])
               for file in files]
        path_for_docs = os.path.join(os.getcwd(), 'docs', 'source', 'schemas', path)
        create_dir(path_for_docs)
        create_doc_file(path_for_docs,
                        "{schema_number}.rst".format(schema_number=schema_number),
                        rst)

    with io.open('./docs/source/schemas.rst', 'w') as f:
        f.write(main_schema_template.format(
            doctree=create_doctree('./openprocurement/schemas/dgf/schemas')))

if __name__ == '__main__':
    print("Create schemas rst files.")
    create_schemas_docs()
    print("End create schemas rst files.")
