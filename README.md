# My Project


# EngiCalc

EngiCalc is a Python package designed to assist engineers in performing
frequent calculations more efficiently. It aims to replace Excel in the
daily workflow by providing easily readable calculation sheets in
Jupyter Notebooks, which can then be output as Word files using Quarto.
Python code is easier to check for errors, making it a more reliable
choice for engineering calculations.

## Installation

Install from this Repo

``` python
from engicalc import *
```

## Functionality

### Integration of Pint units

#### Common Units

common units are stored in variables. They are imported with the import
of the package

``` python
for unit in units.items():
    print(unit[1])
```

    kg
    t
    kNm
    Nm
    N
    kN
    MN
    m
    cm
    dm
    mm
    km
    rad
    deg
    %
    ‰
    s
    °C
    K
    MPa

#### Handling Units

Units can be added with operators:

``` python
v = 30 *kNm

v_t = v + 30*kNm
```

The whole unit registry is imported and can always be accessed:

``` python
u = 400 *ureg.hours

print(u)
```

    400 h

pint conversion

``` python
u.to(s)
```

$1440000\ \mathrm{s}$

### Markdown rendering

#### Numeric representation

``` python
v = 30 *kNm

v_t = v + 30*kNm

put_out(symbolic=False)
```

$$\begin{aligned}v& = 30 \ \mathrm{kNm} \\ v_{t}& = 60 \ \mathrm{kNm}\end{aligned}$$

#### Symbolic Representation

using Sympy sympify for the symbolic representation

``` python
import sympy as sp
```

``` python
sp.sympify("M_Rd__GZT2")
```

$\displaystyle M^{GZT2}_{Rd}$

``` python
M_Rd__GZT2 = 40*kNm 

M_Rd__Top = 2130*kNm 

M_Rd__Bot = 44*kNm


M_Rd = ((M_Rd__GZT2 + M_Rd__Top+M_Rd__Bot + 3409.31*kNm) / (40*m) * 32*cm ).to(kNm)

put_out()
```

$$\begin{aligned}M^{GZT2}_{Rd}& = 40 \cdot \mathrm{kNm} = 40 \ \mathrm{kNm} \\ M^{Top}_{Rd}& = 2130 \cdot \mathrm{kNm} = 2130 \ \mathrm{kNm} \\ M^{Bot}_{Rd}& = 44 \cdot \mathrm{kNm} = 44 \ \mathrm{kNm} \\ M_{Rd}& = \left(M^{GZT2}_{Rd} + M^{Top}_{Rd} + M^{Bot}_{Rd} + 3409.31 \cdot \mathrm{kNm}\right) \cdot \frac{1}{40 \cdot \mathrm{m}} \cdot 32 \cdot \mathrm{cm} = 44.99 \ \mathrm{kNm}\end{aligned}$$

``` python
Theta_pl_A= 5 
m_u_A = 10 
m_y_A=5
l=1
b_w=0.1
EI_II=20
q_S1_A= 10

put_out()
```

$$\begin{aligned}\Theta_{pl A}& = 5 \\ m_{u A}& = 10 \\ m_{y A}& = 5 \\ l& = 1 \\ b_{w}& = 0.1 \\ EI_{II}& = 20 \\ q_{S1 A}& = 10\end{aligned}$$

``` python
alpha_u_A = np.sqrt(Theta_pl_A) / 2
Delta = ((np.sin(alpha_u_A) + (m_u_A - m_y_A) * l * b_w / (3 * EI_II)) * 24 * EI_II / l**3)*m
q_u_A = Delta + q_S1_A*m
put_out()
```

$$\begin{aligned}\alpha_{u A}& = \frac{\sqrt{\Theta_{pl A}}}{2} = 1.12 \\ \Delta& = \left(\sin{\left(\alpha_{u A} \right)} + \frac{\left(m_{u A} - m_{y A}\right) \cdot l \cdot b_{w}}{3 \cdot EI_{II}}\right) \cdot 24 \cdot EI_{II} \cdot \frac{1}{l^{3}} \cdot \mathrm{m} = 435.64 \ \mathrm{m} \\ q_{u A}& = \Delta + q_{S1 A} \cdot \mathrm{m} = 445.64 \ \mathrm{m}\end{aligned}$$

