from IPython.display import Markdown, display 
from numpy import sqrt, pi, tan, arctan, cos, arccos, sin, arcsin, array, arange
from engicalc.units import ureg, kg, t, mm, cm, dm, m, km, N, kN, MN, rad, deg, percent, s, MPa, los
import matplotlib.pyplot as plt

def schneelast_charakteristisch_SIA261_9(mu_i:float, C_e:float, C_T:float, s_k:float, background=False):
    """
    Berechnung der charakteristischen Schneelast gemäss SIA 261:2014, Abschnitt 5.2.2\\
    Diese Funktion berechnet die charakteristische Schneelast basierend auf der Dachformbeiwerte, Windexposition und dem thermischen Beiwert.
    
    Parameter:
    ----------
    mu_i : float; 
        Der Dachformbeiwert.
        
    C_e : float; 
        Die Windexposition des Bauwerks. 

    C_T : float; 
        Der thermische Beiwert.

    s_k : float; 
        Schneelast auf horizontalem Gelände.
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 261:2014 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Die charakteristische Schneelast.
    
    Hinweise:
    -----
    5.2.4\\
    Je nach Windexposition des Bauwerks gilt für den Expositionsbeiwert Ce:\\
    normale Windexposition Ce = 1,0\\
    dem Wind stark ausgesetzte Lage Ce = 0,8\\
    vor Wind geschützte Lage Ce = 1,2\\
    5.2.5\\
    Der thermische Beiwert CT ist im Allgemeinen gleich 1,0 zu setzen. Die Annahme eines kleineren Beiwerts
    ist möglich, wenn ein grosser Wärmedurchgang an der Dachoberfläche den Schmelzprozess beschleunigt. 
    Der Einfluss des Ausfalls technischer Installationen auf den angenommenen Wärmedurchgang ist dabei zu 
    prüfen, beispielsweise bei Giasdächern über geheizten Räumen. 
  

    Beispiele:
    --------
    >>> schneelast_charakteristisch_SIA261_9(1.78*kN/m**2, 1.0, 1.0, 1.5)
    2.67*kN/m**2
    
    >>> schneelast_charakteristisch_SIA261_9(0.9*kN/m**2, 1.0, 1.0, 0.8)
    0.72*kN/m**2
    """

    if background == True:
        display(Markdown("""
*SIA 261:2014 Abschnitt 5.2.2 (9)*

Der charakteristische Wert der Schneelast auf Dächern, bezogen auf die überdeckte Grundrissfläche, beträgt:
$$ q_k = \\mu_i \\cdot C_e \\cdot C_T \\cdot s_k $$
        """))
        
    return mu_i * C_e * C_T * s_k


def schneelast_horizontal_charakteristisch_SIA261_10(h_0:float, background=False):
    """
    Berechnung der charakteristischen Schneelast auf horizontalem Gelände gemäss SI1 262:2014, Abschnitt 5.2.6\\
    Diese Funktion berechnet die charakteristische Schneelast basierend auf der Bezugshöhe h_0 in m.
    
    Parameter:
    ----------
    h_0 : float; 
        Die Bezugshöhe. Eingabe in m **dimensionslos!**
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 261:2014 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Die charakteristische Schneelast im horizontalen Gelände.
    
    Hinweise:
    -----
    Gemäss SIA 261:2014, Abschnitt 5.2.6, wird die charakteristische Schneelast im horizontalen Gelände bestimmt:
  

    Beispiele:
    --------
    >>> schneelast_horizontal_charakteristisch_SIA261_10(650)
    1.78 *kN/m**2
    
    >>> schneelast_horizontal_charakteristisch_SIA261_10(50)
    0.9 *kN/m**2
    """

    if background == True:
        display(Markdown("""
*SIA 261:2014 Abschnitt 5.2.6 (10)*

Der charakteristische Wert der Schneelast im horizontalen Gelände beträgt:
$$ s_k = \\left[1 + \\left(\\frac{h_0}{350}\\right)^2\\right] \\cdot 0{,}4 \\, \\text{kN/m}^2 \\geq 0{,}9 \\, \\text{kN/m}^2 $$
        """))
    


    return max((1 + (h_0 / 350)**2) * 0.4 *kN/m**2, 0.9 *kN/m**2)

