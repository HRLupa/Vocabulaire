import random
def randomized(tableau:dict[str,dict[str,int]],nbessais:int):
    return random.choice(list(tableau.keys())) 
def inorder(tableau:dict[str,dict[str,int]],nbessais:int):
    return tuple(tableau.keys())[nbessais%len(tableau)]
def floors(tableau:dict[str,dict[str,int]],nbessais:int)->str:
    selected:list[str]=[tuple(tableau.keys())[0]]
    for cle,val in tableau.items():
        if val["réussi"]<tableau[selected[0]]["réussi"]:
            selected=[cle]
        elif val["réussi"]==tableau[selected[0]]["réussi"]:
            selected.append(cle)
    return random.choice(selected)