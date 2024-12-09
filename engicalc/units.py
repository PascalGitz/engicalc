"""
Definiert alle relevanten Einheiten.
"""

from pint import UnitRegistry

# Erstellen eines UnitRegistry-Objekts
ureg = UnitRegistry()
ureg.formatter.default_format = "~P"

ureg.define('Nm = newton * meter')
ureg.define('kNm = kilonewton * meter')

# Definition aller relevanten Einheiten
kg = ureg.kg
t = ureg.t

mm = ureg.mm
cm = ureg.cm
dm = ureg.dm
m = ureg.m
km = ureg.km

N = ureg.N
kN = ureg.kN
MN = ureg.MN

kNm = ureg.kNm
Nm = ureg.Nm

rad = ureg.rad
deg = ureg.degree

percent = ureg.percent
permille = ureg.permille
s = ureg.s

degC = ureg.degC

MPa = ureg.MPa
los = ureg.dimensionless