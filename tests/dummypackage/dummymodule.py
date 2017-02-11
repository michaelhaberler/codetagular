# TODO fill module

"""
docstring for dummymodule

.. todo::
    Add some code

this module does nothing
"""

import sys

print(sys.path)


def _foo(arg):
    """
    docstr for _foo

    .. todo::
        private function, won't be documented by sphinx
    """
    # XXX true? _foo does nothing?
    return arg


class Foo(object):
    # TODO also Foo is not doing a lot

    def calc_value(self, x):
        return x + 1 # TODO this could be improved



