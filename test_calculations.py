"""
Test Code
"""

import unittest

class TestMethods(unittest.TestCase):
    """
    Test class
    """
    def test_two_plus_three(self):
        """
        Test 2+3
        """
        self.assertEqual(2+3, 5)


        

if __name__ == '__main__':
    unittest.main()
