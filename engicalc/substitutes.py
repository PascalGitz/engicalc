from engicalc.units import ureg, units


# Units substitution
replacements_units = {}
for unit in units.items():
    formatted_unit = f"\\\mathrm{{{str(unit[1])}}}"
    replacements_units[unit[0]] = f'Symbol("{formatted_unit.replace("deg", "°")}")'



# special characters.
replacements_specials ={
        #special characters
        'diam': r'\\oslash',
        'eps':'varepsilon', #convenience
        'infty': r'\\infty',
}