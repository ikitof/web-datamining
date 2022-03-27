import re
import rdflib
from rdflib import Graph, Literal, URIRef 
from rdflib.plugins.sparql import prepareQuery
from JSONLD import *
import math
from tkinter import *


API_URL = "https://opendata.hauts-de-seine.fr/api/records/1.0/search/?dataset=gares-et-stations-du-reseau-ferre-dile-de-france-par-ligne&q=&rows=258&facet=id_ref_lda&facet=mode&facet=idrefliga&facet=ligne&refine.mode=RER"
context = r'./context.json'
gare_JSONLD = JSONLD(context,API_URL)


#création graph
graph = Graph()
graph.parse(data=gare_JSONLD,format="json-ld")
prefix = "PREFIX pref:<https://unnom.com/ontology#>"
prefix1 = "PREFIX foaf :<http://xmlns.com/foaf/0.1/#>"
print(graph.serialize())






#region querys

#première query
def query_1() :
    rep = graph.query(prefix +'''select distinct ?type
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:type ?type . 
    }''')
    l = ""
    for type, *_ in rep:
        l += str(type.value) + "\n"
    return l

#seconde query
def query_2(choice) :
    rep = graph.query(prefix +'''select ?nom
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:type "'''+ choice + '''" .
    ?c pref:station ?nom .
    }''')
    l =""
    for nom, *_ in rep:
        l += str(nom.value) + "\n"
    return l


#troisième query
def query_3(choice) :
    rep = graph.query(prefix +'''select ?type
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:station "'''+choice+'''" .
    ?c pref:type ?type .
    }''')
    l = ""
    for nom, *_ in rep:
        l+=str(nom.value) + "\n"
    return l

#quatrième query
def query_4() :
    rep = graph.query(prefix +'''select ?nom (count(?type) >= 2 as ?tot)
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:station ?nom .
    ?c pref:type ?type .
    }
    group by ?nom
    ''')
    l = ""
    for nom,ligne, *_ in rep :
        if ligne.value : 
            l+=str(nom.value) + "\n"
    return l


#cinquième query
def query_5():
    rep = graph.query(prefix +'''select ?nom 
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:station ?nom .
    filter regex(?nom,"^C.*", "g")
    }
    ''')
    l = ""
    for nom, *_ in rep :
        l+=str(nom.value) + "\n"
    return l

#sixième query
def query_6():
    rep = graph.query(prefix +'''
    select distinct ?nom (((?lat -2.347013e+00)*(?lat -2.347013e+00) + (?long -4.886182e+01)*(?long -4.886182e+01)) as ?sum)
    where {
    ?a  pref:gare ?b . 
    ?b pref:fields ?c .
    ?c pref:station ?nom .
    ?c pref:geo_point_2d ?lat .
    ?c pref:geo_point_2d ?long .
    }
    order by ?sum 
    offset 1
    limit 4
    ''')
    l=""
    for type,sum, *_ in rep:
        l+=str(type.value) + "\n"
    return l
#endregion

#region affichage_graph
"""
for index,(sub,pred,obj) in enumerate(graph) : 
    print(sub,pred,obj)

print(f'graph has {len(graph)} facts')

for index,(sub,pred,obj) in enumerate(graph) : 
    print(sub,pred,obj)
"""
#endregion

