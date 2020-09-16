# Python code to demonstrate working of unittest
import unittest
from empires import get_empire_info


class TestEmpireAPI(unittest.TestCase):

    def test_empty_query(self):
        response = get_empire_info('')
        self.assertEqual(response, {'message': '400 Bad Request'})

    def test_invalid_query(self):
        response = get_empire_info('testing random query')
        self.assertFalse(response, False)

    def test_valid_name(self):
        data = get_empire_info('Arbalest')
        empire_name = data.get('name')
        self.assertEqual(empire_name, 'Arbalest')

    def test_valid_str_id(self):
        data = get_empire_info('3')
        empire_id = data.get('id')
        self.assertEqual(str(empire_id), '3')

    def test_valid_int_id(self):
        data = get_empire_info(5)
        empire_id = data.get('id')
        self.assertEqual(empire_id, 5)

    def test_invalid_id(self):
        resp = get_empire_info(100000)
        self.assertEqual(resp, False)

    def test_special_chars(self):
        for char in "?.=/\\'<>:":
            res = get_empire_info(char)
            self.assertEqual(res, 0)  # False is 0


if __name__ == '__main__':
    unittest.main()
