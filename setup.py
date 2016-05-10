
from setuptools import setup
import sys
import os
home=os.path.expanduser('~')

setup(
    name = 'data_gui',
    version = '0.0.1',
    description = 'Dataset viewer for pandas, especially large ROOT files',
    # url='',
    # license='GPL v3',
    author = 'Konstantin Schubert',
    author_email = 'konstantin@schubert.fr',
    packages = ['data_gui'],
    install_requires=['root_pandas',
                      'matplotlib',
                      'pandas',
                      # 'pyqt4', # this seems to be unsupported by pip
                      'future'],
    entry_points = { 'gui_scripts': [
                     'datagui = data_gui.__main__:main']},
    classifiers = ['Operating System :: OS Independent',
    		'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 3',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'Topic :: Software Development :: User Interfaces',
            # 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Intended Audience :: Science/Research'],
    keywords = ['ROOT', 'root_pandas', 'table', 'pandas', 'data analysis'],
)