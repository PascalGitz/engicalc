# EngiCalc


EngiCalc is a Python package designed to assist engineers in performing
frequent calculations more efficiently. It aims to replace Excel in the
daily workflow by providing easily readable calculation sheets in
Jupyter Notebooks, which can then be output as Word files using Quarto.
Python code is easier to check for errors, making it a more reliable
choice for engineering calculations.

## Installation

You can install EngiCalc using `pip install engicalcs`.

## Functionality

The core features of the package are shown in the following paragraphs.
Be aware, the rendering is off for the github flavoured markdown format
(gfm). It is properly displayed in a Jupyternotebook.

``` python
import engicalc as e
import numpy as np
```

### Integration of Pint units

#### Common Units

Common units are stored as variables and are automatically imported with
the package. The following units are available:

``` python
for unit in e.units.items():
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

Units can be added using operators:

``` python
v = 30 *e.kNm

v_t = v + 30*e.kNm
```

You can also access the full unit registry:

``` python
u = 400 *e.ureg.hours

print(u)
```

    400 h

Convert units using Pint:

``` python
u.to(e.s)
```

$1440000\ \mathrm{s}$

### Parsing

#### Cell Parsing

A simple parsing function extracts calculations from a cell:

``` python
v = 30 *e.kNm

v_t = v + 30*e.kNm

e.parse_cell()
```

    [{'variable_name': 'v',
      'expression': '30 * e.kNm',
      'result': <Quantity(30, 'kNm')>},
     {'variable_name': 'v_t',
      'expression': 'v + 30 * e.kNm',
      'result': <Quantity(60, 'kNm')>}]

##### Drawbacks

- The parsing function loses datatype information, returning rows as
  strings.
- Currently only assignments work, no conditionals, or other python
  syntax

``` python
b = 20 

if b >20:
    b = 40

e.parse_cell()
```

    [{'variable_name': 'b', 'expression': '20', 'result': 20},
     {'variable_name': 'b', 'expression': '40', 'result': 40}]

### Markdown ec.rendering

Parsed cell content is processed using `sympy.sympify` and converted to
`latex` via the `sympy` latexprinter. Eventually the `latex`code is
inserted into a Markdown math environment. The `render()`function is
capable of the following:

#### Numeric representation

The numeric representation shows the Variablename and its value.

``` python
v = 30 *e.kNm

v_t = v + 30*e.kNm


Theta_pl_A= 5 
m_u_A = 10 
m_y_A=5
l=1
b_w=0.1
EI_II=20
q_S1_A= 10

e.render(symbolic=True)
```

$$\begin{aligned}v& = 30 \cdot \mathrm{kNm} = 30 \ \mathrm{kNm} \\ v_{t}& = v + 30 \cdot \mathrm{kNm} = 60 \ \mathrm{kNm} \\ \Theta_{pl A}& = 5 \\ m_{u A}& = 10 \\ m_{y A}& = 5 \\ l& = 1 \\ b_{w}& = 0.1 \\ EI_{II}& = 20 \\ q_{S1 A}& = 10\end{aligned}$$

#### Symbolic Representation

The symbolic representation is also showing the calculation.

``` python
alpha_u_A = np.sqrt(Theta_pl_A) / 2
Delta = ((np.sin(alpha_u_A) + (m_u_A - m_y_A) * l * b_w / (3 * EI_II)) * 24 * EI_II / l**3)*e.m
q_u_A = Delta + q_S1_A*e.m
e.render(raw=True)
```

    '$$\\begin{aligned}\\alpha_{u A}& = \\frac{\\sqrt{\\Theta_{pl A}}}{2} = 1.12 \\\\ \\Delta& = \\left(\\sin{\\left(\\alpha_{u A} \\right)} + \\frac{\\left(m_{u A} - m_{y A}\\right) \\cdot l \\cdot b_{w}}{3 \\cdot EI_{II}}\\right) \\cdot 24 \\cdot EI_{II} \\cdot \\frac{1}{l^{3}} \\cdot \\mathrm{m} = 435.64 \\ \\mathrm{m} \\\\ q_{u A}& = \\Delta + q_{S1 A} \\cdot \\mathrm{m} = 445.64 \\ \\mathrm{m}\\end{aligned}$$'

##### Only symbolic

As a sidefunctionality, only the symbolic part can be shown.

``` python
Delta
l
x = 2*Delta
e.render(symbolic=True, numeric=False)
```

$$\begin{aligned}\Delta& = \left(\sin{\left(\alpha_{u A} \right)} + \frac{\left(m_{u A} - m_{y A}\right) \cdot l \cdot b_{w}}{3 \cdot EI_{II}}\right) \cdot 24 \cdot EI_{II} \cdot \frac{1}{l^{3}} \cdot \mathrm{m} \\ l& = 1 \\ x& = 2 \cdot \Delta\end{aligned}$$

#### Recalling variables

The defined variables in the notebook are stored in a container. They
can be recalled at anytime and ec.rendered again.

``` python
v
Delta

