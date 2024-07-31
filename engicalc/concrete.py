from IPython.display import Markdown, display 

def kriechdehnung_SIA262_12(psi, epsilon_c_el, background=False):
    """
    Berechnung der Kriechdehnung des Betons gemäss SIA 262:2013, Abschnitt 3.1.2.6.1.
    Diese Funktion berechnet die Kriechdehnung basierend auf der elastischen Dehnung und der Kriechzahl.
    
    Parameter:
    ----------
    psi : float
        Die Kriechzahl.
        
    epsilon_c_el : float
        Die elastische Dehnung des Betons.
        
    background : bool, optional
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Die Kriechdehnung des Betons.
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 3.1.2.6.1, wird die Kriechdehnung des Betons aus den elastischen Dehnungen mithilfe der Kriechzahl bestimmt:
  

    Beispiele:
    --------
    >>> kriechdehnung_SIA262_12(1.5, 0.002)
    0.003
    
    >>> kriechdehnung_SIA262_12(2.0, 0.0025)
    0.005
    """

    if background == True:
        display(Markdown("""
**SIA 262:2013 Abschnitt 3.1.2.6.1**

Die Dehnung infolge Kriechens des Betons wird aus den elastischen Dehnungen mithilfe der Kriechzahl bestimmt:
$$ \\varepsilon_{cc}(t) = \\varphi(t, t_0) \\varepsilon_{c,el} $$
        """))
        
    return psi * epsilon_c_el
