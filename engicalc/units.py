"""
Definiert alle relevanten Einheiten.
"""
from pint import UnitRegistry

# Erstellen eines UnitRegistry-Objekts
ureg = UnitRegistry()
ureg.formatter.default_format = "~P"

ureg.define('Nm = newton * meter')
ureg.define('kNm = kilonewton * meter')


units = {"kg": ureg.kg,
         "t": ureg.t,

         "kNm": ureg.kNm,
         "Nm": ureg.Nm,

         "N": ureg.N,
         "kN": ureg.kN,
         "MN": ureg.MN,
         
         "m": ureg.m,
         "cm": ureg.cm,
         "dm": ureg.dm,
         "mm": ureg.mm,
         "km": ureg.km,

         "rad": ureg.rad,
         "deg": ureg.deg,

         "precent": ureg.percent,
         "permille": ureg.permille,

         "s": ureg.s,

         "degC": ureg.degC,
         "K": ureg.kelvin,

         "MPa": ureg.MPa,
         "los": ureg.dimensionless


         }


globals().update(units)

