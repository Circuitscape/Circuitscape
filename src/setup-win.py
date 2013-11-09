"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2exe
"""

import os
import py2exe
from distutils.core import setup
from csversion import CIRCUITSCAPE_VER, CIRCUITSCAPE_AUTHOR, CIRCUITSCAPE_EMAIL

#INCLUDES = []
INCLUDES =[]
PACKAGES = ['PythonCard', 'wx', 'wxversion', 'numpy', 'scipy', 'pyamg', "scipy.io.matlab.streams"]

DATA_FILES = ['cs_gui.rsrc.py', 'verify.py', 'cs_logo.jpg', 'cs_logo.ico',
              'verify', 'verify/1', 'verify/2', 'verify/3', 'verify/4', 'verify/5', 'verify/6', 'verify/7', 'verify/8']
OPTIONS = {'includes': PACKAGES}

#Now also compile cs_run.py.  compiling it first ensures that dependencies needed for cs_gui also included.
setup(
    console=['cs_run.py'],
    data_files=DATA_FILES,
    options={'py2exe': OPTIONS},
    version=CIRCUITSCAPE_VER,
    author=CIRCUITSCAPE_AUTHOR,
    author_email=CIRCUITSCAPE_EMAIL
)
setup(
    console=['cs_gui.py'],
    data_files=DATA_FILES,
    options={'py2exe': OPTIONS},
    version=CIRCUITSCAPE_VER,
    author=CIRCUITSCAPE_AUTHOR,
    author_email=CIRCUITSCAPE_EMAIL
)


