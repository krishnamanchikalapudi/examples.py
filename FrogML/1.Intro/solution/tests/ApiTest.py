import time, unittest

class ApiTests(unittest.TestCase):
    def setUp(self):
        self.startTime = time.time()
    
    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_hello(self):  # ref: https://docs.python.org/3/library/unittest.html
        self.assertTrue(True)

if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(ApiTests)
    unittest.TextTestRunner(verbosity=0).run(suite)