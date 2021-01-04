import unittest
from utils import my_functions as mf
import warnings

class MyFuntionQuandoo(unittest.TestCase):
    
    def test_valid_mail(self):    # For categorize the difficulty
        
        # using a value, expect a correct mail validation
        self.assertEqual( mf.get_mail ( 'franko.ortiz.gutierrez@gmail.com' ) , 'franko.ortiz.gutierrez@gmail.com')        
              
    def test_invalid_mail(self):    # For get a correct minute from cook and prep times
        
        # using a value, expect a correct mail validation
        self.assertEqual( mf.get_mail ( 'someguy@gmail' ) , '')        
               
if __name__ =='__main__':
    
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
