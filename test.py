# Import modules
try:
    from run import app
    import unittest
except Exception as e:
    print('There are some missing modules {}!'.format(e))


# Test class
class FlaskTest(unittest.TestCase):

    # 200 response on the user route
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/active/Basillica')
        statusCode = response.status_code
        self.assertEqual(statusCode, 200)

    # Testing if response is a json object
    def test_index_content(self):
        tester = app.test_client(self)
        response = tester.get('/active/Basillica')
        self.assertEqual(response.content_type,'application/json')



if __name__ == '__main__':
    unittest.main()