def wind_staudruck_SIA261_11(c_h:float, q_p0:float, background=False):
    """
    Berechnung des Staudrucks gemäss SIA 261:2014, Abschnitt 6.2.1.1\\
    Diese Funktion berechnet den Staudruck mit Profilbeiwert und Referenzwert des Staudrucks.
    
    Parameter:
    ----------
    c_h : float; 
        Der Profilbeiwert.
        
    q_p0 : float; 
        Die Referenzwert des Staudrucks. 
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 261:2014 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Der Wind Staudruck
    
    Hinweise:
    -----
     Gemäss SIA 261:2014, Abschnitt 6.2.1.1, wird der Wind Staudruck bestimmt:
  
    Beispiele:
    --------
    >>> wind_staudruck_SIA261_11(1.02, 0.9*kN/m**2)
    0.92*kN/m**2
    
    >>> wind_staudruck_SIA261_11(1.7, 1.3*kN/m**2)
    2.21*kN/m**2
    """

    if background == True:
        display(Markdown("""
*SIA 261:2014 Abschnitt 6.2.1.1 (11)*

Der Staudruck $q_p$ hängt vom Windklima, der Bodenrauigkeit, der Form der Erdoberfläche und der Bezugshöhe ab. Er wird wie folgt bestimmt: 
$$ q_p = c_h \\cdot q_{p0} $$
        """))
        
    return c_h * q_p0

def wind_profilbeiwert_SIA261_12(z:float, z_g:float, alpha_r:float, plot=False, background=False):
    """
    Berechnung des Profilbeiwerts gemäss SIA 261:2014, Abschnitt 6.2.1.2\\
    Diese Funktion berechnet den Profilbeiwert.
    
    Parameter:
    ----------
    z : float; 
        Höhe über Bodenoberfläche. Eingabe in m **dimensionslos!**
        
    z_g : float; 
        Die Gradientenhöhe. Eingabe in m **dimensionslos!**

    alpha_r : float;
        Die Bodenrauigkeit.

    plot : bool, optional;
        Wenn True, wird die Figur aus SIA 261:2014 angezeigt mit entsprechendem Wert. Standard ist False.
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 261:2014 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Der Profilbeiwert.
    
    Hinweise:
    -----
    Gemäss SIA 261:2014, Abschnitt 6.2.1.2, wird der Profilbeiwert bestimmt:
  
    Beispiele:
    --------
    >>> wind_profilbeiwert_SIA261_12(10 , 526 , 0.3)
    0.74
    
    >>> wind_profilbeiwert_SIA261_12(50 , 450 , 0.23)
    1.53*kN/m**2
    """

    def get_c_h(z, z_g, alpha_r):
        if alpha_r == 0.3 and z < 10:
            z = 10
        elif alpha_r == 0.3 and z > 30:
            z_g = 450
            alpha_r = 0.23
        elif z < 5:
            z = 5
        return 1.6 * ((z / z_g) ** alpha_r + 0.375)**2

    if plot == True:
        z_plot = arange(0, 100, 0.1)

        fig, fig_6 = plt.subplots(figsize=(3,3))
        

        c_h_II = []
        c_h_IIa = []
        c_h_III = []
        c_h_IV = []
        for zi in z_plot:
            c_h_II.append(get_c_h(zi, 300, 0.16))
            c_h_IIa.append(get_c_h(zi, 380, 0.19))
            c_h_III.append(get_c_h(zi, 450, 0.23))
            c_h_IV.append(get_c_h(zi, 526, 0.3))

        fig_6.plot(get_c_h(z, z_g, alpha_r), z, 'o', color='#C80032', label='Wert', markersize=5)
        fig_6.plot(c_h_II, z_plot, color='k', linestyle='solid', linewidth = 1, label='II')
        fig_6.plot(c_h_IIa, z_plot, color='k', linestyle='dotted', linewidth = 1, label='IIa')
        fig_6.plot(c_h_III, z_plot, color='k', linestyle='dashed', linewidth = 1, label='III')
        fig_6.plot(c_h_IV, z_plot, color='k', linestyle='dashdot', linewidth = 1, label='IV')        

        fig_6.set_xlabel("$c_h$")
        fig_6.set_ylabel("$z$ in [m]")
        fig_6.grid(True)
        fig_6.legend()
        fig_6.set_ylim([0, 100])
        fig_6.set_xlim([0, 2.5])


    if background == True:
        display(Markdown("""
*SIA 261:2014 Abschnitt 6.2.1.2 (12)*

Der Profilbeiwert $c_h$ berücksichtigt das Windgeschwindigkeitsprofil in Funktion der Höhe $z$ über dem Boden sowie die durch Bebauung und Bewuchs erzeugte Bodenrauigkeit. Er wird wie folgt bestimmt:
$$ c_h = 1.6 \\left[ \\left(\\frac{z}{z_g}\\right)^{\\alpha_r} + 0.375 \\right]^2 $$
        """))

    return get_c_h(z, z_g, alpha_r)