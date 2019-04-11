# -*- coding: utf-8 -*-
#
# Copyright (c) 2018 Lars Bergmann
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
setup(
    name='pf_nxt',
    version='0.1',
    description='PerFact Lego NXT library',
    long_description='''\
        Toolksuite to run Lego NXT via bleutooth using Python
        Robot can either be run directly using a gamepad as well as remote
        controlled using a simple HTTP server''',
    author='Lars Bergmann',
    author_email='lb@perfact.de',
    packages=[
        'pf_nxt',
    ],
    license='GPLv3',
    scripts=['bin/nxt_direct', 'bin/nxt_start_server', 'bin/nxt_start_client'],
    platforms=['Linux', ],
)
