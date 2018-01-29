# Copyright 2014-2017 Adam Karpierz
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

__all__ = ('__title__', '__summary__', '__uri__', '__version_info__',
           '__version__', '__author__', '__email__', '__copyright__',
           '__license__')

__title__        = "jtypes.jpy"
__summary__      = "Bi-directional Python-Java bridge (ctypes/cffi-based Jpy)"
__uri__          = "http://pypi.python.org/pypi/jtypes.jpy/"
__version_info__ = type("version_info", (), dict(serial=1,
                        major=0, minor=9, micro=0, releaselevel="beta"))
__version__      = "{0.major}.{0.minor}.{0.micro}{1}{2}".format(__version_info__,
                   dict(final="", alpha="a", beta="b", rc="rc")[__version_info__.releaselevel],
                   "" if __version_info__.releaselevel == "final" else __version_info__.serial)
__author__       = "Adam Karpierz"
__email__        = "python@python.pl"
__copyright__    = "Copyright 2014-2017 {0}".format(__author__)
__license__      = "Apache License, Version 2.0 ; {0}".format(
                   "http://www.apache.org/licenses/LICENSE-2.0")
