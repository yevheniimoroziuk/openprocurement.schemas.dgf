# -*- coding: utf-8 -*-
import os
import io
import json
from re import compile
from collections import namedtuple
from jsonschema import Draft4Validator
from jsonschema.exceptions import ValidationError

from ._tree import Tree
from .exceptions import NotFoundSchema

VERSION_RE = compile(r'schema_(?P<version>\d+).json')
INDEX_RE = compile(r'/(?P<index>\d+)$')


def get_default_schema():
    return os.path.join(os.path.dirname(__file__), 'schemas')


class SchemaStore(object):
    """  Object that work with schemas """

    schema_tuple = namedtuple('schema', ['code', 'version', 'schema'])
    root = None
    error_massage_cannot_find = "Can't find schema by version {version}"

    import_exception = (NotFoundSchema, )
    validation_exception = (ValidationError, )

    def __init__(self, path=None):
        """ Init path and update schema(IO operation) """
        self.path = path if path else get_default_schema()
        self.update_schemas_id(self.path)

    def load(self):
        """ Create root """
        self.root = Tree()
        self.build_tree(self.root, self.path)
        return self

    def _check_version_in_branch(self, version, branch):
        """ Check that version in branch if it not then raise exception """
        if version in branch.versions:  # Try find version
            return self.schema_tuple(
                code=branch.index,
                version=version,
                schema=branch.versions[version])
        else:
            raise NotFoundSchema(
                self.error_massage_cannot_find.format(version=version)
            )

    def get_schema(self, code, version='latest'):
        """
        Get schema by code,
        :param code: str
        :param version: str example "001"
        :return: namedtuple with code, version, schema
        """
        result = self._find_child(code=code, version=version, branch=self.root)
        if not result:
            raise NotFoundSchema(
                self.error_massage_cannot_find.format(version=version)
            )
        return result

    def _find_child(self, branch, code, version):
        """
        Try find child by code and version
        :param branch: Tree
        :param code: CAV code
        :param version: string
        :return:
        """
        if branch.index:
            check_code = code[len(branch.index):]
        else:
            check_code = code
        for child in branch.children:
            if check_code.startswith(child.index):
                result = self._get_schema(
                    code=code[len(branch.index):] if branch.index else code,
                    version=version,
                    branch=child)
                if not result:
                    if version != 'latest':
                        raise NotFoundSchema(
                            self.error_massage_cannot_find.format(
                                version=version)
                        )
                    else:
                        return self._check_version_in_branch(version, branch)
                else:
                    return result
        return None

    def _get_schema(self, code, branch, version='latest',):
        """
        Need normal doc string
        :param code: CAV code
        :param version: string length which is 3
        :param branch: Tree
        :return:
        """
        if len(code) == len(branch.index):  # If it last step
            if version == 'latest':
                if branch.versions:
                    version_keys = list(branch.versions.keys())
                    version_keys.sort()
                    return self.schema_tuple(
                        code=branch.index,
                        version=version_keys[-1],
                        schema=branch.versions[version_keys[-1]])
                else:
                    return None  # Get up latest version
            else:
                return self._check_version_in_branch(version, branch)
        else:
            result = self._find_child(branch=branch,
                                      code=code,
                                      version=version)
            if result:
                if branch.index:
                    return self.schema_tuple(
                        code=branch.index + result[0],
                        version=result.version,
                        schema=result.schema)
                else:
                    return result
            if version != 'latest':
                raise NotFoundSchema(
                    self.error_massage_cannot_find.format(version=version)
                )
            else:
                version_keys = list(branch.versions.keys())
                return self.schema_tuple(
                    code=branch.index,
                    version=version_keys[-1],
                    schema=branch.versions[version_keys[-1]])

    def build_tree(self, tree, path):
        """
        Build tree from schemas
        :param tree: _tree.Tree
        :param path: os.path
        """
        for elem_name in os.listdir(path):
            if elem_name.endswith('.json'):
                with io.open(os.path.join(path, elem_name),
                             encoding='utf-8') as f:
                    schema_json = json.load(f)
                    reg_group = VERSION_RE.search(elem_name).groupdict()
                    tree.versions[reg_group['version']] = Draft4Validator(
                        schema_json
                    )
            else:
                if os.path.isdir(os.path.join(path, elem_name)):
                    child = Tree(index=elem_name)
                    tree.children.append(child)
                    self.build_tree(child, os.path.join(path, elem_name))

    def _go_by_schema(self, path, handler_file, handler_path):
        """
        Go by directory and call handler_file and find json and
        call handler path when find another directory
        :param path: os.path
        :param handler_file: function which call when find file
        :param handler_path: function which call when find directory
        :return: None
        """
        for elem_name in os.listdir(path):
            if elem_name.endswith('.json'):
                handler_file(os.path.join(path, elem_name))
            else:
                new_path = os.path.join(path, elem_name)
                if os.path.isdir(new_path):
                    handler_path(new_path,
                                 self.update_file,
                                 self._go_by_schema)

    def update_schemas_id(self, path):
        """
        Update every schemas id
        :param path: os.path
        """
        self._go_by_schema(path, self.update_file, self._go_by_schema)

    def update_file(self, file_path):
        """
        Update schema id
        :param file_path: os.path
        """
        file_path_template = "file://{package}{schema}"
        with io.open(file_path, mode='r+', encoding='utf-8') as f:
            schema_json = json.load(f)
            schema_json['id'] = file_path_template.format(
                package=self.path,
                schema=schema_json['id'].split('schemas')[-1])
            f.seek(0)
            f.truncate()
            f.write(json.dumps(schema_json, indent=4,
                               separators=(',', ': '), ensure_ascii=False))
