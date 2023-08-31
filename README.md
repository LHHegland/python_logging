# Python Logging Example

**NAMESPACE:** me.hegland-lance.examples.python.logging

**PURPOSE:** Example of Python logging with formats and file handlers across various modules and packages.

.

## Table of Contents

- [Features](#features)
- [Background](#background)
- [Known Issues](#known-issues)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Contributors](#contributors)
- [Roadmap](#roadmap)
- [License](#license)

.

## **Features**

Example of Python logging includes
- single reusable and easily importable module for logging
- quick and easy to scan logging output
   - examples of color-coding for ease of log scanning
   - different message formatting based on messaging level: FYI (e.g. debug, info) vs alert (e.g. warning, error, critical, exception)
- vital information for experimenting and debugging
   - system environmental variables logged when execution initiated
   - logger names indicate modules submitting messages
   - alert messages include stack trace
   - log file naming includes module and timestamp
- flexible
   - options to output to file or stderr
- examples to build from
   - sample log messages
   - message filter function
   - argparse for command line interface help messaging

.

## **Background**

Lance created to help him learn how to incorporate Python logging across multiple modules plus quickly find vital information for experimenting and debugging.

.

## **Known Issues**

None

.

## **Requirements**

1. Familiarity and access to Python development tools, such as recent versions of the following:
   | Tool                         | Download | Reference | with VSCode |
   |------------------------------|----------|-----------|-------------|
   | Python | [Link](https://www.python.org/downloads/) | [Link](https://wiki.python.org/moin/BeginnersGuide) | [Link](https://code.visualstudio.com/docs/languages/python) |
   | Git | [Link](https://git-scm.com/downloads) | [Link](https://git-scm.com/videos) | [Link](https://vscode.github.com/) |
   | GitHub  | | [Link](https://github.com) | [Link](https://code.visualstudio.com/docs/sourcecontrol/github) |

.

## **Installation**

1. Review [README](#table-of-contents).
1. Satisfy [minimum requirements](#requirements).
1. Get the repository.
   1. Create a local working directory (e.g. `D:\abc\...\xyz\python-logging\`)
   1. From your local working directory `python-logging`, clone remote GitHub repository `LHHegland/python_logging.git` (`git clone git@github.com:LHHegland/python_logging.git`)

.

## **Configuration**

None

.

## **Usage**

1. Review [README.md](#table-of-contents).
1. Complete [installation](#installation).
1. Review code in modules, especially utils\logz.py, test.py, and a few pkg_*\mdl_*.py.
1. Experiment with utils\logs.py 
   1. Execute `py test.py`
   1. Review `logs\test-[timestamp].log`
1. Experiment with utils\logs.py
   1. Execute `py utils\logs.py --help`
   1. Review on-screen results

.

## **Contributors**

TODO: Identify contributors.

- **Lance Hegland ([lance.hegland@civic-innovations.com](mailto:lance.hegland@civic-innovations.com))**

.

## **Roadmap**

None

.

## **License**

GNU General Public License v3.0 (GNU GPLv3)

- See [LICENSE.txt](LICENSE.txt)
- See [GNU General Public License v3.0 (GNU GPLv3)](https://choosealicense.com/licenses/gpl-3.0/)