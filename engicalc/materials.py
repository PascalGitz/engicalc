from engicalc.units import ureg, kg, t, mm, cm, dm, m, km, N, kN, MN, rad, deg, percent, s, MPa, los
# from engicalc.output import dict_to_markdown_table
from IPython.display import display, Markdown


class Material:
    def __init__(self, name: str, dichte: float):
        self.txt_name = name
        self.rho = dichte

    def get_properties(self):
        return vars(self)
    
    # def _repr_markdown_(self):
    #     return dict_to_markdown_table(self.get_properties())
        


class Beton(Material):
    def __init__(self, NPK: str):
        beton_data = self.Betonsorte(NPK)
        super().__init__(name=beton_data["Name"][0], dichte=2500*kg/m**3)
        self.txt_Druckfestigkeitsklasse = beton_data["Druckfestigkeitsklasse"][0]
        self.txt_Expositionsklassen = beton_data["Expositionsklassen"]
        self.D_max = beton_data["Nennwert Grösstkorn D_max"]
        self.C_l = beton_data["Klasse des Chloridgehalts Cl"]
        self.txt_Konsistenzklasse = beton_data["Konsistenzklasse"][0]
        self.txt_Frost_txt_Tausalz_txt_Widerstand = beton_data["Frost-Tausalz-Widerstand"]
        self.f_ck = beton_data["f_ck"]
        self.f_ctm = beton_data["f_ctm"]

    @staticmethod
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
        >>> Beton("G")
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
    def __str__(self):
        return f"Beton: {self.txt_name} ({self.txt_Druckfestigkeitsklasse})"



class Stahl(Material):
    def __init__(self, Stahlqualität: str):
        stahl_data = self.Stahlsorte(Stahlqualität)
        super().__init__(name=stahl_data["Name"][0], dichte=7850*kg/m**3)
        self.f_yk = stahl_data["f_yk"]
        self.tau_yk = stahl_data["tau_yk"]
        self.f_uk = stahl_data["f_uk"]
        self.Blechstärke = stahl_data["Blechstärke"]



    @staticmethod
    def Stahlsorte(Stahlqualität:str):
        """
        Diese Funktion gibt alle relevanten Stahlparameter aus.
        SIA 263:2013
        
        Parameter:
        ----------
        Stahlqualität : string
        Blechstärke : to be defined
                
        Rückgabe:
        -------
        Dictionary
            Alle Angaben zum Stahl.
        
        Hinweise:
        -----
        Stahlsorten nach SIA 263:2013
        Festigkeiten gemäss SIA 263(2013) 3.2.2.3
    

        Beispiele:
        --------  
        >>> Stahl("S355")
        {'Name': ('S235',), 'f_yk': 355, 'tau_yk': 205, 'f_uk': 510, 'Blechstärke': 't<40mm'}
        """

        if Stahlqualität == "S235":
            S235 = {
                "Name": ("S 235",),
                "f_yk": 235*N/mm**2,
                "tau_yk": 135*N/mm**2,
                "f_uk": 360*N/mm**2,
                "Blechstärke": "t<40mm"
             }
            return S235
        elif Stahlqualität == "S355":
            S355 = {
                "Name": ("S 355",),
                "f_yk": 355*N/mm**2,
                "tau_yk": 205*N/mm**2,
                "f_uk": 510*N/mm**2,
                "Blechstärke": "t<40mm"
            }
            return S355
        else:
            raise ValueError('Stahlsorte nicht erkannt. Inputmöglichkeiten: "S235", "S355"')    
    def __str__(self):
        return f"Stahl: {self.txt_name}\\,(\\,für\\,{self.Blechstärke})"