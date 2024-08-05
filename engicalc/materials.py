from engicalc.units import ureg, kg, t, mm, cm, dm, m, km, N, kN, MN, rad, deg, percent, s, MPa, los

def Betonsorte(NPK:str):
    """
    Diese Funktion gibt alle relevanten Betonparameter aufgrund des NPK's aus.
    NPK-Betone (NPK-Betonsorten), SN EN 206 (2014), NA (2016)
    
    Parameter:
    ----------
    NPK : string
            
    Rückgabe:
    -------
    Dictionary
        Alle Angaben zum Beton.
    
    Hinweise:
    -----
    NPK-Betone (NPK-Betonsorten), SN EN 206 (2014), NA (2016)
    Festigkeiten gemäss SIA 262(2003) 3.1.2.2.7
  

    Beispiele:
    --------  
    >>> kriechdehnung_SIA262_12("G")
    {'Name': ('NPK G',), 'Druckfestigkeitsklasse': ('C30/37',), 'Expositionsklassen': ('XC4', 'XD3', 'XF4'), 'Nennwert Grösstkorn D_max': (32,), 'Klasse des Chloridgehalts Cl': (0.1,), 'Konsistenzklasse': ('C3',), 'Frost-Tausalz-Widerstand': ('hoch',), 'f_ck': 30}
    """

    if NPK == "A":
        NPK_A = {
            "Name": ("NPK A",),
            "Druckfestigkeitsklasse": ("C20/25",),
            "Expositionsklassen": ("XC2",),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": None,
            "f_ck": 20*N/mm**2,
            "f_ctm": 2.2*N/mm**2
        }
        return NPK_A
    elif NPK == "B":
        NPK_B = {
            "Name": ("NPK B",),
            "Druckfestigkeitsklasse": ("C25/30",),
            "Expositionsklassen": ("XC3",),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": None,
            "f_ck": 25*N/mm**2,
            "f_ctm": 2.6*N/mm**2
        }
        return NPK_B
    elif NPK == "C":
        NPK_C = {
            "Name": ("NPK C",),
            "Druckfestigkeitsklasse": ("C30/37",),
            "Expositionsklassen": ("XC4", "XF1"),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": None,
            "f_ck": 30*N/mm**2,
            "f_ctm": 2.9*N/mm**2
        }
        return NPK_C
    elif NPK == "D":
        NPK_D = {
            "Name": ("NPK D",),
            "Druckfestigkeitsklasse": ("C25/30",),
            "Expositionsklassen": ("XC4", "XD1", "XF2"),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": "mittel",
            "f_ck": 25*N/mm**2,
            "f_ctm": 2.6*N/mm**2
        }
        return NPK_D
    elif NPK == "E":
        NPK_E = {
            "Name": ("NPK E",),
            "Druckfestigkeitsklasse": ("C25/30",),
            "Expositionsklassen": ("XC4", "XD1", "XF4"),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": "hoch",
            "f_ck": 25*N/mm**2,
            "f_ctm": 2.6*N/mm**2
        }
        return NPK_E
    elif NPK == "F":
        NPK_F = {
            "Name": ("NPK F",),
            "Druckfestigkeitsklasse": ("C30/37",),
            "Expositionsklassen": ("XC4", "XD3", "XF2"),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": "mittel",
            "f_ck": 30*N/mm**2,
            "f_ctm": 2.9*N/mm**2
        }
        return NPK_F
    elif NPK == "G":
        NPK_G = {
            "Name": ("NPK G",),
            "Druckfestigkeitsklasse": ("C30/37",),
            "Expositionsklassen": ("XC4", "XD3", "XF4"),
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("C3",),
            "Frost-Tausalz-Widerstand": ("hoch",),
            "f_ck": 30*N/mm**2,
            "f_ctm": 2.9*N/mm**2
        }
        return NPK_G
    elif NPK == "H":
        NPK_H = {
            "Name": ("NPK H",),
            "Druckfestigkeitsklasse": ("C25/30",),
            "Expositionsklassen": None,
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("F4",),
            "Frost-Tausalz-Widerstand": "kein oder mittel",
            "f_ck": 25*N/mm**2,
            "f_ctm": 2.6*N/mm**2
        }
        return NPK_H
    elif NPK == "I":
        NPK_I = {
            "Name": ("NPK I",),
            "Druckfestigkeitsklasse": ("C25/30",),
            "Expositionsklassen": None,
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("F5",),
            "Frost-Tausalz-Widerstand": "kein oder mittel",
            "f_ck": 25*N/mm**2,
            "f_ctm": 2.6*N/mm**2
        }
        return NPK_I
    elif NPK == "K":
        NPK_K = {
            "Name": ("NPK K",),
            "Druckfestigkeitsklasse": ("C20/25",),
            "Expositionsklassen": None,
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("F4",),
            "Frost-Tausalz-Widerstand": None,
            "f_ck": 20*N/mm**2,
            "f_ctm": 2.2*N/mm**2
        }
        return NPK_K
    elif NPK == "L":
        NPK_L = {
            "Name": ("NPK L",),
            "Druckfestigkeitsklasse": ("C20/25",),
            "Expositionsklassen": None,
            "Nennwert Grösstkorn D_max": 32*mm,
            "Klasse des Chloridgehalts Cl": 0.10,
            "Konsistenzklasse": ("F5",),
            "Frost-Tausalz-Widerstand": None,
            "f_ck": 20*N/mm**2,
            "f_ctm": 2.2*N/mm**2
        }
        return NPK_L
    else:
        raise ValueError('Betonsorte nicht erkannt. Inputmöglichkeiten: "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L"')