from IPython.display import Markdown, display 
from numpy import sqrt

def as_min_Rechteck(b:float, h:float, d:float, fcd:float, fctd:float, fsd:float, background=False):
    """
    Berechnung der Mindestbewehrung für das Rechteck.\\
    Die Bedingung ist: Mrd < MRd: M-Riss < M-Widerstandsmoment
        
    Parameter:
    ----------
    b : float
        Breite des Querschnitts
        
    h : float
        Höhe des Querschnitts
    
    d : float
        Statische Höhe des Querschnitts (Oberkante Druckzone bis Achse Bewehrung Zugseite)
        
    fcd : float
        Druckfestigkeit des Betons auf Design Niveau
    
    fctd : float
        Zugfestigkeit des Betons auf Design Niveau
    
    fsd : float
        Zugfestigkeit des Betonstahls auf Design Niveau
        
    background : bool, optional
        Wenn True, wird die entsprechende Formel angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Die Mindestbewehrung für den Querschnitt.
    
    Hinweise:
    -----
    keine
  

    Beispiele:
    --------
    >>> As_min_Rechteck(1000*mm, 300*mm, 239*mm, 20*N/mm**2, 2.5*N/mm**2, 435*N/mm**2)
    366.82*mm**2

    >>> As_min_Rechteck(300*mm, 500*mm, 421*mm, 20*N/mm**2, 2.5*N/mm**2, 435*N/mm**2)
    173.22*mm**2
    """

    if background == True:
        display(Markdown("""
Die Mindestbewehrung für den Rechteckquerschnitt beträgt auf Grundlage der Bedingung Mrd < MRd:
$$ A_{s,\\text{min}} = \\frac{b \cdot f_{cd}}{f_{sd}} \cdot \left(d - \sqrt{\\frac{3d^2 \cdot f_{cd} - f_{ctd} \cdot h^2}{3 \cdot f_{cd}}}\\right) $$
        """))
        
    return b*fcd/fsd * (d - sqrt((3*d**2 * fcd - fctd*h**2) / (3*fcd)))

def betondruckfestigkeit_design_SIA262_2(fck:float, gamma_c:float, eta_fc=1.0, eta_t=1.0, background=False):
    """
    Berechnung der Betondruckfestigkeit gemäss SIA 262:2013, Abschnitt 2.3.2.3\\
    Diese Funktion berechnet die Betondruckfestigkeit auf design Niveau auf Grund der charakteristischen Betondruckfestigkeit, der Umrechnungsfaktoren und des Partialsicherheitfaktor.
    
    Parameter:
    ----------
    fck : float; 
        charakteristischer Wert der Zylinderdruckfestigkeit (5%-Fraktilwert)

    gamma_c : float;
        Widerstandsbeiwert für Beton
        
    eta_fc : float, optional; 
        Umrechnungsfaktor zur Berücksichtigung des spröderen Bruchverhaltens von Beton höherer Festigkeit. Standard ist 1.0

    eta_t : float, optional;
        Umrechnungsfaktor für Betonfestigkeiten zur Berücksichtigung von Einwirkungsdauer und Betonalter. Standard ist 1.0
        
    background : bool, optional;
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Betondruckfestigkeit auf design Niveau.
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 2.3.2.3, wird die Betondruckfestigkeit auf design Niveau auf Grund der charakteristischen Betondruckfestigkeit, der Umrechnungsfaktoren und des Partialsicherheitfaktor.
  

    Beispiele:
    --------
    >>> betondruckfestigkeit_design_SIA262_2(30*N/mm**2, 1.5, background=True)
    20 *N/mm**2
    """

    if background == True:
        display(Markdown("""
*SIA 262:2013 Abschnitt 2.3.2.3*

Der Bemessungswert der Betondruckfestigkeit beträgt: 
$$ f_{cd} = \\frac{\eta_{fc} \eta_t f_{ck}}{\gamma_c}  $$
        """))
        
    return eta_fc * eta_t * fck / gamma_c

def fliessgrenze_design_SIA262_4(fsk:float, gamma_s:float, background=False):
    """
    Berechnung der Fliessgrenze gemäss SIA 262:2013, Abschnitt 2.3.2.5\\
    Diese Funktion berechnet die Fliessgrenze auf design Niveau auf Grund des charakteristischen Werts der Fliessgrenze von Betonstahl und des Partialsicherheitsfaktors.
    
    Parameter:
    ----------
    fsk : float; 
        charakteristischer Wert der Fliessgrenze von Betonstahl
        
    gamma_s : float;
        Widerstandsbeiwert für Betonstahl und Spannstahl
        
    background : bool, optional;
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Fliessgrenze Betonstahl auf design Niveau.
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 2.3.2.5, wird die Fliessgrenze auf design Niveau auf Grund des charakteristischen Werts der Fliessgrenze von Betonstahl und des Partialsicherheitsfaktors.
  

    Beispiele:
    --------
    >>> fliessgrenze_design_SIA262_4(500*N/mm**2, 1.15, background=True)
    435 *N/mm**2
    """

    if background == True:
        display(Markdown("""
*SIA 262:2013 Abschnitt 2.3.2.5*

Der Bemessungswert der Fliessgrenze des Betonstahls beträgt: 
$$ f_{sd} = \\frac{f_{sk}}{\gamma_s}  $$
        """))
        
    return fsk / gamma_s

