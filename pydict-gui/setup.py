# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python
# command line to build: python setup.py build


from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

executables = [
    Executable('pydict-gui.py', base='Win32GUI')
]

setup(name='在线翻译',
      version='Version 1.0.0',
      description='在线翻译,支持保存本地保存',
      executables=executables
      )
