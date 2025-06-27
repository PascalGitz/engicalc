from pint import UnitRegistry

# Erstellen eines UnitRegistry-Objekts
ureg = UnitRegistry()
ureg.formatter.default_format = "~P"

ureg.define('Nm = newton * meter')
ureg.define('kNm = kilonewton * meter')

# Define unit variables as globals
kg = ureg.kg
t = ureg.t
kNm = ureg.kNm
Nm = ureg.Nm
N = ureg.N
kN = ureg.kN
MN = ureg.MN
m = ureg.m
cm = ureg.cm
dm = ureg.dm
mm = ureg.mm
km = ureg.km
rad = ureg.rad
deg = ureg.deg
percent = ureg.percent
permille = ureg.permille
s = ureg.s
degC = ureg.degC
K = ureg.kelvin
MPa = ureg.MPa
Hz = ureg.hertz
los = ureg.dimensionless

# Build the units dictionary only from the explicitly defined unit variables above
units = {
    "kg": kg,
    "t": t,
    "kNm": kNm,
    "Nm": Nm,
    "N": N,
    "kN": kN,
    "MN": MN,
    "m": m,
    "cm": cm,
    "dm": dm,
    "mm": mm,
    "km": km,
    "rad": rad,
    "deg": deg,
    "percent": percent,
    "permille": permille,
    "s": s,
    "degC": degC,
    "K": K,
    "MPa": MPa,
    "Hz": Hz,
    "los": los
}