e.render()
```

$$\begin{aligned}v& = 30 \cdot \mathrm{kNm} = 30 \ \mathrm{kNm} \\ \Delta& = \left(\sin{\left(\alpha_{u A} \right)} + \frac{\left(m_{u A} - m_{y A}\right) \cdot l \cdot b_{w}}{3 \cdot EI_{II}}\right) \cdot 24 \cdot EI_{II} \cdot \frac{1}{l^{3}} \cdot \mathrm{m} = 435.64 \ \mathrm{m}\end{aligned}$$

#### Multiple Rows

The markdown math environment is capable of displaying the equations in
multiple rows:

``` python
v
Delta
Theta_pl_A
EI_II
v_t
e.render(rows=3, symbolic=False)
e.render(rows=5, symbolic=False)
```

$$\begin{aligned}v& = 30 \ \mathrm{kNm} \quad & \Delta& = 435.64 \ \mathrm{m} \quad & \Theta_{pl A}& = 5 \\ EI_{II}& = 20 \quad & v_{t}& = 60 \ \mathrm{kNm} \quad & \end{aligned}$$

$$\begin{aligned}v& = 30 \ \mathrm{kNm} \quad & \Delta& = 435.64 \ \mathrm{m} \quad & \Theta_{pl A}& = 5 \quad & EI_{II}& = 20 \quad & v_{t}& = 60 \ \mathrm{kNm}\end{aligned}$$

#### Numpy functions

The package is based around the numpy functions and they should be used.
Currently the `numpy.`is stripped and the numpyfunction gets translated
to `sympy` via `sympy.sympify`.

``` python
alpha = 45*e.deg
test = np.atan(alpha.to(e.los) + 25)

e.render(raw=True)
```

    '$$\\begin{aligned}\\alpha& = 45 \\cdot \\mathrm{°} = 45 \\ \\mathrm{°} \\\\ test& = \\operatorname{atan}{\\left(\\alpha + 25 \\right)} = 1.53 \\ \\mathrm{rad}\\end{aligned}$$'

An array is translated to a matrix.

``` python
F_x = np.abs(np.array([-13,30,23,12])*e.kN)
F_v = F_x * 2
F_z = F_x*np.atan(alpha)**np.sqrt(1)
F_y = F_x * F_v
e.render(symbolic=True)
```

$$\begin{aligned}F_{x}& = \left|{\left[\begin{matrix}- 13 \cdot \mathrm{kN}\\30 \cdot \mathrm{kN}\\23 \cdot \mathrm{kN}\\12 \cdot \mathrm{kN}\end{matrix}\right]}\right| = \left[\begin{matrix}13\\30\\23\\12\end{matrix}\right] \ \mathrm{kN} \\ F_{v}& = F_{x} \cdot 2 = \left[\begin{matrix}26\\60\\46\\24\end{matrix}\right] \ \mathrm{kN} \\ F_{z}& = F_{x} \cdot \operatorname{atan}^{\sqrt{1}}{\left(\alpha \right)} = \left[\begin{matrix}8.66\\19.97\\15.31\\7.99\end{matrix}\right] \ \mathrm{kN} \cdot \mathrm{rad} \\ F_{y}& = F_{x} \cdot F_{v} = \left[\begin{matrix}338\\1800\\1058\\288\end{matrix}\right] \ \mathrm{kN}^{2}\end{aligned}$$

#### Raw Markdown

As the markdowncode is stored anyways, it can be output aswell. Could be
used to copy into a table.

``` python
v
Delta
Theta_pl_A
e.render(symbolic=True, raw=True)
```

    '$$\\begin{aligned}v& = 30 \\cdot \\mathrm{kNm} = 30 \\ \\mathrm{kNm} \\\\ \\Delta& = \\left(\\sin{\\left(\\alpha_{u A} \\right)} + \\frac{\\left(m_{u A} - m_{y A}\\right) \\cdot l \\cdot b_{w}}{3 \\cdot EI_{II}}\\right) \\cdot 24 \\cdot EI_{II} \\cdot \\frac{1}{l^{3}} \\cdot \\mathrm{m} = 435.64 \\ \\mathrm{m} \\\\ \\Theta_{pl A}& = 5\\end{aligned}$$'

#### Special Characters

Some special characters are inserted in the string before the sympy
conversion takes place. In the `output` module, a replacement dictionary
is created to replace the special characters. This can be expanded. It
has to correspond to the `latex` syntax.

``` python
diam_infty = 20

