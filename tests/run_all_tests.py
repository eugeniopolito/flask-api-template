"""
Run all tests (integration and system tests).

Note: all tests use an in-memory SQLite DB server so they can be easily reproduced and no data will be saved on real DB.
"""

import unittest

loader = unittest.TestLoader()
start_dir = '.'
suite = loader.discover(start_dir)

runner = unittest.TextTestRunner()
runner.run(suite)
