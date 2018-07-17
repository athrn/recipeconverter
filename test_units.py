# -*- coding: utf-8 -*-
import unittest as ut
import re

from units import *

def assert_close(x, y, err=1e-3):
    if abs(x-y) > err:
        raise AssertionError('Not Close: {!r} <> {!r} diff={}'.format(x,y,abs(x-y)))
    

class Tests(ut.TestCase):
    def test1_convert_unit(self):
        assert_close(2*2.36588, convert_unit(2, units.us_cup, units.eur_dl))
        assert_close(94.6353, convert_unit(2, units.us_pint, units.eur_cl))        
        assert_close(0.141096, convert_unit(4, units.eur_g, units.us_oz))
        
        assert_close(0.83267, convert_unit(1, units.us_pint, units.uk_pint))

    def test1_find_closest_unit(self):
        self.assertEqual(units.eur_dl, find_closest_unit(units.us_cup, 'eur'))
        self.assertEqual(units.us_quart, find_closest_unit(units.eur_l, 'us'))
        self.assertEqual(units.eur_g, find_closest_unit(units.us_oz, 'eur'))

        self.assertEqual(units.eur_tbsp, find_closest_unit(units.us_tbsp, 'eur'))
        self.assertEqual(units.eur_tsp, find_closest_unit(units.us_tsp, 'eur'))

        
    def test2_convert_to_system(self):
        (amount, unit) = convert_to_system(2, units.us_cup, 'eur')
        self.assertEqual(units.eur_dl, unit)
        assert_close(2*2.36588, amount)

    def test3_temperature(self):
        (amount, unit) = convert_to_system(2, units.us_F, 'eur')
        self.assertEqual(units.eur_C, unit)
        assert_close((2-32)/1.8, amount)

        (amount, unit) = convert_to_system(2, units.eur_C, 'us')
        self.assertEqual(units.us_F, unit)
        assert_close(2*1.8+32, amount)

    def test5_match_patterns(self):
        for unit in Unit.all_:
            try:
                rex = re.compile(unit.pattern, re.I)
            except:
                print(repr(unit))
                raise
            
            self.assert_(rex.match(unit.name), msg=repr(unit))

    # TODO: Better testing of regexps


if __name__ == "__main__":
    ut.main(failfast=True, exit=False)
    