infty__infty_infty__diam = 10
e.render(raw=False)
```

$$\begin{aligned}\oslash_{\infty}& = 20 \\ \infty^{\infty \oslash}_{\infty}& = 10\end{aligned}$$

#### Pint unit handling

``` python
v = v_t.to(e.Nm) + 30*2*e.Nm
q = v_t.magnitude*e.Nm + v
q__shortcut = v_t.m * e.Nm + v
e.render()
```

$$\begin{aligned}v& = v_{t} + 30 \cdot 2 \cdot \mathrm{Nm} = 60060.0 \ \mathrm{Nm} \\ q& = v_{t} \cdot \mathrm{Nm} + v = 60120.0 \ \mathrm{Nm} \\ q^{shortcut}& = v_{t} \cdot \mathrm{Nm} + v = 60120.0 \ \mathrm{Nm}\end{aligned}$$

#### Functions

It can be useful to display the calculations that have been done in a
function environment. For that there is a second parsing function. The
Funcion parses the local variables.

``` python
from IPython.display import Markdown
```

``` python
def test(alpha__top, b):
    x = alpha__top + b 
    y = alpha__top-b*2
    z = x + y
    display(Markdown('**Only Symbolic representation**'))
    e.render_func(numeric=False ,rows=2)
    display(Markdown('**Whole representation**'))
    e.render_func(numeric=True ,rows=3)
    return z

```

``` python
z = test(3,4)
```

**Only Symbolic representation**

$$\begin{aligned}\alpha^{top}& = 3 \quad & b& = 4 \\ x& = \alpha^{top} + b \quad & y& = \alpha^{top} - b \cdot 2 \\ z& = x + y \quad & \end{aligned}$$

**Whole representation**

$$\begin{aligned}\alpha^{top}& = 3 \quad & b& = 4 \quad & x& = \alpha^{top} + b = 7 \\ y& = \alpha^{top} - b \cdot 2 = -5 \quad & z& = x + y = 2 \quad & \end{aligned}$$

``` python
z__2 = test(5*e.kNm + 3*e.kNm, 3*e.kNm)
```

**Only Symbolic representation**

$$\begin{aligned}\alpha^{top}& = 8 \ \mathrm{kNm} \quad & b& = 3 \ \mathrm{kNm} \\ x& = \alpha^{top} + b \quad & y& = \alpha^{top} - b \cdot 2 \\ z& = x + y \quad & \end{aligned}$$

**Whole representation**

$$\begin{aligned}\alpha^{top}& = 8 \ \mathrm{kNm} \quad & b& = 3 \ \mathrm{kNm} \quad & x& = \alpha^{top} + b = 11 \ \mathrm{kNm} \\ y& = \alpha^{top} - b \cdot 2 = 2 \ \mathrm{kNm} \quad & z& = x + y = 13 \ \mathrm{kNm} \quad & \end{aligned}$$

##### Drawback

The `render` function parses the assignments inside the function.

``` python
def test2(a, b):
    x = a + b 
    y = a**b
    z = x + y
    return z

e.render()
```

$$\begin{aligned}x& = a + b = None \\ y& = a^{b} = None \\ z& = x + y = None\end{aligned}$$

``` python
z = test2(3,4)

e.render()
```

$$\begin{aligned}z& = \operatorname{test}_{2}{\left(3,4 \right)} = 88\end{aligned}$$

### Markdown tables

It can be useful to summarize the calculations in a table. For that the
variables can easily be inserted into the table.

``` python
import pandas as pd
```

``` python


# Example lists
col_1 = e.render_list([z, Delta, q__shortcut, v_t], raw=True)
names = ['Höhe', 'Differenz', 'Test', 'Test3']

# Define column names
columnnames = ['Bezeichnung', 'Berechnung']

# Create DataFrame
DF = pd.DataFrame(list(zip(names, col_1)), columns=columnnames)

# Display the DataFrame
display(DF)
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|     | Bezeichnung | Berechnung                                           |
|-----|-------------|------------------------------------------------------|
| 0   | Höhe        | \$\$\begin{aligned}z& = \operatorname{test}\_{2}{... |
| 1   | Differenz   | \$\$\begin{aligned}\Delta& = \left(\sin{\left(\a...  |
| 2   | Test        | \$\$\begin{aligned}q^{shortcut}& = v\_{t} \cdot \\.. |
| 3   | Test3       | \$\$\begin{aligned}v\_{t}& = v + 30 \cdot \mathrm... |

</div>
