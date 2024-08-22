from IPython.display import Markdown, display 
from numpy import sqrt, pi, tan, arctan, cos, arccos, sin, arcsin
from engicalc.units import ureg, kg, t, mm, cm, dm, m, km, N, kN, MN, rad, deg, percent, s, MPa, los

def Schneelast_charakteristisch_SIA261_9(mu_i:float, C_e:=1.0, C_T:float, s_k:float, background=False):
    """
    Berechnung der charakteristischen Schneelast gemäss SIA 262:2013, Abschnitt 5.2.2\\
    Diese Funktion berechnet die charakteristische Schneelast basierend auf der der Dachformbeiwerte, Windexposition und dem thermischen Beiwert.
    
    Parameter:
    ----------
    mu_i : float; 
        Die Kriechzahl.
        
    C_e : float; 
        Die Windexposition des Bauwerks. 
        Gemäss 5.2.4: 
        normale Exposition: 1.0
        dem Wind stark ausgesetzte Lage: 0.8
        vor Wind geschützter Lage: 1.2

    C_T : float; 
        Die thermische Beiwert.

    s_k : float; 
        Schneelast auf horizontalem Gelände.
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Die Kriechdehnung des Betons.
    
    Hinweise:
    -----
    Gemäss SIA 261:2014, Abschnitt 5.2.2, wird die charakteristische Schneelast basierend auf der der Dachformbeiwerte, Windexposition und dem thermischen Beiwert bestimmt:
  

    Beispiele:
    --------
    >>> kriechdehnung_SIA262_12(1.5, 0.002)
    0.003
    
    >>> kriechdehnung_SIA262_12(2.0, 0.0025)
    0.005
    """

    if background == True:
        display(Markdown("""
*SIA 261:2014 Abschnitt 5.2.2 (9)*

Der charakteristische Wert der Schneelast auf Dächern, bezogen auf die überdeckte Grundrissfläche, beträgt:
$$ q_k = \\mu_i \\cdot C_e \\cdot C_T \\cdot s_k $$
        """))
        
    return mu_i * C_e * C_T * s_k