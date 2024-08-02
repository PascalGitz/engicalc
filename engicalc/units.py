"""
Definiert alle relevanten Einheiten.
"""

from pint import UnitRegistry

# Erstellen eines UnitRegistry-Objekts
ureg = UnitRegistry()
ureg.formatter.default_format = "~P"

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

rad = ureg.rad
deg = ureg.degree

percent = ureg.percent
s = ureg.s

MPa = ureg.MPa
los = ureg.dimensionless