# -*- coding: utf-8 -*-

# See http://peak.telecommunity.com/DevCenter/setuptools#namespace-packages
try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

__author__ = """Serbokryl Oleg"""
__email__ = 'oleh.serbokryl@unity-bars.com'
__version__ = '0.1.0'