##### Only symbolic

``` python
M_Rd

put_out(numeric=False)
```

$$\begin{aligned}M_{Rd}& = \left(M^{GZT2}_{Rd} + M^{Top}_{Rd} + M^{Bot}_{Rd} + 3409.31 \cdot \mathrm{kNm}\right) \cdot \frac{1}{40 \cdot \mathrm{m}} \cdot 32 \cdot \mathrm{cm}\end{aligned}$$

#### Recalling variables

``` python
v
M_Rd

put_out()
```

$$\begin{aligned}v& = 30 \cdot \mathrm{kNm} = 30 \ \mathrm{kNm} \\ M_{Rd}& = \left(M^{GZT2}_{Rd} + M^{Top}_{Rd} + M^{Bot}_{Rd} + 3409.31 \cdot \mathrm{kNm}\right) \cdot \frac{1}{40 \cdot \mathrm{m}} \cdot 32 \cdot \mathrm{cm} = 44.99 \ \mathrm{kNm}\end{aligned}$$

#### Multiple Rows

``` python
v
M_Rd__Bot
M_Rd__Top
put_out(rows=3, symbolic=False)
```

$$\begin{aligned}v& = 30 \ \mathrm{kNm} \quad & M^{Bot}_{Rd}& = 44 \ \mathrm{kNm} \quad & M^{Top}_{Rd}& = 2130 \ \mathrm{kNm}\end{aligned}$$

#### Numpy functions

``` python
alpha = 45*deg
test = np.atan(alpha + 25*deg)

put_out()
```

$$\begin{aligned}\alpha& = 45 \cdot \mathrm{°} = 45 \ \mathrm{°} \\ test& = \operatorname{atan}{\left(\alpha + 25 \cdot \mathrm{°} \right)} = 0.88 \ \mathrm{rad}\end{aligned}$$

``` python
F_x = np.abs(np.array([-13,30,23,12])*kN)
F_z = F_x*np.atan(alpha)

put_out()
```

$$\begin{aligned}F_{x}& = \left|{\left[\begin{matrix}- 13 \cdot \mathrm{kN}\\30 \cdot \mathrm{kN}\\23 \cdot \mathrm{kN}\\12 \cdot \mathrm{kN}\end{matrix}\right]}\right| = \left[\begin{matrix}13\\30\\23\\12\end{matrix}\right] \ \mathrm{kN} \\ F_{z}& = F_{x} \cdot \operatorname{atan}{\left(\alpha \right)} = \left[\begin{matrix}8.66\\19.97\\15.31\\7.99\end{matrix}\right] \ \mathrm{kN} \cdot \mathrm{rad}\end{aligned}$$

#### Raw Markdown

``` python
v
M_Rd__Bot
M_Rd__Top
put_out(symbolic=False, raw=True)
```

$$\begin{aligned}v& = 30 \ \mathrm{kNm} \\ M^{Bot}_{Rd}& = 44 \ \mathrm{kNm} \\ M^{Top}_{Rd}& = 2130 \ \mathrm{kNm}\end{aligned}$$

    $$\begin{aligned}v& = 30 \ \mathrm{kNm} \\ M^{Bot}_{Rd}& = 44 \ \mathrm{kNm} \\ M^{Top}_{Rd}& = 2130 \ \mathrm{kNm}\end{aligned}$$

#### Special Characters

``` python
diam_infty = 20

infty__infty_infty__diam = 10
put_out(raw=False)
```

$$\begin{aligned}\oslash_{\infty}& = 20 \\ \infty^{\infty \oslash}_{\infty}& = 10\end{aligned}$$
