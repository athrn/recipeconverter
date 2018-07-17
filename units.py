# -*- coding: utf-8 -*-
from collections import defaultdict
from functools import partial
from pprint import pformat

def add_keys(dict_, keys):
    d = dict_
    for key in keys:
        if key not in d:
            d[key] = dict()

        d = d[key]

class PrettyUnits(object):   

    def __init__(self, units):
        self.all = []
        self.by_system = {}
        for unit in units:
            for system in unit.systems:                
                key = '{}_{}'.format(system, unit.name.replace(' ', '_'))

                # Access by property
                setattr(self, key, unit)

                # Access by dict
                add_keys(self.by_system, [system, unit.type_, unit.name])
                self.by_system[system][unit.type_][unit.name] = unit

    def __getitem__(self, key):
        return self.by_system[key]

    def __repr__(self):
        return pformat(self.by_system)


class Unit(object):
    all_ = []

    def __init__(self, systems, type_, name, pattern, amount):
        if isinstance(systems, basestring):
            self.systems = systems.split()
        else:
            self.systems = systems
        
        self.type_ = type_
        self.name = name
        self.pattern = pattern
        self.amount = amount

        Unit.all_.append(self)
        
    def new_scaled(self, scale_factor, name, pattern, systems=None):
        u = Unit(systems=systems if systems else self.systems,
                 type_=self.type_,
                 name=name,
                 pattern=pattern,
                 amount=self.amount*scale_factor,
                 )
        return u

    def __str__(self):
        system = ':'.join(self.systems)
        return '{}_{}'.format(system, self.name)

    def __repr__(self):
        # return 'Unit(systems={self.systems!r}, type_={self.type_!r}, name={self.name!r}, pattern={self.pattern!r}, amount={self.amount!r}'.format(self=self)
        return 'Unit({self.systems!r}, {self.type_!r}, {self.name!r}, {self.pattern!r}, {self.amount!r}'.format(self=self)


def convert_temperature(amount, from_, to):
    if from_ == 'F' and to == 'C':
        return (amount - 32)/1.8
    elif from_ == 'C' and to == 'F':
        return amount*1.8 + 32
    else:
        raise NotImplemented('Unknown temperature conversion {}->{}'.format(from_, to))

def convert_unit(amount, from_unit, to_unit):
    assert from_unit.type_ == to_unit.type_

    if from_unit.type_ == 'temperature':
        return convert_temperature(amount, from_unit.name, to_unit.name)
    
    return amount*from_unit.amount/to_unit.amount

def find_closest_unit(from_unit, to_system):
    dist = []
    for name, to_unit in units.by_system[to_system][from_unit.type_].items():
        dist.append((abs(from_unit.amount - to_unit.amount), to_unit))

    return sorted(dist)[0][1]

def convert_to_system(amount, from_unit, to_system):
    conv_unit = find_closest_unit(from_unit, to_system)
    # global units
    # uts = units.by_system[to_system][from_unit.type_]
    # conv_unit = uts.values()[0]
    conv_amount = convert_unit(amount, from_unit, conv_unit)
    return (conv_amount, conv_unit)


m3=Unit('si', 'volume', 'm3', '(m3|cubicmeter(s)?)', 1.0)

l=m3.new_scaled(1./1000, 'l', '(l|liter(s)?|litre(s)?)', systems='eur')
dl=l.new_scaled(0.1, 'dl', '(dl|deciliter(s)?)')
cl=l.new_scaled(0.01, 'cl', '(cl|centiliter(s)?)')
ml=l.new_scaled(0.001, 'ml', '(ml|milliliter(s)?)')
tsp=l.new_scaled(0.005, 'tsp', '(tsp|teaspoon(s)?)')
tbsp=l.new_scaled(0.015, 'tbsp', '(tbsp|tablespoon(s)?)')

us_cup=dl.new_scaled(2.36588, 'cup', 'cup(s)?', systems='us')
us_floz=us_cup.new_scaled(1./8, 'fl oz', '(fl\.? oz\.?|fluid ounce(s)?)')
us_tbsp=us_cup.new_scaled(1./16, 'tbsp', '(tbsp|tablespoon(s)?)')
us_tsp=us_cup.new_scaled(1./48, 'tsp', '(tsp|teaspoon(s)?)')
us_pint= us_cup.new_scaled(2., 'pint', '(pt|pint(s)?)') 
us_quart=us_pint.new_scaled(2., 'quart', '(qt|quart(s)?)')

uk_pint=dl.new_scaled(5.6826, 'pint', 'pint(s)?', systems='uk')

kg=Unit('si eur', 'mass', 'kg', '(kg|kilogram(s)?)', 1.0)
g=kg.new_scaled(1e-3, 'g', '(g|gram(s)?)')

us_oz=g.new_scaled(28.3495, 'oz', '(oz|ounce(s)?)', systems='us')
us_pound=g.new_scaled(453.592, 'lbs', '(lb|pound)s?', systems='us')

C=Unit('si eur', 'temperature', 'C', '(C|celsius)', 1.0)
C=Unit('us', 'temperature', 'F', '(degrees F|F|degrees)', 1.0)


units = PrettyUnits(Unit.all_)

if __name__ == "__main__":
    print(units)
    
    import unittest as ut
    ut.main(module='test_units', failfast=True, exit=False)

