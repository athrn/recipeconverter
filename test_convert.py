# -*- coding: utf-8 -*-
import unittest as ut

from convert import *

class Tests(ut.TestCase):
    def test1_unicode_fractions(self):        
        self.assertEqual(u'1/2', replace_unicode_fractions(u'½'))
        self.assertEqual(u'3/4', replace_unicode_fractions(u'¾'))
        self.assertEqual(u'5 3/4', replace_unicode_fractions(u'5¾'))
        self.assertEqual(u'5 3/4', replace_unicode_fractions(u'5 ¾'))
        self.assertEqual(u'ape 5 3/4 bat', replace_unicode_fractions(u'ape 5¾ bat'))
        self.assertEqual(u'ape 5 3/4 bat', replace_unicode_fractions(u'ape 5 ¾ bat'))
        
    def test2_text_fractions(self):
        self.assertEqual(u'0.75', replace_text_fractions(u'3/4'))
        self.assertEqual(u'3.75', replace_text_fractions(u'3 3/4'))
        self.assertEqual(u'ape 0.75 bat', replace_text_fractions(u'ape 3/4 bat'))
        self.assertEqual(u'ape 3.75 bat', replace_text_fractions(u'ape 3 3/4 bat'))

    def test3_replace_fractions(self):
        self.assertEqual(u'ape 3.75 bat', replace_fractions(u'ape 3 3/4 bat'))
        self.assertEqual(u'ape 3.75 bat', replace_fractions(u'ape 3¾ bat'))
        self.assertEqual(u'ape 3.75 bat', replace_fractions(u'ape 3 ¾ bat'))
        self.assertEqual(u'    2.5 cups flour', replace_fractions(u'    2½ cups flour'))

    def test60_convert_units_line(self):
        self.assertEqual(u'2.4 dl', convert_units_line(u'1 cup', from_system='us', to_system='eur'))
        self.assertEqual(u'2.4 dl', convert_units_line(u'1 CuPs', from_system='us', to_system='eur'))
        
        self.assertEqual(u'1 Family', convert_units_line(u'1 Family', from_system='us', to_system='eur'))
        self.assertEqual(u'176.7 C', convert_units_line(u'350F', from_system='us', to_system='eur'))
        self.assertEqual(u'176.7 C', convert_units_line(u'350 F', from_system='us', to_system='eur'))
        self.assertEqual(u'176.7 C', convert_units_line(u'350 degrees F', from_system='us', to_system='eur'))
        self.assertEqual(u'176.7 C', convert_units_line(u'350 degrees', from_system='us', to_system='eur'))

    def test61_round_trip(self):
        self.assertEqual(u'1.0 dl', convert_units_line(u'1 dl', from_system='eur', to_system='eur'))
        


    def test7_multiple_conversions_per_line(self):
        self.assertEqual(u'2.4 dl sugar and 56.7 g water',
                         convert_units_line(u'1 cup sugar and 2 oz water',
                                              from_system='us',
                                              to_system='eur'))        

        self.assertEqual(u'2.4 dl sugar and 4.7 dl water',
                         convert_units_line(u'1 cup sugar and 2 cups water',
                                              from_system='us',
                                              to_system='eur'))        

        self.assertEqual(u'1.0 tbsp sugar and 1.0 tsp water',
                         convert_units_line(u'1 tbsp sugar and 1 tsp water',
                                              from_system='us',
                                              to_system='eur'))        


    def test8_units_with_same_name(self):
        self.assertEqual(u'0.8 pint water and 1.7 pint beer',
                         convert_units_line(u'1 pint water and 2 pints beer',
                                              from_system='us',
                                              to_system='uk'))        


if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
