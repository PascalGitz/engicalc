from IPython.display import Markdown, display 

def kriechdehnung_SIA262_12(psi, epsilon_c_el, background=False):
    """
    psi = Kriechzahl
    epsilon_c_el = elastische Dehnung

    """
    if background == True:
        display(Markdown("""
*SIA 262:2013 Ziff 3.1.2.6.1*

Die Dehnung infolge Kriechens des Betons wird aus den elastischen Dehnungen mithilfe der Kriechzahl bestimmt:
$$ \\varepsilon_{cc}(t) = \\varphi(t, t_0) \\varepsilon_{c,el} $$                         
                         """))
        
    return psi*epsilon_c_el