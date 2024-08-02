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
        print("NPK A wurde noch nicht definiert")
    elif NPK == "B":
        print("NPK B wurde noch nicht definiert")
    elif NPK == "C":
        print("NPK C wurde noch nicht definiert")
    elif NPK == "D":
        print("NPK D wurde noch nicht definiert")
    elif NPK == "E":
        print("NPK E wurde noch nicht definiert")
    elif NPK == "F":
        print("NPK F wurde noch nicht definiert")
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
        print("NPK H wurde noch nicht definiert")
    elif NPK == "I":
        print("NPK I wurde noch nicht definiert")
    elif NPK == "K":
        print("NPK K wurde noch nicht definiert")
    elif NPK == "L":
        print("NPK L wurde noch nicht definiert")
    else:
        raise ValueError('Betonsorte nicht erkannt. Inputmöglichkeiten: "A", "B", "C", "D", "E", "F", "G", "H", "I", "K", "L"')