from IPython.display import Markdown, display 
from numpy import sqrt, pi, tan, arctan, cos, arccos, sin, arcsin
from engicalc.units import ureg, kg, t, mm, cm, dm, m, km, N, kN, MN, rad, deg, percent, s, MPa, los

def schneelast_charakteristisch_SIA261_9(mu_i:float, C_e:float, C_T:float, s_k:float, background=False):
    """
    Berechnung der charakteristischen Schneelast gemäss SIA 262:2013, Abschnitt 5.2.2\\
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
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
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
    Berechnung der charakteristischen Schneelast auf horizontalem Gelände gemäss SIA 262:2013, Abschnitt 5.2.6\\
    Diese Funktion berechnet die charakteristische Schneelast basierend auf der Bezugshöhe h_0 in m.
    
    Parameter:
    ----------
    h_0 : float; 
        Die Bezugshöhe. Eingabe in m **dimensionslos!**
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
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