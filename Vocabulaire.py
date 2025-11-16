from parameters import *
import json


def get_liste(show:bool=False):
    #renvoi:list[tuple[str,str]]=[]
    liste:dict[str,list[str]]=json.load(open(path_file_list))[listechoisie]
    res:dict[str,dict[str,int]]={}
    for cle in liste.keys():
        res[cle]={"apparu":0,"réussi":0,"raté":0}
        if show:
            nv=liste[cle][0]
            for i in range(1,len(liste[cle])):
                nv+=", "+liste[cle][i]
            print(f"{cle} : {nv}")
    return liste,res


def devinette(nbpoints:int,nbessais:int,suite:int,demande:str):
    essai=input(demande+"\n").strip()
    if essai=="exit":
        return nbpoints,nbessais,suite
    elif essai in tableau[demande]:
        resultats[demande]["réussi"]+=1
        nbpoints+=1
        suite+=1
        print(f"Vous avez {nbpoints} points sur {nbessais+1} ce qui vous fait un taux de {(nbpoints/(nbessais+1))*100} % de réussite !")
        texterajoute={True:"",False:". Vous pouviez répondre "+repr(tableau[demande][0])+"".join(", ou "+repr(tableau[demande][i]) for i in range(1,len(tableau[demande])))}
        print(f"Bravo ! La réponse était effectivement {essai} {texterajoute[len(tableau[demande])==1]}")
        if suite>=3:
            print(f"Incroyable ! Vous êtes sur une série de {suite} bonnes réponses")
    else:
        resultats[demande]["raté"]+=1
        suite=0
        print(f"Vous avez {nbpoints} points sur {nbessais+1} ce qui vous fait un taux de {(nbpoints/(nbessais+1))*100} % de réussite !")
        if len(tableau[demande])==0:
            print(f"La réponse était {tableau[demande][0]}")
        else:
            print(f"Vous pouviez répondre {repr(tableau[demande][0])}{"".join(", ou "+repr(tableau[demande][i]) for i in range(1,len(tableau[demande])))}")
        rectification=""
        while rectification not in tableau[demande]:
            rectification=input(f"Essayez de réécrire { {True:"la réponse",False:"une des réponses"}[len(tableau[demande])==1] } :\n")
    resultats[demande]["apparu"]+=1
    nbessais+=1
    return nbpoints,nbessais,suite
def analyse_résultats():
    apparus,reussis,rates=maxium(resultats,5)
    print("############################################################")
    print("####################   LES TOPS   ##########################")
    print("############################################################")
    for i in range(len(apparus)):
        print(f"Le mot {apparus[i]} est apparu {resultats[apparus[i]]["apparu"]} fois.")
    print()
    for i in range(len(reussis)):
        print(f"Le mot{ reussis[i]} a été réussi {resultats[reussis[i]]["réussi"]} fois.")
    print()
    for i in range(len(rates)):
        print(f"Le mot {rates[i]} a été râté {resultats[rates[i]]["raté"]} fois.")
def maxium(tableau:dict[str,dict[str,int]],tops:int):
    return (sorted(tableau,reverse=True,key=lambda dict:tableau[dict][categorie])[:tops] for categorie in ["apparu","réussi","raté"])
def newboucle():
    points=0
    essais=0
    suite=0
    suivant=True
    if len(tableau)==0:
        print("Aucun élément à apprendre")
        return
    while suivant:
        demande=getdemande(resultats,essais)
        precessais=essais
        points,essais,suite=devinette(points,essais,suite,demande)
        if precessais==essais:
            analyse_résultats()
            inpsuiv=""
            while inpsuiv.lower()!="oui" and inpsuiv.lower()!="non":
                inpsuiv=str(input("Voulez-vous continuer le quiz ? (oui ou non)\n"))
            if inpsuiv.lower()=="non":
                suivant=False
def add_nouveaux():
    try:
        tableau:dict[str,dict[str,list[str]]]=json.load(open(path_file_list,encoding="utf-8"))
    except (json.decoder.JSONDecodeError,FileNotFoundError):
        tableau:dict[str,dict[str,list[str]]]={}
    with open("./nouveaux.txt",encoding="utf-8") as f:
        content:list[str]=f.read().splitlines()
    if len(content)==0:
        if tableau.get(listechoisie)==None:
            tableau[listechoisie]={}
            json.dump(tableau,open(path_file_list,"w",encoding="utf-8"))
        return
    for i in range(len(content)):
        demande,reponse=content[i].split("=")
        if tableau.get(listechoisie)==None:
            tableau[listechoisie]={}
        tabrep:list[str]=[]
        i=0
        while i<len(reponse):
            if reponse[i]==",":
                if reponse[i-1]!="\\":
                    tabrep.append(reponse[:i])
                    reponse=reponse[i+1:]
                    i=0
                else:
                    reponse=reponse[:i-1]+reponse[i:]
            else:
                i+=1
        tabrep.append(reponse)
        tableau[listechoisie][demande.strip()]=[val.strip() for val in tabrep]
    with open("./nouveaux.txt","w",encoding="utf-8") as f:
        f.write("")
    json.dump(tableau,open(path_file_list,"w",encoding="utf-8"))
def print_currents():
    for cle,val in tableau.items():
        aff=cle+"="
        for i in range(len(val)):
            for j in range(len(val[i])):
                if val[i][j]=="," and val[i][j-1]!="\\":
                    val[i]=val[i][:j]+"\\"+val[i][j:]
            if i!=0:
                aff+=", "
            aff+=val[i]
        print(aff)




add_nouveaux()
tableau,resultats=get_liste()
print_currents()

newboucle()
