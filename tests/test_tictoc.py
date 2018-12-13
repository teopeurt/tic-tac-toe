import unittest
import os
import json
from app import create_app


class TicTocTestCase(unittest.TestCase):
    """This class represents the tictoc test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
