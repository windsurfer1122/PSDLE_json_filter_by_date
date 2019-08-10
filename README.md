# PSDLE_json_filter_by_date.py (c) 2019 by "windsurfer1122"
Filter [PSDLE][1] JSON exports on purchase date or release date.

* Cross platform support
  * Decision: Python 3
    * Compatible with Python 2 (target version 2.7)
      * Identical output
      * Forward-compatible solutions preferred

## Execution
For available options execute: `PSDLE_json_filter_by_date.py -h`<br>

### Installing on Debian
1. Python 3, which is the recommended version, and most modules can be installed via apt.<br>
Install Python 3 via the following apt packages: `python3 python3-pip`.<br>

1. Python 2 is the default on Debian, but comes with an outdated pip version until Debian 8.<br>
__Starting with Debian 9 "Stretch"__ install Python 2 modules via the following apt packages: `python-pip python-future`.<br>
For __Debian up to 8 "Jessie"__ use the pip version from the original [PyPi](https://pypi.org/project/pip/) source:<br>
   ```
   apt-get purge python-pip python-dev python-future
   apt-get autoremove
   wget https://bootstrap.pypa.io/get-pip.py
   python2 get-pip.py
   pip2 install --upgrade future
   ```

### Installing on Windows
1. Install Python<br>
   Checked with Python 3.7 x64 on Windows 10 x64 Version 1803.
   * Get it from the [Python homepage](https://www.python.org/)
   * Install launcher for all users
   * Add Python to PATH<br>
     Adds %ProgramFiles%\Python37 + \Scripts to PATH
   * __Use Customize Installation (!!! necessary for advanced options !!!)__
   * Advanced Options
     * Install for all users

1. Install necessary Python modules via pip.
   * Start an __elevated(!!!)__ Command Prompt (Run As Admin via Right Click)
   * Update PIP itself first: `python -m pip install --upgrade pip`
   * Exit Command Prompt: `exit`

Executing python scripts can be done via Windows Explorer or a Command Prompt. Normally no elevation is necessary for script execution, except when the python script wants to change something in the system internals.

## Original Source
git master repository at https://github.com/windsurfer1122

## License
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

[1]: https://github.com/RePod/psdle
