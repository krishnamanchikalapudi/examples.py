import time, unittest
import src.PredictApi as api

class PredictApiTests(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()
        self.app = api.test_client()
    
    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_hello(self):  # ref: https://docs.python.org/3/library/unittest.html
        self.assertTrue(True)

    def test_index(self): 
        resp = self.app.get('/')
        print("Index Response:: ", resp)
        self.assertTrue(True)


if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(PredictApiTests)
    unittest.TextTestRunner(verbosity=0).run(suite)