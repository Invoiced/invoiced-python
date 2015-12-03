from invoiced.errors import ApiError
import unittest


class TestError(unittest.TestCase):

    def test_error(self):
        error = ApiError("ERROR!", 500)
        self.assertEqual("(500): ERROR!", str(error))

if __name__ == '__main__':
    unittest.main()
