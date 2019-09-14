#!/usr/bin/env python3
# coding: utf-8
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#


import os
import sys
import platform
import shutil

# finding os platform
os_type = platform.system()

if os_type == 'Linux' or os_type == 'FreeBSD' or os_type == 'OpenBSD':
    from setuptools import setup
    setuptools_available = True
    print(os_type + " detected!")
else:
    print('This script is only work for GNU/Linux or BSD!')
    sys.exit(1)

# Checking dependencies!
not_installed = ''

# PySide2
try:
    import PySide2
    print('PySide2 is found')
except:
    print('Error : PySide2 is not installed!')
    not_installed = not_installed + 'PySide2, '

# youtube_dl
try:
    import youtube_dl
    print('youtube-dl is found')
except:
    print('Warning: youtube-dl is not installed!')
    not_installed = not_installed + 'youtube-dl, '

# show warning , if dependencies not installed!
if not_installed != '':
    print('########################')
    print('####### WARNING ########')
    print('########################')
    print('Some dependencies are not installed .It causes some problems for persepolis! : \n')
    print(not_installed + '\n\n')
    answer = input('Do you want to continue?(y/n)')
    if answer not in ['y', 'Y', 'yes']:
        sys.exit(1)

if sys.argv[1] == "test":
    print('We have not unit test :)')
    sys.exit('0')

DESCRIPTION = 'Converter from SRT to TXT format'

# finding current directory
cwd = os.path.abspath(__file__)
setup_dir = os.path.dirname(cwd)

# clearing __pycache__
src_pycache = os.path.join(setup_dir, 'srttotxt', '__pycache__')
gui_pycache = os.path.join(setup_dir, 'srttotxt', 'gui', '__pycache__')
scripts_pycache = os.path.join(setup_dir, 'srttotxt', 'scripts', '__pycache__')

for folder in [src_pycache, gui_pycache, scripts_pycache]:
    if os.path.isdir(folder):
        shutil.rmtree(folder)
        print(f'{str(folder)} is removed!')

setup(
    name='SRTtoTTX',
    version='0.2.1',
    license='GPL3',
    description=DESCRIPTION,
    long_description=DESCRIPTION,
    include_package_data=True,
    url='https://github.com/DoctorChe/srttotxt',
    author='Doctor_Che',
    author_email='duncan.reg@yandex.ru',
    maintainer='Doctor_Che',
    maintainer_email='duncan.reg@yandex.ru',
    packages=(
        'srttotxt',
        'srttotxt.gui',
        'srttotxt.scripts',
    ),
    entry_points={
        'console_scripts': [
            'srttotxt = srttotxt.__main__'
        ]
    }
)
