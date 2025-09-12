---
section-numbering:
  1.1.1
title:
  EngiCalc
toc-title:
  Table
  of
  contents
---

EngiCalc
is
a
Python
package
designed
to
assist
engineers
in
performing
frequent
calculations
more
efficiently.
It
aims
to
replace
Excel
in
the
daily
workflow
by
providing
easily
readable
calculation
sheets
in
Jupyter
Notebooks,
which
can
then
be
output
as
Word
files
using
Quarto.
Python
code
is
easier
to
check
for
errors,
making
it
a
more
reliable
choice
for
engineering
calculations.

## Examples

::: {.cell execution_count="23"}
``` {.python .cell-code}
from engicalc import *
import numpy as np
```
:::

### Parameters

::: {.cell execution_count="24"}
``` {.python .cell-code}
diam_sw = 12*mm
s_sw = 150*mm
z = 190*mm

f_sd = 435*N/mm**2
alpha = 25*deg

parameters = Cell(show_expression=False, rows=3)
```
:::

:::: {.cell execution_count="25"}
``` {.python .cell-code}
parameters
```

::: {.cell-output .cell-output-display .cell-output-markdown execution_count="25"}
$$\begin{aligned}& \oslash_{sw}=12 \ \mathrm{mm} \quad  s_{sw}=150 \ \mathrm{mm} \quad  z=190 \ \mathrm{mm} \\ &  f_{sd}=\frac{435.0 \ \mathrm{N}}{\mathrm{mm}^{2}} \quad  \alpha=25 \ \mathrm{°}\end{aligned}$$
:::
::::

:::: {.cell execution_count="26"}
``` {.python .cell-code}
print(parameters)
```

::: {.cell-output .cell-output-stdout}
    $$\begin{aligned}& \oslash_{sw}=12 \ \mathrm{mm} \quad  s_{sw}=150 \ \mathrm{mm} \quad  z=190 \ \mathrm{mm} \\ &  f_{sd}=\frac{435.0 \ \mathrm{N}}{\mathrm{mm}^{2}} \quad  \alpha=25 \ \mathrm{°}\end{aligned}$$
:::
::::

### Shearrestistance

:::: {.cell execution_count="27"}
``` {.python .cell-code}
a_sw = (diam_sw**2 / 4 * np.pi /s_sw).to(mm**2/m)
V_Rd__s = (z / np.tan(alpha) *  f_sd * a_sw).to(kN)

Cell(precision=2)
```

::: {.cell-output .cell-output-display .cell-output-markdown execution_count="27"}
$$\begin{aligned}& a_{sw}=\frac{\oslash_{sw}^{2} \ \pi}{4 \ s_{sw}}=\frac{753.98 \ \mathrm{mm}^{2}}{\mathrm{m}} \\ &  V^{s}_{Rd}=\frac{z \ f_{sd} \ a_{sw}}{\tan{\left(\alpha \right)}}=133.64 \ \mathrm{kN}\end{aligned}$$
:::
::::

### Function

the
function
body
is
indented

::: {.cell execution_count="28"}
``` {.python .cell-code}
def V_Rd__s(diam_sw, s_sw, f_s, z, alpha):
    a_s = (diam_sw**2 / 4 * np.pi /s_sw).to(mm**2/m)
    if a_s >= 20 *mm**2/m + diam_sw.m * mm**2 / m:
        alpha = 43*deg
    elif a_s >= 30 *mm**2/m:
        alpha = 22*deg
    else:
        alpha = alpha
    return (z / np.tan(alpha) *  f_s * a_s).to(kN)



V_Rd__s_visual = Cell(show_expression=True)
```
:::

:::: {.cell execution_count="29"}
``` {.python .cell-code}
V_Rd__s_visual
```

::: {.cell-output .cell-output-display .cell-output-markdown execution_count="29"}
$$\begin{aligned}&\end{aligned}$$
:::
::::

:::: {.cell execution_count="30"}
``` {.python .cell-code}
V_Rd__s__1 = V_Rd__s(10*mm, 150*mm, 435*N/mm**2, 200*mm, 25*deg)
V_Rd__s__2 = V_Rd__s(10*mm, 150*mm, 435*N/mm**2, 120*mm, 45*deg)

Cell()
```

::: {.cell-output .cell-output-display .cell-output-markdown execution_count="30"}
$$\begin{aligned}& V^{s 1}_{Rd}=V^{s}_{Rd}{\left(10 \ \mathrm{mm},150 \ \mathrm{mm},\frac{435 \ \mathrm{N}}{\mathrm{mm}^{2}},200 \ \mathrm{mm},25 \ \mathrm{°} \right)}=48.85 \ \mathrm{kN} \\ &  V^{s 2}_{Rd}=V^{s}_{Rd}{\left(10 \ \mathrm{mm},150 \ \mathrm{mm},\frac{435 \ \mathrm{N}}{\mathrm{mm}^{2}},120 \ \mathrm{mm},45 \ \mathrm{°} \right)}=29.31 \ \mathrm{kN}\end{aligned}$$
:::
::::

### Conditional

:::: {.cell execution_count="31"}
``` {.python .cell-code}
if alpha >= 25*deg:
    z = np.sqrt(300)*mm
elif alpha < 25*deg and alpha >= 10*deg:
    z = np.log(200*mm)
else:
    z = 500*mm

Cell(show_expression=True, show_name=True, show_value=True)
```

::: {.cell-output .cell-output-display .cell-output-markdown execution_count="31"}
$$\begin{aligned}&\end{aligned}$$
:::
::::

::: {.cell execution_count="32"}
``` {.python .cell-code}
b_w = 100*mm
f_cd = 20 *N/mm**2

params = Cell(rows=3, show_expression=False)
```
:::

::::: {.cell execution_count="33"}
``` {.python .cell-code}


A_s = diam_sw**2 / 4 * np.pi

x = A_s * f_sd /(0.85* b_w * f_cd)

calc = Cell()


display(params, calc)
```

::: {.cell-output .cell-output-display .cell-output-markdown}
$$\begin{aligned}& b_{w}=100 \ \mathrm{mm} \quad  f_{cd}=\frac{20.0 \ \mathrm{N}}{\mathrm{mm}^{2}}\end{aligned}$$
:::

::: {.cell-output .cell-output-display .cell-output-markdown}
$$\begin{aligned}& A_{s}=\frac{\oslash_{sw}^{2} \ \pi}{4}=113.1 \ \mathrm{mm}^{2} \\ &  x=\frac{A_{s} \ f_{sd}}{0.85 \ b_{w} \ f_{cd}}=28.94 \ \mathrm{mm}\end{aligned}$$
:::
:::::

## Installation

Install
from
this
Repo