#region UI
def sel():
    choix = listbox.get(ANCHOR)
    #window.destroy()
    if choix == "Séléctionne toutes les lignes de RER distincte" :
        query1 = Tk()
        query1.title("première query")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Séléctionne toutes les lignes de RER distincte")
        label_res = Label(query1,text=query_1())
        label_pres.pack()
        label_res.pack()
        button_retour = Button(query1, text = "retour",command= retour(query1))
        button_retour.pack()
        query1.mainloop()
    elif choix == "Affichage des stations sur chaque ligne" :
        query1 = Tk()
        query1.title("Affichage des stations sur chaque ligne")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Choissisez la ligne dont vous voulez voir les stations")
        label_pres.pack()
        choice = Listbox(query1)
        choice.insert(0,"RER A")
        choice.insert(1,"RER B")
        choice.insert(2,"RER C")
        choice.insert(3,"RER D")
        choice.insert(4,"RER E")
        choice.pack()
        button_choisir = Button(query1,text= "selectionner",command = lambda:aff_2(choice,query1))
        button_choisir.pack()
        
        button_retour = Button(query1, text = "retour",command=retour(query1))
        button_retour.pack()
        query1.mainloop()
    elif choix == "Affichage des lignes disponible dans les stations" :
        query1 = Tk()
        query1.title("Affichage des lignes disponible dans les stations")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Choissisez la station dont vous voulez voir les lignes")
        label_pres.pack()
        choice = Listbox(query1)
        choice.insert(0,"Louvres")
        choice.insert(1,"Châtelet-Les Halles")
        choice.insert(2,"Massy-Palaiseau")
        choice.insert(3,"Gare du Nord")
        choice.insert(4,"Bourg-la-Reine")
        choice.insert(5,"Antony")
        choice.insert(6,"Noisiel")
        choice.pack()
        button_choisir = Button(query1,text= "selectionner",command = lambda:aff_3(choice,query1))
        button_choisir.pack()
        
        button_retour = Button(query1, text = "retour",command=retour(query1))
        button_retour.pack()
        query1.mainloop()
    elif choix == "Affichage des stations qui sont desservie par plusieurs ligne" :
        query1 = Tk()
        query1.title("Affichage des stations qui sont desservie par plusieurs ligne")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Affiche toutes les stations qui sont desservie par plusieurs ligne")
        label_res = Label(query1,text=query_4())
        label_pres.pack()
        label_res.pack()
        button_retour = Button(query1, text = "retour",command= retour(query1))
        button_retour.pack()
        query1.mainloop()
    elif choix == "Affichage de toute les stations qui commence par C":
        query1 = Tk()
        query1.title("Affichage de toute les stations qui commence par C")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Affiche toutes les stations qui commencent par la lettre C")
        label_res = Label(query1,text=query_5())
        label_pres.pack()
        label_res.pack()
        button_retour = Button(query1, text = "retour",command= retour(query1))
        button_retour.pack()
        query1.mainloop()
    else :
        query1 = Tk()
        query1.title("Affiche les stations les plus proches de Châtelet les halles")
        query1.geometry("500x500")
        query1.minsize(500,500)
        label_pres = Label(query1, text="Affiche les stations les plus proches de Châtelet les halles")
        label_res = Label(query1,text=query_6())
        label_pres.pack()
        label_res.pack()
        button_retour = Button(query1, text = "retour",command= retour(query1))
        button_retour.pack()
        query1.mainloop()

def aff_2(x,query1) :
    affic = x.get(ANCHOR)
    scrollbar = Scrollbar(query1)
    scrollbar.pack( side = RIGHT, fill = Y )
    listbox_res = Listbox(query1,yscrollcommand = scrollbar.set)
    res = query_2(affic)
    for z in res.split("\n") :
        listbox_res.insert(END,z)
    listbox_res.pack()

def aff_3(x,query1):
    affic = x.get(ANCHOR)
    label_res = Label(query1,text=query_3(affic))
    label_res.pack()
    

def retour(x):
    return lambda : x.destroy()


    
#créer la fenetre
window = Tk()
#personalisation
window.title("menue principal")
window.geometry("500x500")
window.minsize(500,500)

#contenue
label_title = Label(window, text="Quel query voulez vous séléctionnez ?")
label_title.pack()
listbox = Listbox(window,width = 60)
listbox.insert(0,"Séléctionne toutes les lignes de RER distincte")
listbox.insert(1,"Affichage des stations sur chaque ligne")
listbox.insert(2,"Affichage des lignes disponible dans les stations")
listbox.insert(3,"Affichage des stations qui sont desservie par plusieurs ligne")
listbox.insert(4,"Affichage de toute les stations qui commence par C")
listbox.insert(5,"Affiche les stations les plus proches de Châtelet les halles")
listbox.pack(pady=15)
button1 = Button(window, text="Selection",command = sel)
button1.pack()
button2 = Button(window,text="quit",command=window.destroy)
button2.pack()
#affichage
window.mainloop()
#endregion


