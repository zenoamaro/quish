Quish
=====

Executes a script from a user's gists.

_Warning: Executing random code from internet may be dangerous. Script responsibly._

  1. [Quick start](#quick-start)
  2. [Usage guide](#usage-guide)
  3. [API reference](#api-reference)
  4. [Building and testing](#building-and-testing)
  5. [Roadmap](#roadmap)
  6. [Changelog](#changelog)
  7. [License](#license)


Quick start
-----------
Suppose you have a Gist like this one:

	A few of my util scripts.

	my-script.sh
		#!/usr/bin/env bash
		echo "This is a useful script."

	my-other-script.sh
		#!/usr/bin/env python3
		print("This is not a useful script.")

Then, you can do this:

    # Get a copy of quish
    $ wget https://raw.githubusercontent.com/zenoamaro/quish/master/qsh.py

	$ ./qsh YourGitUsername/my-script
	This is a useful script.

	$ ./qsh YourGitUsername/my-other-script
	This is not a useful script.


Usage guide
-----------
TBD


API reference
-------------
TBD


Building and testing
--------------------
Quish is made of a single file, and has no external dependencies or build steps, so that it can be fetched and used with a single `wget`.

That said, you can clone the project to work on it or run tests:

    git clone https://github.com/zenoamaro/quish && cd quish
    python3 -m doctest qsh.py


Roadmap
-------
  - Installation and testing using `setup.py`
  - Compatibility with Python 2.7
  - Caching of gists lists and scripts
  - Local username for shorter invocation
  - GitHub API Authentication


Changelog
---------
#### v0.1.0
- Initial version

[Full changelog](CHANGELOG.md)


License
-------
The MIT License (MIT)

Copyright (c) 2015, zenoamaro <zenoamaro@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.