def betonzugfestigkeit_95Fraktil_SIA262_8(fctm:float, background=False):
    """
    Berechnung der Fliessgrenze gemäss SIA 262:2013, Abschnitt 3.1.2.2.5\\
    Diese Funktion berechnet den 95% Fraktilwert der Betonzugfestigkeit charakteristisch auf Basis der mittleren Betonzugfestigkeit.
    
    Parameter:
    ----------
    fctm : float
        Mittlere Betonzugfestigkeit
        
    background : bool, optional;
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        95% Fraktilwert der Betonzugfestigkeit charakteristisch
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 3.1.2.2.5, wird der 95% Fraktilwert der Betonzugfestigkeit charakteristisch auf Basis der mittleren Betonzugfestigkeit berechnet.
  

    Beispiele:
    --------
    >>> betonzugfestigkeit_95Fraktil_SIA262_8(2.9 *N/mm**2)
    3.77 *N/mm**2
    """

    if background == True:
        display(Markdown("""
*SIA 262:2013 Abschnitt 3.1.2.2.5*

Der 95% Fraktilwert der Betonzugfestigkeit charakteristisch beträgt: 
$$ f_{ctk 0,95} = 1.3 f_{ctm}  $$
        """))
        
    return 1.3*fctm

def kriechdehnung_SIA262_12(psi:float, epsilon_c_el:float, background=False):
    """
    Berechnung der Kriechdehnung des Betons gemäss SIA 262:2013, Abschnitt 3.1.2.6.1.\\
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
*SIA 262:2013 Abschnitt 3.1.2.6.1*

Die Dehnung infolge Kriechens des Betons wird aus den elastischen Dehnungen mithilfe der Kriechzahl bestimmt:
$$ \\varepsilon_{cc}(t) = \\varphi(t, t_0) \\varepsilon_{c,el} $$
        """))
        
    return psi * epsilon_c_el

def betonzugfestigkeit_design_SIA262_98(fctm:float, kt:float, background=False):
    """
    Berechnung der Betonzugfestigkeit gemäss SIA 262:2013, Abschnitt 4.4.1.3\\
    Diese Funktion berechnet die Betonzugfestigkeit auf design Niveau auf Grund des Mittelwerts der Betonzugfestigkeits und des Abminderungsfaktors k_t
    
    Parameter:
    ----------
    fctm : float
        Mittlere Betonzugfestigkeit
        
    kt : float
        Abminderungsfaktor
        
    background : bool, optional
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Betonzugfestigkeit auf design Niveau.
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 4.4.1.3, wird die Betonzugfestigkeit auf design Niveau auf Grund des Mittelwerts der Betonzugfestigkeits und des Abminderungsfaktors k_t
  

    Beispiele:
    --------
    >>> betonzugfestigkeit_design_SIA262_98(2.9*N/mm**2, 0.87)
    2.52 *N/mm**2
    
    >>> betonzugfestigkeit_design_SIA262_98(2.2*N/mm**2, 0.87)
    2.09 *N/mm**2
    """

    if background == True:
        display(Markdown("""
*SIA 262:2013 Abschnitt 4.4.1.3*

Der Bemessungswert der Betonzugfestigkeit beträgt: 
$$ f_{ctd} = k_t \cdot f_{ctm}  $$
        """))
        
    return fctm * kt

def abminderungsfaktor_kt_SIA262_99(t:float , biegebeanspruchung:bool , background=False):
    """
    Berechnung der Kriechdehnung des Betons gemäss SIA 262:2013, Abschnitt 3.1.2.6.1.\\
    Diese Funktion berechnet die Kriechdehnung basierend auf der elastischen Dehnung und der Kriechzahl.
    
    Parameter:
    ----------
    t : float; 
        Abmessung in m. Eingabe **dimensionslos!**

    biegebeanspruchung : bool; 
        Wenn True, wird t = h/3 berechnet; Wenn False, wird t direkt weiterverwendet
        
    background : bool, optional; 
        Wenn True, wird die entsprechende Formel aus SIA 262:2013 angezeigt. Standard ist False.
    
    Rückgabe:
    -------
    float
        Abminderungsfaktor k_t
    
    Hinweise:
    -----
    Gemäss SIA 262:2013, Abschnitt 4.4.1.3, wird der Abminderungsfaktor k_t zur Berücksichtigung der Abmessung bestimmt:
  

    Beispiele:
    --------
    >>> abminderungsfaktor_kt_SIA262_99(0.3, False)
    0.87
    
    >>> abminderungsfaktor_kt_SIA262_99(0.3, True)
    0.95
    """

    if biegebeanspruchung == False:
        if background == True:
            display(Markdown("""
*SIA 262:2013 Abschnitt 4.4.1.3*

Gemäss SIA 262:2013, Abschnitt 4.4.1.3, wird der Abminderungsfaktor k_t zur Berücksichtigung der Abmessung bestimmt:
$$ k_t = \\frac{1}{1+0.5*t} $$
            """))
            
        return 1 / (1 + 0.5*t)
    
    elif biegebeanspruchung == True:
        if background == True:
            display(Markdown("""
*SIA 262:2013 Abschnitt 4.4.1.3*

Gemäss SIA 262:2013, Abschnitt 4.4.1.3, wird der Abminderungsfaktor k_t zur Berücksichtigung der Abmessung bestimmt:\\
Massgebend ist die jeweils kleinste Abmessung des betrachteten Zuggurts. Für Platten- und Rechteckquerschnitte unter Biegebeanspruchung gilt t = h/3. 
$$ t = \\frac{h}{3} $$
$$ k_t = \\frac{1}{1+0.5*t} $$
            """))
            
        return 1 / (1 + 0.5*(t/3))