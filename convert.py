# -*- coding: utf-8 -*-
import re

# # SI Volume        
# m3 = Volume('si', 'm3', 1.0, 'cubicmeter')

# # SI Volume
# # m3 = 1
# l = m3*1e-3
# dl = 0.1*l
# ml = l*1e-3    
# kg = 1
# g = 1e-3*kg

# us_cup=2.3659*dl
# us_pint= 2*us_cup
# us_tbsp=us_cup / 16
# us_tsp=us_cup / 48
# us_floz=us_cup / 8
# us_quart=2*us_pint

re_flags=re.I


unicode_fractions = {u'¾': '3/4',
                     u'½': '1/2',
                     u'¼': '1/4',
                     unichr(0x2153): '2/3',
                     unichr(0x2154): '2/3',
                     }

def replace_unicode_fractions(line):
    for ufrac, frac in unicode_fractions.items():
        line = re.sub(r'(\d+)\s*' + ufrac, r'\1 ' + frac, line, flags=re_flags)
        line = re.sub(ufrac, frac, line, flags=re_flags)

    return line

def replace_text_fractions(line):
    pattern = ur'(\d+\s*)?(\d+)/(\d+)'
    m = re.search(pattern, line, flags=re_flags)
    if m:
        (i, n, d) = m.groups()
        i = 0 if not i else int(i)
        n, d = int(n), int(d)
        line = re.sub(pattern,
                      str(int(i) + float(n)/d),
                      line,
                      flags=re_flags)

    return line

def replace_fractions(line):
    line = replace_unicode_fractions(line)
    line = replace_text_fractions(line)
    return line

def aliases(unit):
    # Plural first.
    # yield unit+'s'
    yield unit


from units import units, convert_to_system

def convert_units_line(line, from_system, to_system):

    for type_ in units[from_system]:
        for name,unit in units[from_system][type_].items():
            pattern = r'(\d+(\.\d+)?)(\s*){}(?![a-z])'.format(unit.pattern)

            matches = list(re.finditer(pattern, line, flags=re_flags))
            if matches:
                new_line = ''
                pos = 0
                for m in matches:
                    new_line += line[pos:m.start()]

                    amount = float(m.group(1))
                    conv_amount, conv_unit = convert_to_system(amount, unit, to_system)
                    new_line += '{:.1f} {}'.format(conv_amount, conv_unit.name)

                    pos = m.end()

                new_line += line[pos:]
                line = new_line


    return line

def convert(recipe, to='eur', from_='us'):

    converted = []
    for line in recipe.splitlines():
        line = replace_fractions(line)
        line = convert_units_line(line, from_system=from_, to_system=to)
        converted.append(line)

    return '\n'.join(converted)

# def convert_file(filename, to, from_):
#     # TODO: Detect encodings...
#     text = open(filename, encoding='utf-8').read()
#     return convert(text, to=to, from_=from_)

if __name__ == "__main__":
    import unittest as ut
    ut.main(module='test_convert', failfast=True, exit=False)

    from codecs import open
    recipe = open('recipe.txt', encoding='utf-8').read()
    converted = convert(recipe)
    print(converted)
    
