import sqlite3
from tkinter import*

#creation de la fenetre
window=Tk()
window.title("Généa-logique !")
window.config(width=1200, height=600)


#creation du canevas de la partie superieur
canevas_up = Canvas(window, width=1200, height=600)
canevas_up.place(x=0, y=0)

#creation du cannevas de la partie inferieur
canevas_down=Canvas(window,width=1200,height=600,bg="#AEFF00")
canevas_down.place(x=0,y=430)

#importation de toute les images
fond=PhotoImage(file="fond_sql_python.gif")
valider_off=PhotoImage(file="bouton_off.png")
valider_on=PhotoImage(file="bouton_on.png")
retour_on=PhotoImage(file="retour_on.png")
retour_off=PhotoImage(file="retour_off.png")
arbre=PhotoImage(file="arbre_left_join.png")
feuille=PhotoImage(file="feuille.png")
feuille_clique=PhotoImage(file="feuille_clique.png")
logo=PhotoImage(file="logo_genealogique.png")
save=PhotoImage(file="save.png")
help_save=PhotoImage(file="help.png")


#creation des images
img_retour_off=canevas_down.create_image(32,15, image=retour_off)
canevas_down.delete(img_retour_off)
img_retour_off=canevas_down.create_image(5000,15, image=retour_off)
img_help_save=canevas_down.create_image(10200,65, image=help_save)
canevas_down.delete(img_help_save)
canevas_up.create_image(600,300, image=fond)
arbre_arbre=canevas_up.create_image(850,250, image=arbre)
img_logo=canevas_up.create_image(200,85,image=logo)
img_valider_off=canevas_down.create_image(5000,32, image=valider_off)


#liste avec les position x et y des feuilles correspondante
position_valide=[[830, 361],[648, 216],[1012, 226],[731, 95],[568,97],[1096, 97],[917, 95]]


class Feuille:
    """class feuille permettant avec les deux argument de changer une feuille en fonction de son id_personne
    mais aussi grace a l'indice des postion des feuilles enregistrer dans la variable position_valide """
    def __init__(self,id_personne,indice):
        self.position_x=position_valide[indice][0]
        self.position_y=position_valide[indice][1]
        self.feuille=canevas_up.create_image(self.position_x,self.position_y,image=feuille)
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        print(id_personne)
        curseur.execute("select Personne.nom,Personne.prenom from Personne where Personne.id_personne='"+str(id_personne)+"'")
        self.nom_prenom=curseur.fetchone()
        connexion.commit()
        connexion.close()
        if self.nom_prenom == None:
            self.txt_nom_prenom=canevas_up.create_text(self.position_x,self.position_y,text="Inconnue",fill="yellow",font="Arial 10",justify="center") 
        else:
            self.txt_nom_prenom=canevas_up.create_text(self.position_x,self.position_y,text=self.nom_prenom[0]+"\n"+self.nom_prenom[1],fill="yellow",font="Arial 10",justify="center")
    def detruire(self):
        """Fonction permettant de detruire le contenue de la feuille"""
        canevas_up.coords(self.txt_nom_prenom,5000,100)
        canevas_up.coords(self.feuille,5000,100)
    def clique(self,position_x,position_y):
        """La fonction clique permets de verifier que l'on ce trouve dans les bonnes coordonéées lorsque que l'on clique sur l'une des 3 feuilles
        mais aussi d'effectuer les recherche dont l'ont a besoin dont la base de donnée """
        
        
        #fonction identique a celle presente plus bas (verification_identite) 
        global liste_feuille
        if self.position_x-66.5<position_x<self.position_x+66.5 and self.position_y-16.5<position_y<self.position_y+16.5 and self.nom_prenom != None:
            for i in range (len(liste_feuille)):
                liste_feuille[i].detruire()
            liste_feuille=[]
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("select Personne.id_personne from Personne where personne.nom='"+self.nom_prenom[0]+"' and Personne.prenom='"+self.nom_prenom[1]+"'")
            id_personne_recherchee = curseur.fetchall() 

            script_blaze="""SELECT Enfant.nom,Enfant.prenom,Pere.nom,Pere.prenom,Mere.nom,Mere.Prenom FROM Personne AS Enfant JOIN Personne AS 
            Pere ON Enfant.id_pere=Pere.id_personne JOIN Personne AS Mere ON Enfant.id_mere=Mere.id_personne where Enfant.nom=? and Enfant.prenom=? """
            curseur.execute(script_blaze,(self.nom_prenom[0],self.nom_prenom[1]))
            information_personne_famille=curseur.fetchall()
            script_dinfo_naissance="""select Deces.date,lieu_deces.adresse,lieu_deces.ville,Naissance.date,lieu_naissance.adresse,lieu_naissance.ville
            from Naissance
            left join Personne
            on Personne.id_naissance=Naissance.id_naissance
            left join Deces
            on Personne.id_deces=Deces.id_deces
            left join Lieu as lieu_deces
            on Deces.id_lieu=lieu_deces.id_lieu 
            left join lieu as lieu_naissance
            on Naissance.id_lieu=lieu_naissance.id_lieu
            where Personne.nom=? and Personne.prenom=?
            """
            curseur.execute(script_dinfo_naissance,(self.nom_prenom[0],self.nom_prenom[1]))
            information_personne_naissance=curseur.fetchall()
            indo_pers=(self.nom_prenom[0],self.nom_prenom[1])
            script_blaze="""SELECT Enfant.nom,Enfant.prenom,Pere.nom,Pere.prenom,Mere.nom,Mere.Prenom FROM Personne AS Enfant left JOIN Personne AS 
            Pere ON Enfant.id_pere=Pere.id_personne left JOIN Personne AS Mere ON Enfant.id_mere=Mere.id_personne where Enfant.nom=? and Enfant.prenom=? """
            curseur.execute(script_blaze,indo_pers)
            k=0
            h=0
            tout_prenom_nom = curseur.fetchall()
            script_info_deces_naissance="""select Deces.date,lieu_deces.adresse,lieu_deces.ville,Naissance.date,lieu_naissance.adresse,lieu_naissance.ville
            from Naissance
            left join Personne
            on Personne.id_naissance=Naissance.id_naissance
            left join Deces
            on Personne.id_deces=Deces.id_deces
            left join Lieu as lieu_deces
            on Deces.id_lieu=lieu_deces.id_lieu 
            left join lieu as lieu_naissance
            on Naissance.id_lieu=lieu_naissance.id_lieu
            where Personne.nom=? and Personne.prenom=?
            """
            curseur.execute(script_info_deces_naissance,indo_pers)
            
            info_deces_naissance=curseur.fetchall()
            script_id_personne="""SELECT Enfant.id_personne,Mere.id_personne,Pere.id_personne,Mere_mere.id_personne,Mere_pere.id_personne,Pere_mere.id_personne,Pere_pere.id_personne
            FROM Personne
            AS Enfant
            left JOIN Personne
            AS Pere 
            ON Enfant.id_pere=Pere.id_personne 
            left JOIN Personne 
            AS Mere
            ON Enfant.id_mere=Mere.id_personne
            left join Personne
            as Mere_mere
            on Mere.id_mere=Mere_mere.id_personne
            left join Personne
            as Mere_pere
            on Mere.id_pere=Mere_pere.id_personne
            left join Personne
            as Pere_mere
            on Pere.id_mere=Pere_mere.id_personne
            left join Personne
            as Pere_pere
            on Pere.id_pere=Pere_pere.id_personne
            where Enfant.nom=? and Enfant.prenom=?"""
            curseur.execute(script_id_personne,indo_pers)
            info_feuille=curseur.fetchall()
            print(info_feuille)
            for p in range (7):
                """modification de la feuille"""
                liste_feuille.append(Feuille(info_feuille[0][p],p))

            if id_personne_recherchee == []:
                    entree_modify_conjoint.insert(0,"Inconnue") 
                    entree_modify_conjointe.insert(0,"Inconnue")
            else:
                entree_modify_conjoint.delete(0,END)                
                entree_modify_conjointe.delete(0,END)
                entree_modify_date_mariage.delete(0,END)
                entree_modify_adresse_mariage.delete(0,END)  
                entree_modify_ville_mariage.delete(0,END)

                script_mariage_info='''SELECT Mariage.id_epoux, Mariage.id_epouse, Mariage.Date, Mariage.id_lieu
                FROM Mariage
                WHERE Mariage.id_epouse = ''' + str(id_personne_recherchee[0][0]) + ''' OR Mariage.id_epoux = ''' + str(id_personne_recherchee[0][0])
                curseur.execute(script_mariage_info)
                mariage_info = curseur.fetchall()
                print(mariage_info)

                if mariage_info == [] :
                    entree_modify_conjointe.place_forget()
                    entree_modify_conjoint.place_forget()
                    entree_modify_date_mariage.place_forget()
                    entree_modify_adresse_mariage.place_forget()
                    entree_modify_ville_mariage.place_forget()
                    txt_modify_mariage_date.place_forget()
                    txt_modify_mariage_ville.place_forget()
                    txt_modify_mariage_adresse.place_forget()
                    txt_modify_conjointe.place_forget()
                    txt_modify_conjoint.place_forget()


                elif mariage_info == None:
                    entree_modify_conjointe.place_forget()
                    entree_modify_conjoint.place_forget()
                    entree_modify_date_mariage.place_forget()
                    entree_modify_adresse_mariage.place_forget()
                    entree_modify_ville_mariage.place_forget()
                    txt_modify_mariage_date.place_forget()
                    txt_modify_mariage_ville.place_forget()
                    txt_modify_mariage_adresse.place_forget()
                    txt_modify_conjointe.place_forget()
                    txt_modify_conjoint.place_forget()
                else:


                    script_id_epoux_epouse="""select epoux.prenom,epouse.prenom
                    from Personne
                    as epoux
                    left join Mariage
                    on epoux.id_personne=Mariage.id_epoux
                    left join Personne
                    as epouse
                    on epouse.id_personne=Mariage.id_epouse
                    where id_epouse="""+str(mariage_info[0][1])+""" and id_epoux="""+str(mariage_info[0][0])+""" """
                    curseur.execute(script_id_epoux_epouse)
                    nom_prenom_epoux_epouse=curseur.fetchall()
                    script_adresse_mariage="""select lieu.adresse,lieu.ville
                    from lieu
                    join Mariage
                    on Mariage.id_lieu= lieu.id_lieu
                    where Mariage.id_lieu="""+str(mariage_info[0][3])+""" """
                    curseur.execute(script_adresse_mariage)
                    adresse_mariage_ville_adresse=curseur.fetchall()

                    print(nom_prenom_epoux_epouse)
                    entree_modify_conjoint.insert(0,nom_prenom_epoux_epouse[0][0])
                    entree_modify_conjointe.insert(0,nom_prenom_epoux_epouse[0][1])
                    entree_modify_date_mariage.insert(0,mariage_info[0][2])
                    entree_modify_adresse_mariage.insert(0,adresse_mariage_ville_adresse[0][0])
                    entree_modify_ville_mariage.insert(0,adresse_mariage_ville_adresse[0][1])

                    txt_modify_conjoint.config(text= "Prénom du conjoint :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
                    txt_modify_conjointe.config(text= "Prénom de la conjointe :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
                    txt_modify_mariage_date.config(text= "Date du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
                    txt_modify_mariage_ville.config(text= "Ville du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
                    txt_modify_mariage_adresse.config(text= "Adresse du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))

                    entree_modify_conjoint.place(x=780,y=15)                    
                    entree_modify_conjointe.place(x=780,y=45)
                    entree_modify_date_mariage.place(x=780,y=75)
                    entree_modify_adresse_mariage.place(x=780,y=105)  
                    entree_modify_ville_mariage.place(x=780,y=135)
                    txt_modify_conjoint.place(x=620,y=15)
                    txt_modify_conjointe.place(x=600,y=42)
                    txt_modify_mariage_date.place(x=640,y=70)
                    txt_modify_mariage_adresse.place(x=620,y=100)
                    txt_modify_mariage_ville.place(x=640,y=131)
            existe_pas = False
            for i in tout_prenom_nom:
                    
                if(i[1].upper() == self.nom_prenom[1].upper() and i[0].upper() == self.nom_prenom[0].upper()):
                    modify_nom.delete(0,END)
                    modify_prenom.delete(0,END)
                    modify_naissance_date.delete(0,END)
                    modify_naissance_ville.delete(0,END)
                    modify_prenom_pere.delete(0,END)
                    modify_prenom_mere.delete(0,END)
                    modify_deces_date.delete(0,END)
                    modify_deces_ville.delete(0,END)
                    modify_deces_adresse.delete(0,END)
                    modify_naissance_adresse.delete(0,END)
                    existe_pas = True
                    if tout_prenom_nom[k][0] == None:

                        modify_nom.insert(0,"Inconnue")
                    else:

                        modify_nom.insert(0,tout_prenom_nom[k][0])

                    if tout_prenom_nom[k][1] == None:

                        modify_prenom.insert(0,"Inconnue")
                    else:
                        modify_prenom.insert(0,tout_prenom_nom[k][1])

                    if info_deces_naissance == []:
                        modify_naissance_date.insert(0,"Inconnue") 

                    elif info_deces_naissance[h][3] == None:
                            
                        modify_naissance_date.insert(0,"Inconnue") 
                    else: 

                        modify_naissance_date.insert(0,info_deces_naissance[h][3])
                    if info_deces_naissance == []:

                        modify_naissance_adresse.insert(0,"Inconnue") 

                    elif info_deces_naissance[h][4] == None:

                        modify_naissance_adresse.insert(0,"Inconnue")  
                    else:

                        modify_naissance_adresse.insert(0,info_deces_naissance[h][4])

                    if info_deces_naissance == []:

                        modify_naissance_ville.insert(0,"Inconnue") 

                    elif info_deces_naissance[h][5] == None:

                        modify_naissance_ville.insert(0,"Inconnue")  
                    else:

                        modify_naissance_ville.insert(0,info_deces_naissance[h][5])

                    if tout_prenom_nom[h][3] == None:

                        modify_prenom_pere.insert(0,"Inconnue")

                    else:

                        modify_prenom_pere.insert(0,tout_prenom_nom[h][3])
                

                    if tout_prenom_nom[h][5] == None:

                        modify_prenom_mere.insert(0,"Inconnue")
                        
                    else:
                        modify_prenom_mere.insert(0,tout_prenom_nom[h][5])

                   
                        


                    modify_prenom_mere.place(x=200,y=140)
                    modify_prenom_pere.place(x=200,y=115)
                    modify_naissance_ville.place(x=200,y=90)
                    modify_naissance_date.place(x=200,y=65)
                    modify_prenom.place(x=200,y=40)
                    modify_nom.place(x=200,y=15)                                        
                    modify_deces_date.place(x=470,y=15)               
                    modify_deces_ville.place(x=470,y=40)                   
                    modify_deces_adresse.place(x=470,y=65)
                    modify_naissance_adresse.place(x=470,y=90)

                    
                    if info_deces_naissance==[]:
                        modify_deces_date.insert(0,"Inconnue")
        
                        modify_deces_ville.insert(0,"Inconnue")   

                        modify_deces_adresse.insert(0,"Inconnue")


                    elif info_deces_naissance[h][0] == "0" or info_deces_naissance[h][2]=="0" or info_deces_naissance[h][1]=="0":
                        modify_deces_date.insert(0,"Inconnue/Vivant")
                        modify_deces_ville.insert(0,"Inconnue/Vivant")
                        modify_deces_adresse.insert(0,"Inconnue/Vivant")
                    else:
                        modify_deces_date.insert(0,info_deces_naissance[h][0])
        
                        modify_deces_ville.insert(0,info_deces_naissance[h][2])   

                        modify_deces_adresse.insert(0,info_deces_naissance[h][1])
            connexion.commit()
            connexion.close()
    def onclick(self,position_x,position_y):
        """onclick comme son nom l'indique nous permets de changer l'apparence de la feuille lorsque qu'on passe notre curseur dessus"""
        
        if self.position_x-66.5<position_x<self.position_x+66.5 and self.position_y-16.5<position_y<self.position_y+16.5:
            canevas_up.itemconfig(self.feuille,image=feuille_clique)
        else: 
            canevas_up.itemconfig(self.feuille,image=feuille)
        canevas_up.coords(self.position_x,self.position_y,self.txt_nom_prenom)




def deplacement_valider(event):
    global numero_menu
    """
        Fonction liée au déplacement de la souris,
        vérifie si le curseur et bien aux coordonée rentrer
    """
    # Vérifie si le curseur est sur le bouton img_valider 
    if(event.x >= 208 and event.y >= 23 and event.x <= 292 and event.y <= 40):
        canevas_down.itemconfig(img_valider_off, image = valider_on)
    else:
        canevas_down.itemconfig(img_valider_off, image = valider_off)
    if(event.x >= 0 and event.y >= 6 and event.x <= 70 and event.y <= 22):
        canevas_down.itemconfig(img_retour_off, image = retour_on)
    else:
        canevas_down.itemconfig(img_retour_off, image = retour_off)
    if(event.x >= 949 and event.y >= 79 and event.x <= 974 and event.y <= 101) and numero_menu==1:
        canevas_down.itemconfig(img_help_save, image = help_save)

def deplacement_valider_up(event):

    """
        Fonction liée au déplacement de la souris,
        vérifie si le curseur et bien aux coordonée rentrer
    """
    # Vérifie si le curseur est sur le bouton img_valider 
    if(event.x >= 208 and event.y >= 23 and event.x <= 292 and event.y <= 40):
        canevas_down.itemconfig(img_valider_off, image = valider_on)
    else:
        canevas_down.itemconfig(img_valider_off, image = valider_off)
    if(event.x >= 0 and event.y >= 6 and event.x <= 70 and event.y <= 22):
        canevas_down.itemconfig(img_retour_off, image = retour_on)
    else:
        canevas_down.itemconfig(img_retour_off, image = retour_off)



    if len(liste_feuille) != 0:
        for i in range(len(liste_feuille)):
            liste_feuille[i].onclick(event.x,event.y)

#creation de toute les entry utiliser 
entre_recherche_prenom = Entry(canevas_down,width = 15)
entre_recherche_prenom.config(bg="#58EC99",fg='red')

entre_recherche_nom = Entry(canevas_down,width = 15)
entre_recherche_nom.config(bg="#58EC99",fg='red')

entre_insert_nom = Entry(canevas_down,width = 15)
entre_insert_nom.config(bg="#58EC99",fg='red')

entre_insert_prenom = Entry(canevas_down,width = 15)
entre_insert_prenom.config(bg="#58EC99",fg='red')

entre_insert_naissance_date = Entry(canevas_down,width = 15)
entre_insert_naissance_date.config(bg="#58EC99",fg='red')

entre_insert_naissance_adresse = Entry(canevas_down,width = 15)
entre_insert_naissance_adresse.config(bg="#58EC99",fg='red')

entre_insert_naissance_ville = Entry(canevas_down,width = 15)
entre_insert_naissance_ville.config(bg="#58EC99",fg='red')

entre_insert_lieu_adresse = Entry(canevas_down,width = 15)
entre_insert_lieu_adresse.config(bg="#58EC99",fg='red')

entre_insert_lieu_ville = Entry(canevas_down,width = 15)
entre_insert_lieu_ville.config(bg="#58EC99",fg='red')

entre_insert_deces_date = Entry(canevas_down,width = 15)
entre_insert_deces_date.config(bg="#58EC99",fg='red')

entre_insert_deces_adresse = Entry(canevas_down,width = 15)
entre_insert_deces_adresse.config(bg="#58EC99",fg='red')

entre_insert_deces_ville = Entry(canevas_down,width = 15)
entre_insert_deces_ville.config(bg="#58EC99",fg='red')


entre_insert_pere_nom = Entry(canevas_down,width = 15)
entre_insert_pere_nom.config(bg="#58EC99",fg='red')

entre_insert_pere_prenom = Entry(canevas_down,width = 15)
entre_insert_pere_prenom.config(bg="#58EC99",fg='red')

entre_insert_mere_nom = Entry(canevas_down,width = 15)
entre_insert_mere_nom.config(bg="#58EC99",fg='red')

entre_insert_mere_prenom = Entry(canevas_down,width = 15)
entre_insert_mere_prenom.config(bg="#58EC99",fg='red')

modify_prenom=Entry(canevas_down,width=15)
modify_prenom.config(bg="#58EC99",fg='red')

modify_nom=Entry(canevas_down,width=15)
modify_nom.config(bg="#58EC99",fg='red')

modify_naissance_date=Entry(canevas_down,width=15)
modify_naissance_date.config(bg="#58EC99",fg='red')

modify_naissance_ville=Entry(canevas_down,width=15)
modify_naissance_ville.config(bg="#58EC99",fg='red')


modify_naissance_adresse=Entry(canevas_down,width=15)
modify_naissance_adresse.config(bg="#58EC99",fg='red')


modify_deces_date=Entry(canevas_down,width=15)
modify_deces_date.config(bg="#58EC99",fg='red')

modify_deces_ville=Entry(canevas_down,width=15)
modify_deces_ville.config(bg="#58EC99",fg='red')


modify_deces_adresse=Entry(canevas_down,width=15)
modify_deces_adresse.config(bg="#58EC99",fg='red')


modify_prenom_pere=Entry(canevas_down,width=15)
modify_prenom_pere.config(bg="#58EC99",fg='red')

modify_prenom_mere=Entry(canevas_down,width=15)
modify_prenom_mere.config(bg="#58EC99",fg='red')


entree_conjoint_nom=Entry(canevas_down, width=15)
entree_conjoint_nom.config(bg="#58EC99",fg='red')


entree_conjoint_prenom=Entry(canevas_down, width=15)
entree_conjoint_prenom.config(bg="#58EC99",fg='red')

entree_conjointe_nom=Entry(canevas_down, width=15)
entree_conjointe_nom.config(bg="#58EC99",fg='red')

entree_conjointe_prenom=Entry(canevas_down, width=15)
entree_conjointe_prenom.config(bg="#58EC99",fg='red')

entree_date_mariage=Entry(canevas_down, width=15)
entree_date_mariage.config(bg="#58EC99",fg='red')

entree_ville_mariage=Entry(canevas_down, width=15)
entree_ville_mariage.config(bg="#58EC99",fg='red')

entree_adresse_mariage=Entry(canevas_down, width=15)
entree_adresse_mariage.config(bg="#58EC99",fg='red')

entree_modify_date_mariage=Entry(canevas_down, width=15)
entree_modify_date_mariage.config(bg="#58EC99",fg='red')

entree_modify_adresse_mariage=Entry(canevas_down, width=15)
entree_modify_adresse_mariage.config(bg="#58EC99",fg='red')

entree_modify_ville_mariage=Entry(canevas_down, width=15)
entree_modify_ville_mariage.config(bg="#58EC99",fg='red')

entree_modify_conjoint=Entry(canevas_down, width=15)
entree_modify_conjoint.config(bg="#58EC99",fg='red')

entree_modify_conjointe=Entry(canevas_down, width=15)
entree_modify_conjointe.config(bg="#58EC99",fg='red')

def deplacement_souris(event):
    #importation de toute les variable neccessaire pour la fonction
    global numero_menu
    """
        Fonction liée au déplacement de la souris,
        vérifie si le curseur et bien aux coordonée rentrer
    """
    # Vérifie si le curseur est sur le bouton img_valider 
    print(event.x,event.y)
    if(event.x >= 208 and event.y >= 23 and event.x <= 292 and event.y <= 40) and numero_menu == 1:
        verification_identite()

    if(event.x >= 0 and event.y >= 6 and event.x <= 70 and event.y <= 22) and numero_menu == 2:
        back_identite()



def deplacement_souris_up(event):
    #importation de toute les variable neccessaire pour la fonction
    global numero_menu
    """
    Fonction liée au déplacement de la souris,
    vérifie si le curseur et bien aux coordonée rentrer
    """
    # Vérifie si le curseur est sur le bouton img_valider 
    print(event.x,event.y)
    if(event.x >= 208 and event.y >= 23 and event.x <= 292 and event.y <= 40) and numero_menu == 1:
        verification_identite()

    if(event.x >= 0 and event.y >= 6 and event.x <= 70 and event.y <= 22) and numero_menu == 2:
        back_identite()

    if len(liste_feuille) != 0:
        for i in range(len(liste_feuille)):
            liste_feuille[i].clique(event.x,event.y)
 


def inseret_naissance():
    """insertion naissance permets d'inseret la date de naissance l'id de naissance , la ville de naissance et l'adresse
    pour cela on doit donc inseret des information dans la table lieu, naissance et personne 
    permets de verifier si la date de naissance et valide avec une notation de type xx/xx/xxxx"""
    #importation de toute les variable neccessaire pour la fonction
    global etape_insertion,info_personne
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    #verifie si la personne a bien remplie toute les entry
    if(entre_insert_naissance_date.get() == '' or entre_insert_naissance_ville.get()== '' or entre_insert_naissance_adresse ==''):
        texte_erreur.config(text = "Veuillez remplir les entrées.", font = ('', 15, ''))
        texte_erreur.place(x = 800, y = 60)
    else:
        verification = False
        #verifie si la date rentrer et bien valide de type xx/xx/xxxx
        if entre_insert_naissance_date.get()[2] == "/" == entre_insert_naissance_date.get()[5]:
            verification= True
    
        #verifie la personne existe si oui insert tout les information de naissance et de lieu sinon refuse pour date invalide
        if(verification == True):
            print(entre_insert_naissance_date.get())
            curseur.execute("INSERT INTO lieu(adresse,ville) VALUES('"+entre_insert_naissance_adresse.get()+"','"+entre_insert_naissance_ville.get()+"');")
            texte_erreur.config(text = "Les informations de naissances\n ont été ajouté !", font = ('', 15, ''))
            curseur.execute("SELECT id_lieu from Lieu where lieu.adresse='"+entre_insert_naissance_adresse.get()+"' and lieu.ville='"+entre_insert_naissance_ville.get()+"'")
            id_lieu=curseur.fetchall()
            curseur.execute("INSERT INTO Naissance(date,id_lieu) VALUES ('"+str(entre_insert_naissance_date.get())+"','"+str(id_lieu[0][0])+"');")
            curseur.execute("SELECT id_naissance from Naissance where Naissance.date='"+str(entre_insert_naissance_date.get())+"' and Naissance.id_lieu='"+str(id_lieu[0][0])+"'")
            id_naissance=curseur.fetchall()
            
            curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
            info_personne = curseur.fetchall()
            curseur.execute("UPDATE Personne set id_naissance='"+str(id_naissance[0][0])+"' where Personne.nom = '"+info_personne[len(info_personne)-1][0]+"' and Personne.prenom = '"+info_personne[len(info_personne)-1][1]+"'")
            
            DELETE_ALL()
            etape_insertion=3
            texte_erreur.place(x = 800, y = 60)
            entre_insert_naissance_date.delete(0, END)
            entre_insert_naissance_adresse.delete(0, END)
            entre_insert_naissance_ville.delete(0, END)
            etape_3bis.place(x=455,y=135)


        else:
            texte_erreur.config(text = "Cette date n'est \npas valide", font = ('', 15, ''))
            texte_erreur.place(x = 800, y = 60)



        connexion.commit()
        connexion.close()

def inseret_deces():
    '''Fonction qui permets d'inseret la date de déces, l'adresse decées et la ville déces et qui nous permets de voir
    si la personne est encore vivante en completant avec trois 0 dans les entry mais aussi que la date et valide avec la position
    des / dans la date'''
    #importation de toute les variable neccessaire pour la fonction
    global etape_insertion,info_personne,finir_pere,finir_mere
    nom_nul=2
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    verification = False
    #verifie si la date rentrer et bien valide de type xx/xx/xxxx
    if (len(entre_insert_deces_date.get())>=10):
        if(entre_insert_deces_date.get()[2] == "/" == entre_insert_deces_date.get()[5]):
            print(entre_insert_deces_date.get())
            curseur.execute("INSERT INTO lieu(adresse,ville) VALUES('"+entre_insert_deces_adresse.get()+"','"+entre_insert_deces_ville.get()+"');")
            texte_erreur.config(text ="Les informations de déces\n ont été ajouté !", font = ('', 15, ''))
            curseur.execute("SELECT id_lieu from Lieu where lieu.adresse='"+entre_insert_deces_adresse.get()+"' and lieu.ville='"+entre_insert_deces_ville.get()+"'")
            id_lieu=curseur.fetchall()
            curseur.execute("INSERT INTO Deces(date,id_lieu) VALUES ('"+str(entre_insert_deces_date.get())+"','"+str(id_lieu[0][0])+"');")
            texte_erreur.place(x = 800, y = 60)
            curseur.execute("SELECT id_deces from Deces where Deces.date='"+str(entre_insert_deces_date.get())+"' and Deces.id_lieu='"+str(id_lieu[0][0])+"'")
            id_deces=curseur.fetchall()
            curseur.execute("UPDATE Personne set id_deces='"+str(id_deces[0][0])+"' where Personne.nom = '"+info_personne[len(info_personne)-1][0]+"' and Personne.prenom = '"+info_personne[len(info_personne)-1][1]+"'")
            nom_nul=None
            etape_insertion=4
            DELETE_ALL()
            #verifie pour proposer de rentrer un nouveau pere/mere ou bien une personne
            if finir_pere == True:
                etape_insertion=5
                etape_5bis.place(x=455,y=135)
            elif finir_mere == True:
                etape_insertion=1
                etape_bon.place(x=455,y=135)
                etape_4bis.place(x=700,y=135)                         
            else:
                etape_4bis.place(x=455,y=135)
                    
                
                            
            texte_erreur.place(x = 800, y = 60)

    #condition qui laisse la posibiliter d'avoir une personne vivante             
    if(entre_insert_deces_date.get() == '0' or entre_insert_deces_adresse.get()== '0' or entre_insert_deces_date =='0'):
        curseur.execute("INSERT INTO lieu(adresse,ville) VALUES('"+entre_insert_deces_adresse.get()+"','"+entre_insert_deces_ville.get()+"');")
        curseur.execute("SELECT id_lieu from Lieu where lieu.adresse='"+entre_insert_deces_adresse.get()+"' and lieu.ville='"+entre_insert_deces_ville.get()+"'")
        id_lieu=curseur.fetchall()
        curseur.execute("INSERT INTO Deces(date,id_lieu) VALUES ('"+str(entre_insert_deces_date.get())+"','"+str(id_lieu[0][0])+"');")
        texte_erreur.config(text = "Cette personne est encore vivante\n elle est bien enregistré.", font = ('', 15, ''))
        curseur.execute("SELECT id_deces from Deces where Deces.date='"+str(entre_insert_deces_date.get())+"' and Deces.id_lieu='"+str(id_lieu[0][0])+"'")
        id_deces=curseur.fetchall()
        curseur.execute("UPDATE Personne set id_deces='"+str(id_deces[0][0])+"' where Personne.nom = '"+info_personne[len(info_personne)-1][0]+"' and Personne.prenom = '"+info_personne[len(info_personne)-1][1]+"'")
        nom_nul=None
        etape_insertion=4
        DELETE_ALL()
        if finir_pere == True:
            etape_insertion=5
            etape_5bis.place(x=455,y=135)
        elif finir_mere == True:
            etape_insertion=1
            etape_bon.place(x=455,y=135)
            etape_4bis.place(x=700,y=135)                         
        else:
            etape_4bis.place(x=455,y=135)
                
                            
        texte_erreur.place(x = 800, y = 60)

    
    
    #si date pas valide 
    elif (nom_nul!=None):
        texte_erreur.config(text = "Cette date n'est  \n pas valide", font = ('', 12, ''))
        texte_erreur.place(x = 800, y = 60)



    connexion.commit()
    connexion.close()
#creation de la verification du pere
finir_pere=False

def inseret_pere():
    """fonction inseret_pere qui permets d'inseret a une personne son pere
    verifie que la persone n'est pas déja presente dans la base de donnée
    et verifie si les entry sont vide ou non """
    #importation de toute les variable neccessaire pour la fonction
    global etape_insertion,info_personne,finir_pere  
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    #verifie que les entry sois bien completer
    if(entre_insert_nom.get() == '' or entre_insert_prenom.get() == ''):
        texte_erreur.config(text = "Veuillez remplir les entrées.", font = ('', 15, ''))
        texte_erreur.place(x = 800, y = 60)
    else:
        curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
        info_personne = curseur.fetchall()
        existe_deja = False
        for i in info_personne:
            #verifie que la personne n'est pas déja presente dans la base de donnée
            if(i[0].upper() == entre_insert_nom.get().upper()) and (i[1].upper()== entre_insert_prenom.get().upper()):
                existe_deja = True
        #si la personne n'est pas presente on insert son nom et prenom dans la base de donnée sinon on affiche le message d'erreur
        if(not existe_deja):
            recup_info= (entre_insert_nom.get(),entre_insert_prenom.get())
            curseur.execute("INSERT INTO Personne(nom,prenom) VALUES (?,?)",recup_info)
            texte_erreur.config(text = "La personne à été ajouté !", font = ('', 15, ''))
            connexion.commit()
            connexion.close()
            connexion = sqlite3.connect("Genealogie.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT id_Personne from Personne where Personne.nom='"+entre_insert_nom.get()+"' and Personne.prenom='"+entre_insert_prenom.get()+"'")
            id_pere = curseur.fetchall()
            print(id_pere)
            print(info_personne)
            curseur.execute("UPDATE Personne set id_pere='"+str(id_pere[0][0])+"' where Personne.nom = '"+info_personne[len(info_personne)-1][0]+"' and Personne.prenom = '"+info_personne[len(info_personne)-1][1]+"'")
            DELETE_ALL()
            texte_erreur.place(x = 800, y = 60)
            etape_insertion = 4
            etape_2bis.place(x=455,y=135)  
            finir_pere=True

        else:
            texte_erreur.config(text = "Cette personne est déja presente \ndans la base de donnée", font = ('', 12, ''))
            texte_erreur.place(x = 800, y = 60)


        connexion.commit()
        connexion.close()





def insertion_nom_prenom_du_mariage():
    """permets de liées deux personnes dans la table mariage 
    verifie si toute les entry sont remplie ou pas
    et verifie si elle est deja presente dans la base de donnée 
    """
    #importation de toute les variable neccessaire pour la fonction
    global etape_mariage,id_epouse,id_epoux
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()

    #on verifie que les entry sois bien rempli
    if(entree_conjoint_nom.get() == '' or entree_conjoint_prenom.get() == '' or entree_conjointe_nom.get() == '' or entree_conjointe_prenom.get() == ''):
        texte_erreur.config(text = "Veuillez remplir toute les entrées.", font = ('', 15, ''))
        texte_erreur.place(x = 800, y = 60)
    #si oui on on recherche tout les nom et prenom des personne dans la base de donnée
    else:
        curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
        info_personne = curseur.fetchall()
        existe_deja = False
        existe_deja_bis=False
        for i in info_personne:
            if(i[0].upper() == entree_conjointe_nom.get().upper()) and (i[1].upper()== entree_conjointe_prenom.get().upper()):
                existe_deja = True

            if (i[1].upper() == entree_conjoint_prenom.get().upper()) and (i[0].upper() == entree_conjoint_nom.get().upper()):
                existe_deja_bis=True

        #on verifie que le conjoint et la conjointe sont bien existant et si oui on les insert dans la table mariage
        if(existe_deja==True and existe_deja_bis==True):

            info_nom_prenom_conjointe=(entree_conjointe_prenom.get(),entree_conjointe_nom.get())
            info_nom_prenom_conjoint=(entree_conjoint_prenom.get(),entree_conjoint_nom.get())
            script_id_epoux="""select personne.id_personne
            from Personne
            where Personne.prenom=? and Personne.nom=?"""

            curseur.execute(script_id_epoux,info_nom_prenom_conjoint)
            id_epoux= curseur.fetchall()

            script_id_epouse="""select personne.id_personne
            from Personne
            where Personne.prenom=? and Personne.nom=?"""

            curseur.execute(script_id_epouse,info_nom_prenom_conjointe)
            id_epouse = curseur.fetchall()
            connexion.commit()
            connexion.close()
            print(id_epouse[0][0])
            print(id_epoux[0][0])
            connexion = sqlite3.connect("Genealogie.db")
            curseur = connexion.cursor()
            curseur.execute("insert into Mariage(id_epoux,id_epouse) values ('"+str(id_epoux[0][0])+"','"+str(id_epouse[0][0])+"')")
            connexion.commit()
            connexion.close()
            texte_erreur.config(text = "La personne à été ajouté !", font = ('', 15, ''))
            DELETE_ALL()
            etape_bis_1_mariage.place(x=455,y=135)
            texte_erreur.place(x = 800, y = 60)
            etape_mariage=2
        #si elle ne sont pas presente on affiche le message d'erreur
        else:
            texte_erreur.config(text = "Cette personne n'est pas presente \ndans la base de donnée", font = ('', 12, ''))
            texte_erreur.place(x = 800, y = 60)


        

def insertion_date_adresse_ville_mariage():
    """ permets d'inseret la ville et l'adresse dans la table lieux et la date de mariage dans la table mariage
    verifie que la date sois valide de type xx/xx/xxxx 
    la fonction n'inserre pas la date mais modifie la ligne de mariage déja presente avec les information déja presente(id_epoux,id_epouse)
    pour y ajouter la date de mariage"""

    #importation de toute les variable neccessaire pour la fonction
    global etape_mariage,id_epoux,id_epouse
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    nom_nul=2
    verification = False
    print(entree_date_mariage.get())
    #on verifie que la date rentrée et bien valide de type xx/xx/xxxx si oui on insert les information de mariage dans la table mariage et lieu
    #dans la table mariage la date et dans la table lieu l'adresse et la ville
    if (len(entree_date_mariage.get())>=10):
        if(entree_date_mariage.get()[2] == "/" == entree_date_mariage.get()[5]):
            print(entree_date_mariage.get())
            curseur.execute("INSERT INTO lieu(adresse,ville) VALUES('"+entree_adresse_mariage.get()+"','"+entree_ville_mariage.get()+"');")
            texte_erreur.config(text ="Les informations de mariages\n ont été ajouté !", font = ('', 15, ''))
            connexion.commit()
            connexion.close()
            connexion = sqlite3.connect("Genealogie.db")
            curseur = connexion.cursor()
            curseur.execute("SELECT id_lieu from Lieu where lieu.adresse='"+entree_adresse_mariage.get()+"' and lieu.ville='"+entree_ville_mariage.get()+"'")
            id_lieu=curseur.fetchall()
            curseur.execute("UPDATE mariage set date='"+entree_date_mariage.get()+"'where Mariage.id_epoux = '"+str(id_epoux[0][0])+"' and Mariage.id_epouse = '"+str(id_epouse[0][0])+"'")
            curseur.execute("UPDATE Mariage set id_lieu='"+str(id_lieu[0][0])+"' where Mariage.id_epoux = '"+str(id_epoux[0][0])+"' and Mariage.id_epouse = '"+str(id_epouse[0][0])+"'")
            connexion.commit()
            connexion.close()
            texte_erreur.place(x = 800, y = 60)
            nom_nul=None
            etape_mariage=1
            DELETE_ALL()                             
            texte_erreur.place(x = 800, y = 60)
            entree_conjoint_nom.place(x=230,y=50)
            entree_conjoint_prenom.place(x=230,y=140)
            entree_conjointe_nom.place(x=400,y=50)
            entree_conjointe_prenom.place(x=400,y=140)
            text_nom_pers.place(x=220,y=5)
            text_prenom_pers.place(x=210,y=90)
            texte_pere.place(x=380,y=90)
            texte_mere.place(x=390,y=5)
            bouton_nom_prenom_mariage.place(x=565,y=110)
            etape_bis_2_mariage.place()
    # si la date n'est pas valide on affiche le message d'erreur
    elif (nom_nul !=None):
        texte_erreur.config(text = "Cette date n'est  \n pas valide", font = ('', 12, ''))
        texte_erreur.place(x = 800, y = 60)








#creation de la verification de la mére 
finir_mere=False     

def inseret_mere():
    """fonction inseret_mere qui permets d'inseret a une personne sa mere
    verifie que la persone n'est pas déja presente dans la base de donnée
    et verifie si les entry sont vide ou non """
    #importation de toute les variable neccessaire pour la fonction
    global etape_insertion,info_personne,finir_mere,finir_pere
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    #verifie que les entry sois bien completer
    if(entre_insert_nom.get() == '' or entre_insert_prenom.get() == ''):
        texte_erreur.config(text = "Veuillez remplir les entrées.", font = ('', 15, ''))
        texte_erreur.place(x = 800, y = 60)
    else:
        curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
        info_personne = curseur.fetchall()
        existe_deja = False
        for i in info_personne:
            if(i[0].upper() == entre_insert_nom.get().upper()) and (i[1].upper()== entre_insert_prenom.get().upper()):
                existe_deja = True
        #si la personne n'est pas presente on insert son nom et prenom dans la base de donnée 
        if(not existe_deja):
            recup_info= (entre_insert_nom.get(),entre_insert_prenom.get())
            curseur.execute("INSERT INTO Personne(nom,prenom) VALUES (?,?)",recup_info)
            texte_erreur.config(text = "La personne à été ajouté !", font = ('', 15, ''))
            curseur.execute("SELECT id_Personne from Personne where Personne.nom='"+entre_insert_nom.get()+"' and Personne.prenom='"+entre_insert_prenom.get()+"'")
            id_mere = curseur.fetchall()
            curseur.execute("UPDATE Personne set id_mere='"+str(id_mere[0][0])+"' where Personne.nom = '"+info_personne[len(info_personne)-2][0]+"' and Personne.prenom = '"+info_personne[len(info_personne)-2][1]+"'")
            DELETE_ALL()
            texte_erreur.place(x = 800, y = 60)
            etape_insertion = 5
            etape_2bis.place(x=455,y=135)
            finir_mere=True 
            finir_pere=False
        #si la personne est déja presente dans la base de donnée on affiche le message d'erreur
        else:
            texte_erreur.config(text = "Cette personne est déja presente \ndans la base de donnée", font = ('', 12, ''))
            texte_erreur.place(x = 800, y = 60)


        connexion.commit()
        connexion.close()



def inseret_personne():
    """Permets d'inseret une personne qui n'est pas déja presente dans la base de donnée
    et verifie si les entry sont vide ou non"""
    #importation de toute les variable neccessaire pour la fonction
    global etape_insertion
    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
     #verifie que les entry sois bien completer
    if(entre_insert_nom.get() == '' or entre_insert_prenom.get() == ''):
        texte_erreur.config(text = "Veuillez remplir les entrées.", font = ('', 15, ''))
        texte_erreur.place(x = 800, y = 60)
    #on recherche dans la base de donnée tout les nom et prenom de la base de donnée
    else:
        curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
        info_personne = curseur.fetchall()
        existe_deja = False
        for i in info_personne:
            if(i[0].upper() == entre_insert_nom.get().upper()) and (i[1].upper()== entre_insert_prenom.get().upper()):
                existe_deja = True
        #si la personne n'existe pas on insert sont nom et prenom dans la base de donnée
        if(not existe_deja):
            recup_info= (entre_insert_nom.get(),entre_insert_prenom.get())
            curseur.execute("INSERT INTO Personne(nom,prenom) VALUES (?,?)",recup_info)
            texte_erreur.config(text = "La personne à été ajouté !", font = ('', 15, ''))
            DELETE_ALL()
            texte_erreur.place(x = 800, y = 60)
            etape_2bis.place(x=455,y=135)
            etape_insertion = 2 
        #si elle existe déja on affiche le message d'erreur
        else:
            texte_erreur.config(text = "Cette personne est déja presente \ndans la base de donnée", font = ('', 12, ''))
            texte_erreur.place(x = 800, y = 60)


        connexion.commit()
        connexion.close()



def verification_identite():
    """cette fonction permets de rechercher tout les information d'une personne 
    date de naissance,adresse,ville
    date de déces si il y'en a une 
    prenom des parents
    nom des epoux/epouse si il sont present avec la date de mariage,l'adresse et la ville"""
    #importation de toute les variable neccessaire pour la fonction
    global liste_tempo_affichage,numero_menu,id_epouse,id_epoux,id_personne_recherchee


    connexion = sqlite3.connect("Genealogie.db")
    curseur = connexion.cursor()
    #condition qui verifie que les entry sont completer
    if(entre_recherche_prenom.get() == '' or entre_recherche_nom.get() == ''):
        texte_erreur.config(text = "Veuillez rentrée un prénom et nom.", font = ('', 15, ''))
        texte_erreur.place(x = 625, y = 60)
        return

    indo_pers= (entre_recherche_nom.get(),entre_recherche_prenom.get())




    curseur.execute("select Personne.id_personne from Personne where personne.nom=? and Personne.prenom=?",indo_pers)
    id_personne_recherchee = curseur.fetchall() 

    


  


    script_blaze="""SELECT Enfant.nom,Enfant.prenom,Pere.nom,Pere.prenom,Mere.nom,Mere.Prenom FROM Personne AS Enfant left JOIN Personne AS 
    Pere ON Enfant.id_pere=Pere.id_personne left JOIN Personne AS Mere ON Enfant.id_mere=Mere.id_personne where Enfant.nom=? and Enfant.prenom=? """
    curseur.execute(script_blaze,indo_pers)
    k=0
    h=0
    tout_prenom_nom = curseur.fetchall()
    script_info_deces_naissance="""select Deces.date,lieu_deces.adresse,lieu_deces.ville,Naissance.date,lieu_naissance.adresse,lieu_naissance.ville
    from Naissance
    left join Personne
    on Personne.id_naissance=Naissance.id_naissance
    left join Deces
    on Personne.id_deces=Deces.id_deces
    left join Lieu as lieu_deces
    on Deces.id_lieu=lieu_deces.id_lieu 
    left join lieu as lieu_naissance
    on Naissance.id_lieu=lieu_naissance.id_lieu
    where Personne.nom=? and Personne.prenom=?
    """
    curseur.execute(script_info_deces_naissance,indo_pers)
    info_deces_naissance=curseur.fetchall()
    script_id_personne="""SELECT Enfant.id_personne,Mere.id_personne,Pere.id_personne,Mere_mere.id_personne,Mere_pere.id_personne,Pere_mere.id_personne,Pere_pere.id_personne
    FROM Personne
    AS Enfant
    left JOIN Personne
    AS Pere 
    ON Enfant.id_pere=Pere.id_personne 
    left JOIN Personne 
    AS Mere
    ON Enfant.id_mere=Mere.id_personne
    left join Personne
    as Mere_mere
    on Mere.id_mere=Mere_mere.id_personne
    left join Personne
    as Mere_pere
    on Mere.id_pere=Mere_pere.id_personne
    left join Personne
    as Pere_mere
    on Pere.id_mere=Pere_mere.id_personne
    left join Personne
    as Pere_pere
    on Pere.id_pere=Pere_pere.id_personne
    where Enfant.nom=? and Enfant.prenom=?"""
    curseur.execute(script_id_personne,indo_pers)
    info_feuille=curseur.fetchall()
    #condition qui verifie que la liste ne sois pas vide sinon recherche l'id de l'epoux/epouse
    if id_personne_recherchee == []:
        entree_modify_conjoint.insert(0,"Inconnue") 
        entree_modify_conjointe.insert(0,"Inconnue")
    else:
        script_mariage_info='''SELECT Mariage.id_epoux, Mariage.id_epouse, Mariage.Date, Mariage.id_lieu
        FROM Mariage
        WHERE Mariage.id_epouse = ''' + str(id_personne_recherchee[0][0]) + ''' OR Mariage.id_epoux = ''' + str(id_personne_recherchee[0][0])
        curseur.execute(script_mariage_info)
        mariage_info = curseur.fetchall()
        print(mariage_info)
        #condition qui verifie que la liste ne sois pas vide sinon affiche le nom,prenom de l'epoux/epouse et la date,adresse et ville de mariage
        if mariage_info == [] :
            entree_modify_conjoint.insert(0,"Inconnue") 
            entree_modify_conjointe.insert(0,"Inconnue")
            entree_modify_date_mariage.insert(0,"Inconnue") 
            entree_modify_adresse_mariage.insert(0,"Inconnue") 
            entree_modify_ville_mariage.insert(0,"Inconnue") 

        elif mariage_info == None:
            entree_modify_conjoint.insert(0,"Inconnue") 
            entree_modify_conjointe.insert(0,"Inconnue") 
            entree_modify_date_mariage.insert(0,"Inconnue") 
            entree_modify_adresse_mariage.insert(0,"Inconnue") 
            entree_modify_ville_mariage.insert(0,"Inconnue") 
        else:
            entree_modify_conjoint.delete(0,END)                
            entree_modify_conjointe.delete(0,END)
            entree_modify_date_mariage.delete(0,END)
            entree_modify_adresse_mariage.delete(0,END)  
            entree_modify_ville_mariage.delete(0,END)

            script_id_epoux_epouse="""select epoux.prenom,epouse.prenom
            from Personne
            as epoux
            left join Mariage
            on epoux.id_personne=Mariage.id_epoux
            left join Personne
            as epouse
            on epouse.id_personne=Mariage.id_epouse
            where id_epouse="""+str(mariage_info[0][1])+""" and id_epoux="""+str(mariage_info[0][0])+""" """
            curseur.execute(script_id_epoux_epouse)
            nom_prenom_epoux_epouse=curseur.fetchall()
            script_adresse_mariage="""select lieu.adresse,lieu.ville
            from lieu
            join Mariage
            on Mariage.id_lieu= lieu.id_lieu
            where Mariage.id_lieu="""+str(mariage_info[0][3])+""" """
            curseur.execute(script_adresse_mariage)
            adresse_mariage_ville_adresse=curseur.fetchall()

            print(nom_prenom_epoux_epouse)
            entree_modify_conjoint.insert(0,nom_prenom_epoux_epouse[0][0])
            entree_modify_conjointe.insert(0,nom_prenom_epoux_epouse[0][1])
            entree_modify_date_mariage.insert(0,mariage_info[0][2])
            entree_modify_adresse_mariage.insert(0,adresse_mariage_ville_adresse[0][0])
            entree_modify_ville_mariage.insert(0,adresse_mariage_ville_adresse[0][1])

            txt_modify_conjoint.config(text= "Prénom du conjoint :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            txt_modify_conjointe.config(text= "Prénom de la conjointe :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            txt_modify_mariage_date.config(text= "Date du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            txt_modify_mariage_ville.config(text= "Ville du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            txt_modify_mariage_adresse.config(text= "Adresse du mariage :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))

            entree_modify_conjoint.place(x=780,y=15)                    
            entree_modify_conjointe.place(x=780,y=45)
            entree_modify_date_mariage.place(x=780,y=75)
            entree_modify_adresse_mariage.place(x=780,y=105)  
            entree_modify_ville_mariage.place(x=780,y=135)
            txt_modify_conjoint.place(x=620,y=15)
            txt_modify_conjointe.place(x=600,y=42)
            txt_modify_mariage_date.place(x=640,y=70)
            txt_modify_mariage_adresse.place(x=620,y=100)
            txt_modify_mariage_ville.place(x=640,y=131)
    existe_pas = False
    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()
    curseur.execute("SELECT Personne.nom,Personne.prenom FROM Personne")   
    info_personne = curseur.fetchall()
    print(info_personne)
    for i in info_personne:
        #verifie que le prenom et nom sont bien present dans la base de donnée
        if(i[1].upper() == entre_recherche_prenom.get().upper() and i[0].upper() == entre_recherche_nom.get().upper()):

            
            for p in range (7):
                liste_feuille.append(Feuille(info_feuille[0][p],p))
        
            modify_nom.delete(0,END)
            modify_prenom.delete(0,END)
            modify_naissance_date.delete(0,END)
            modify_naissance_ville.delete(0,END)
            modify_prenom_pere.delete(0,END)
            modify_prenom_mere.delete(0,END)
            modify_deces_date.delete(0,END)
            modify_deces_ville.delete(0,END)
            modify_deces_adresse.delete(0,END)
            modify_naissance_adresse.delete(0,END)

            existe_pas = True
            #verifie que la liste contenant les information sur la genealogie ne sois pas vide sinon affiche la personne demander ou la date naissance/deces
            if tout_prenom_nom[k][0] == None:

                modify_nom.insert(0,"Inconnue")
            else:

                modify_nom.insert(0,tout_prenom_nom[k][0])

            if tout_prenom_nom[k][1] == None:

                modify_prenom.insert(0,"Inconnue")
            else:
                modify_prenom.insert(0,tout_prenom_nom[k][1])

            if info_deces_naissance == []:

                modify_naissance_date.insert(0,"Inconnue") 

            elif info_deces_naissance[h][3] == None:
                            
                modify_naissance_date.insert(0,"Inconnue") 
            else: 

                modify_naissance_date.insert(0,info_deces_naissance[h][3])

            if info_deces_naissance == []:

                modify_naissance_adresse.insert(0,"Inconnue") 

            elif info_deces_naissance[h][4] == None:

                modify_naissance_adresse.insert(0,"Inconnue")  
            else:

                modify_naissance_adresse.insert(0,info_deces_naissance[h][4])

            if info_deces_naissance == []:

                modify_naissance_ville.insert(0,"Inconnue") 

            elif info_deces_naissance[h][5] == None:

                modify_naissance_ville.insert(0,"Inconnue")  
            else:

                modify_naissance_ville.insert(0,info_deces_naissance[h][5])

            if tout_prenom_nom[h][3] == None:

                modify_prenom_pere.insert(0,"Inconnue")

            else:

                modify_prenom_pere.insert(0,tout_prenom_nom[h][3])
        

            if tout_prenom_nom[h][5] == None:

                modify_prenom_mere.insert(0,"Inconnue")
                
            else:
                modify_prenom_mere.insert(0,tout_prenom_nom[h][5])

            
                

            bouton_save.place(x=920,y=20)
            modify_prenom_mere.place(x=200,y=140)
            modify_prenom_pere.place(x=200,y=115)
            modify_naissance_ville.place(x=200,y=90)
            modify_naissance_date.place(x=200,y=65)
            modify_prenom.place(x=200,y=40)
            modify_nom.place(x=200,y=15)                                        
            modify_deces_date.place(x=470,y=15)               
            modify_deces_ville.place(x=470,y=40)                   
            modify_deces_adresse.place(x=470,y=65)
            modify_naissance_adresse.place(x=470,y=90)
            #condition si la personne n'a aucune information completer
            if info_deces_naissance == []:
                modify_deces_date.insert(0,"Inconnue")

                modify_deces_ville.insert(0,"Inconnue")   

                modify_deces_adresse.insert(0,"Inconnue")

            #condition si la personne et vivante
            elif info_deces_naissance[h][0] == "0" or info_deces_naissance[h][2]=="0" or info_deces_naissance[h][1]=="0":

                modify_deces_date.insert(0,"Inconnue/Vivant")
                modify_deces_ville.insert(0,"Inconnue/Vivant")
                modify_deces_adresse.insert(0,"Inconnue/Vivant")
            #affiche les information si existante
            else:
        
                modify_deces_date.insert(0,info_deces_naissance[h][0])

                modify_deces_ville.insert(0,info_deces_naissance[h][2])   

                modify_deces_adresse.insert(0,info_deces_naissance[h][1])






            numero_menu=2
            entre_recherche_nom.place_forget()
            entre_recherche_prenom.place_forget()
            texte_erreur.place_forget()
            txt_rentrer_prenom.place_forget()
            txt_rentrer_nom.place_forget()
            canevas_down.itemconfig(img_retour_off, image = retour_off)
            canevas_down.coords(img_retour_off,32,15)
            text_nom_pers.config(text = "Nom :" ,fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            text_prenom_pers.config(text = "Prénom :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            txt_deces_adresse.config(text= "Adresse de décés :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            txt_deces_date.config(text= "Date de décés :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            txt_deces_ville.config(text= "Ville de décés :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            texte_pere.config(text= "Prenom pére :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            texte_mere.config(text= "Prenom mére :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
            texte_naissance_adresse.config(text="Adresse de naissance :",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            txt_deces_adresse.place(x=320,y=15)
            txt_deces_date.place(x=345,y=40)
            txt_deces_ville.place(x=350,y=65)
            texte_naissance_adresse.place(x=300,y=88)
            text_nom_pers.place(x=134,y=15)
            text_prenom_pers.place(x=110,y=40)
            texte_naissance_date.place(x=18,y=65)
            texte_naissance_ville.place(x=42,y=90)
           
            texte_pere.place(x=71,y=115)
            texte_mere.place(x=68,y=140)
            canevas_down.delete(img_valider_off)
 


    if(not existe_pas):      
        texte_erreur.config(text = "Cet personne n'est pas dans la base de donnée.", font = ('', 15, ''))
        texte_erreur.place(x = 625 , y = 60)
    connexion.commit()
    connexion.close()
      



def UPDATE_longue():
    """Fonction qui permets de modifier des information déja existante dans toute les tables
    avec les condition qu'il soit donc presente dans la base de donnée"""
    infor_perso= (modify_nom.get(),modify_prenom.get())
    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()


    go_erreur=10
    curseur.execute("select Personne.id_personne from Personne where personne.nom=? and Personne.prenom=?",infor_perso)
    id_personne_recherchee = curseur.fetchall() 
    connexion.commit()
    connexion.close()
      #condition qui verifie si l'entry est vide ou pas si oui, definie le prenom comme NULL si non change le prenom
    if modify_prenom.get()=='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set Personne.prenom=NULL where Personne.id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()
    else:
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set prenom='"+str(modify_prenom.get())+"' where id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()
    #condition qui verifie si l'entry est vide ou pas si oui, definie le nom comme NULL si non change le nom
    if modify_nom.get()=='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set nom=NULL where id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()
    else:
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set nom='"+str(modify_nom.get())+"' where id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()

    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()
    curseur.execute("select personne.id_naissance from personne where personne.id_personne="+str(id_personne_recherchee[0][0]))
    id_naissance=curseur.fetchone()
    connexion.commit()
    connexion.close()
    print(id_naissance)
    #condition qui verifie si l'entry est vide ou pas si oui, definie la date comme NULL sinon change la date de naissance
    if modify_naissance_date.get()=='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Naissance set date=NULL where id_naissance="+str(id_naissance[0]))
        connexion.commit()
        connexion.close()
    else:
        if id_naissance==(None,):
            print("okok")
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE Naissance set date='"+str(modify_naissance_date.get())+"' where id_naissance="+str(id_naissance[0]))
            connexion.commit()
            connexion.close()
    id_naissance_lieu=None
    #condition qui verifie si l'id_naissance existe, si oui cherche l'id_lieu pour les recherche qui arrive
    if id_naissance != (None,):
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("select Naissance.id_lieu from naissance where id_naissance="+str(id_naissance[0]))
        id_naissance_lieu=curseur.fetchone()
        connexion.commit()
        connexion.close()
    if id_naissance_lieu !=None:
        #condition qui verifie si id_lieu de naissance existe si oui change la ville de naissance
        if modify_naissance_ville.get()=='':
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set ville=NULL where id_lieu="+str(id_naissance_lieu[0]))
            connexion.commit()
            connexion.close()
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set ville='"+str(modify_naissance_ville.get())+"' where id_lieu="+str(id_naissance_lieu[0]))
            connexion.commit()
            connexion.close() 

    id_naissance_lieu=None
    #condition qui verifie si id_lieu de naissance existe si oui change l'adresse de naissance
    if id_naissance_lieu!=None:

        if modify_naissance_adresse.get()=='':
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set adresse=NULL where id_lieu="+str(id_naissance_lieu[0]))
            connexion.commit()
            connexion.close()
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set adresse='"+str(modify_naissance_adresse.get())+"' where id_lieu="+str(id_naissance_lieu[0]))
            connexion.commit()
            connexion.close()

    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()
    curseur.execute("select personne.id_deces from personne where personne.id_personne="+str(id_personne_recherchee[0][0]))
    id_deces=curseur.fetchone()
    connexion.commit()
    connexion.close()
    id_deces=None
    #condition qui verifie si id_deces existe si oui change la date de deces
    if id_deces !=None:
        if modify_deces_date.get()=='':
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE Deces set date=NULL where id_deces="+str(id_deces[0]))
            connexion.commit()
            connexion.close()
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE Deces set date='"+str(modify_deces_date.get())+"' where id_deces="+str(id_deces[0]))
            connexion.commit()
            connexion.close()
    
    if id_deces !=None:
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur=connexion.cursor()
        curseur.execute("select deces.id_lieu from deces where id_deces="+str(id_deces[0]))
        id_deces_lieu=curseur.fetchone()
        connexion.commit()
        connexion.close()
    id_deces_lieu=None
        #condition qui verifie si id_deces existe si oui change la ville de deces
    if id_deces_lieu!=None:
        if modify_deces_ville.get()=='':
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set ville=NULL where id_lieu="+str(id_deces_lieu[0]))
            connexion.commit()
            connexion.close()
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set ville='"+str(modify_deces_ville.get())+"' where id_lieu="+str(id_deces_lieu[0]))
            connexion.commit()
            connexion.close() 
    #condition qui verifie si id_deces existe si oui change l'adresse de deces
    if id_deces_lieu!=None:
        if modify_deces_adresse.get()=='':
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set adresse=NULL where id_lieu="+str(id_deces_lieu[0]))
            connexion.commit()
            connexion.close()
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE lieu set adresse='"+str(modify_deces_adresse.get())+"' where id_lieu="+str(id_deces_lieu[0]))
            connexion.commit()
            connexion.close()
    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()
    curseur.execute("select personne.id_pere from Personne where personne.prenom='"+modify_prenom.get()+"' and personne.nom='"+modify_nom.get()+"'")
    id_pere=curseur.fetchone()
    connexion.commit()
    connexion.close()
    #condition pour changer le prenom de la mere si existante
    if modify_prenom_pere.get()=='' or modify_prenom_pere.get().upper() == "INCONNUE" :
        print(id_pere)
        print("--------")
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set id_pere=NULL where id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()
    else:
        if id_pere == (None,):
            print("VOILAAAAAA")
            go_erreur=go_erreur-1
            texte_erreur.config(text="Veuillez inserer un pére \navant de modifier ses information",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            texte_erreur.place(x=800,y=50)
            
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE Personne set prenom='"+modify_prenom_pere.get()+"' where id_personne="+str(id_pere[0]))
            connexion.commit()
            connexion.close()
    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()
    curseur.execute("select personne.id_mere from Personne where personne.prenom='"+modify_prenom.get()+"' and personne.nom='"+modify_nom.get()+"'")
    id_mere=curseur.fetchone()
    connexion.commit()
    connexion.close()
    #condition pour changer le prenom de la mere si existante
    if modify_prenom_mere.get()=='' or modify_prenom_mere.get().upper() == "INCONNUE":
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Personne set id_mere=NULL where id_personne="+str(id_personne_recherchee[0][0]))
        connexion.commit()
        connexion.close()
    else:
        if id_mere == (None,):
            texte_erreur.config(text="Veuillez inserer une mére \navant de modifier ses information",fg = 'red',bg='#AEFF00',font = ('', 12, ''))
            texte_erreur.place(x=800,y=50)
            go_erreur=go_erreur-1
        else:
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()
            curseur.execute("UPDATE Personne set prenom='"+modify_prenom_mere.get()+"' where id_personne="+str(id_mere[0]))
            connexion.commit()
            connexion.close()
            
    connexion=sqlite3.connect("Genealogie.db")
    curseur=connexion.cursor()           
    script_mariage_info='''SELECT Mariage.id_epoux, Mariage.id_epouse,Mariage.id_mariage
    FROM Mariage
    WHERE Mariage.id_epouse = ''' + str(id_personne_recherchee[0][0]) + ''' OR Mariage.id_epoux = ''' + str(id_personne_recherchee[0][0])
    curseur.execute(script_mariage_info)
    mariage_info = curseur.fetchall()
    connexion.commit()
    connexion.close()
    #condition pour modifier le/la conjoint/conjointe si existant
    if entree_modify_conjoint.get()!="Inconnue" and entree_modify_conjoint.get()!='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("select personne.id_personne from personne where personne.prenom='"+entree_modify_conjoint.get()+"'")
        id_new_epoux=curseur.fetchone()
        connexion.commit()
        connexion.close()
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("select personne.id_personne from personne where personne.prenom='"+entree_modify_conjointe.get()+"'")
        id_new_epouse=curseur.fetchone()
        connexion.commit()
        connexion.close()
        #condition pour derterminer si on change le conjoint ou la conjointe
        if str(mariage_info[0][0])== str(id_personne_recherchee[0][0]):
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()  
            curseur.execute("update Mariage set id_epouse="+str(id_new_epouse[0])+" where id_mariage="+str(mariage_info[0][2])+"")
            connexion.commit()
            connexion.close()
        elif str(mariage_info[0][1])== str(id_personne_recherchee[0][0]):
            connexion=sqlite3.connect("Genealogie.db")
            curseur=connexion.cursor()  
            curseur.execute("update Mariage set id_epoux="+str(id_new_epoux[0])+" where id_mariage="+str(mariage_info[0][2])+"")
            connexion.commit()
            connexion.close()
    #condition pour modifier la date de mariage si existant
    if entree_modify_date_mariage.get()!="Inconnue" and entree_modify_conjoint.get()!='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("UPDATE Mariage set date='"+str(entree_modify_date_mariage.get())+"' where id_mariage='"+str(mariage_info[0][2])+"'")
        connexion.commit()
        connexion.close()
    #condition pour modifier la ville de mariage si existant
    if entree_modify_ville_mariage.get()!="Inconnue" and entree_modify_conjoint.get()!='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("select mariage.id_lieu from mariage where mariage.id_mariage='"+str(mariage_info[0][2])+"'")
        id_mariage_lieu=curseur.fetchone()
        curseur.execute("UPDATE lieu set ville='"+entree_modify_ville_mariage.get()+"' where id_lieu="+str(id_mariage_lieu[0]))
        connexion.commit()
        connexion.close()
        #condition pour modifier l'adresse de mariage si existant
    if entree_modify_adresse_mariage.get()!="Inconnue" and entree_modify_conjoint.get()!='':
        connexion=sqlite3.connect("Genealogie.db")
        curseur=connexion.cursor()
        curseur.execute("select mariage.id_lieu from mariage where mariage.id_mariage='"+str(mariage_info[0][2])+"'")
        id_mariage_lieu=curseur.fetchone()
        curseur.execute("UPDATE lieu set adresse='"+entree_modify_adresse_mariage.get()+"' where id_lieu="+str(id_mariage_lieu[0]))
        connexion.commit()
        connexion.close()
    txt_validation_modification.place_forget()
    if go_erreur==10:
        txt_validation_modification.place(x=900,y=50)
        texte_erreur.place_forget()
    

        
       







def apparition_rechercher():
    """Permets de faire apparaitre l'interface rechercher avec les deux entry et le bouton valider"""
    global numero_menu   
    numero_menu=1
    DELETE_ALL()
    entre_recherche_prenom.place(x=120,y=120)
    entre_recherche_nom.place(x=300,y=120)
    txt_rentrer_nom.place(x=100,y=500)
    txt_rentrer_prenom.place(x=285,y=500)
    canevas_down.itemconfig(img_valider_off, image = valider_off)
    canevas_down.coords(img_valider_off,250,32)


def apparition_inseret():
    """Permets d'afficher l'interface inseret et de suprimmer le contenue de la feuille si
    l'utillisateur changer de menu"""
    global liste_feuille

    for i in range(len(liste_feuille)):
        liste_feuille[i].detruire()
        
    liste_feuille=[]
    DELETE_ALL()
    canevas_down.coords(img_valider_off,5000,15)
    canevas_down.coords(img_retour_off,5000,15)
    entre_insert_nom.place(x=250,y=40)
    entre_insert_prenom.place(x=250,y=100)
    insertion_personne.place(x=250,y=135)
    text_nom_pers.config(text = "Rentrée le nom d'une personne:", font = ('', 12, ''))
    text_prenom_pers.config(text = "Rentrée le prénom d'une personne:", font = ('', 12, ''))
    text_nom_pers.place(x=220,y=15)
    text_prenom_pers.place(x=220,y=75)




def etape_naissance():
    """permets de passer a l'étape de naissance l'or de l'insertion"""
    DELETE_ALL()
    entre_insert_naissance_date.place(x=250,y=15)
    entre_insert_naissance_adresse.place(x=250,y=65)
    entre_insert_naissance_ville.place(x=250,y=115)
    insertion_naissance.place(x=250,y=140)
    texte_naissance_date.config(text = "Rentrée la date de naissance\n de la personne:",fg='red', font = ('', 11, ''))
    txt_lieu_adresse.config(text="Rentrée l'adresse de naissance:",fg='red',font=('',11,''))
    txt_lieu_ville.config(text="Rentrée la ville de naissance:",fg='red',font=('',11,''))
    texte_naissance_date.place(x=50,y=5)
    txt_lieu_adresse.place(x=25,y=60)
    txt_lieu_ville.place(x=35,y=115)


def etape_deces():
    """permets de passer a l'étape de décés l'or de l'insertion"""
    DELETE_ALL()
    insertion_deces.place(x=250,y=140)
    entre_insert_deces_date.place(x=250,y=15)
    entre_insert_deces_adresse.place(x=250,y=65)
    entre_insert_deces_ville.place(x=250,y=115)
    texte_naissance_ville.config(text = "Rentrée la date de deces \n de la personne:",fg='red', font = ('', 11, ''))
    txt_lieu_adresse.config(text="Rentrée l'adresse de deces:",fg='red',font=('',11,''))
    txt_lieu_ville.config(text="Rentrée la ville de deces:",fg='red',font=('',11,''))
    texte_erreur.config(text="Si la personne est vivante \ncompleter les trois zone d'entrée avec 0")
    texte_erreur.place(x=500,y=65)
    texte_naissance_ville.place(x=34,y=5)
    txt_lieu_adresse.place(x=25,y=60)
    txt_lieu_ville.place(x=35,y=115)


def etape_pere():
    """permets de passer a l'étape du pére l'or de l'insertion"""
    DELETE_ALL()
    entre_insert_nom.place(x=250,y=40)
    entre_insert_prenom.place(x=250,y=100)
    insertion_pere.place(x=250,y=135)
    text_nom_pers.config(text = "Rentrée le nom d'une personne(pére):", font = ('', 12, ''))
    text_prenom_pers.config(text = "Rentrée le prénom d'une personne(pére):", font = ('', 12, ''))
    text_nom_pers.place(x=220,y=15)
    text_prenom_pers.place(x=220,y=75)
    canevas_down.coords(img_valider_off,5000,15)
    canevas_down.coords(img_retour_off,5000,15)

def etape_mere():
    """permets de passer a l'étape de la  mére l'or de l'insertion"""
    DELETE_ALL()
    entre_insert_nom.place(x=250,y=40)
    entre_insert_prenom.place(x=250,y=100)
    insertion_mere.place(x=250,y=135)
    text_nom_pers.config(text = "Rentrée le nom d'une personne(mére):", font = ('', 12, ''))
    text_prenom_pers.config(text = "Rentrée le prénom d'une personne(mére):", font = ('', 12, ''))
    text_nom_pers.place(x=220,y=15)
    text_prenom_pers.place(x=220,y=75)
    canevas_down.coords(img_valider_off,5000,15)
    canevas_down.coords(img_retour_off,5000,15)



def etape_mariage_nom_prenom():
    """permets de passer à l'étape d'insertion du prenom et du nom dans le menu mariage"""
    DELETE_ALL()
    entree_conjoint_nom.place(x=230,y=50)
    entree_conjoint_prenom.place(x=230,y=140)
    entree_conjointe_nom.place(x=400,y=50)
    entree_conjointe_prenom.place(x=400,y=140)
    
    text_nom_pers.config(text = "Rentrée le nom\nde la conjointe:", font = ('', 12, ''))
    text_prenom_pers.config(text = "Rentrée le prénom\nde la conjointe:", font = ('', 12, ''))
    texte_mere.config(text = "Rentrée le nom\nde la conjoint:", font = ('', 12, ''))
    texte_pere.config(text = "Rentrée le prénom\nde la conjoint:", font = ('', 12, ''))

    text_nom_pers.place(x=220,y=5)
    text_prenom_pers.place(x=210,y=90)
    texte_pere.place(x=380,y=90)
    texte_mere.place(x=390,y=5)
    bouton_nom_prenom_mariage.place(x=565,y=110)

    

def etape_mariage_date_adresse_ville():
    """permets de passer à l'étape d'insertion des information de ville,adresse et ville du mariage"""
    DELETE_ALL()

    entree_ville_mariage.place(x=250,y=115)
    entree_adresse_mariage.place(x=250,y=65)
    entree_date_mariage.place(x=250,y=15)
    bouton_date_adresse_ville_mariage.place(x=590,y=110)
    txt_lieu_adresse.config(text="Rentrée l'adresse du mariage:",fg='red',font=('',11,''))
    txt_lieu_ville.config(text="Rentrée la ville du mariage:",fg='red',font=('',11,''))
    texte_naissance_date.config(text = "Rentrée la date du mariage\n des mariées:",fg='red', font = ('', 11, ''))
    texte_naissance_date.place(x=50,y=5) 
    txt_lieu_adresse.place(x=25,y=60)
    txt_lieu_ville.place(x=35,y=115)


    





    


def back_identite():
    """ Permets de revenir a l'étape de recherche pour en effectuer une nouvelle"""
    global img_retour_off,liste_tempo_affichage,img_valider_off,numero_menu,liste_feuille
    DELETE_ALL()

    for i in range(len(liste_feuille)):
        liste_feuille[i].detruire()
        
    liste_feuille=[]
    numero_menu=1
    canevas_down.coords(img_retour_off,5000,15)
    entre_recherche_nom.place(x=300,y=120)
    entre_recherche_prenom.place(x=120,y=120)
    txt_rentrer_nom.place(x=100,y=500)
    txt_rentrer_prenom.place(x=285,y=500)
    canevas_down.itemconfig(img_valider_off, image = valider_on)
    liste_tempo_affichage=[]
    img_valider_off=canevas_down.create_image(250,32, image=valider_off)





etape_insertion=1

def save_insert(x):
    """permets de sauvgarder l'étape ou l'on c'est arreter durant l'insertion d'une personne"""
    global etape_insertion
    if x==1:
        apparition_inseret()
    elif x==2:
        etape_naissance()
    elif x==3:
        etape_deces()
    elif x==4:
        etape_pere()
    elif x==5:
        etape_mere()


etape_mariage=1

def save_insert_mariage(x):
    """permets de sauvgarder l'étape ou l'on c'est arreter durant l'insertion d'une mariage"""
    global etape_mariage
    if x==1:
        etape_mariage_nom_prenom()
    elif x==2:
        etape_mariage_date_adresse_ville()
    
def mariage_depart():
    """permets d'acceder au menu du mariage """
    global numero_menu
    numero_menu=3
    DELETE_ALL()
    save_insert_mariage(etape_mariage)
    
def insert_depart():
    """permets de faire appelle a la fonction de save_insert durant les differentes étapes """
    global etape_insertion,img_valider_off,numero_menu
    numero_menu=0
    DELETE_ALL()
    save_insert(etape_insertion)

def DELETE_ALL():
    """  permets de suprimmer tout les éléments en une fois  """
    global img_retour_off,img_valider_off
    txt_validation_modification.place_forget()
    bouton_save.place_forget()
    entree_modify_date_mariage.place_forget()
    entree_modify_adresse_mariage.place_forget()
    entree_modify_ville_mariage.place_forget()
    txt_modify_mariage_date.place_forget()
    txt_modify_mariage_ville.place_forget()
    txt_modify_mariage_adresse.place_forget()
    texte_naissance_adresse.place_forget()
    txt_modify_conjointe.place_forget()
    txt_modify_conjoint.place_forget()
    entree_modify_date_mariage.delete(0,END)
    entree_modify_adresse_mariage.delete(0,END)  
    entree_modify_ville_mariage.delete(0,END)
    entree_modify_conjointe.place_forget()
    entree_modify_conjointe.delete(0,END)
    entree_modify_conjoint.place_forget()
    entree_modify_conjoint.delete(0,END)
    modify_naissance_adresse.place_forget()
    modify_naissance_adresse.delete(0,END)
    bouton_date_adresse_ville_mariage.place_forget()
    etape_bis_1_mariage.place_forget()
    etape_bis_2_mariage.place_forget()
    bouton_nom_prenom_mariage.place_forget()
    entree_adresse_mariage.place_forget()
    entree_ville_mariage.place_forget()
    entree_date_mariage.place_forget()
    entree_adresse_mariage.delete(0,END)
    entree_ville_mariage.delete(0,END)
    entree_date_mariage.delete(0,END)
    entree_conjoint_nom.place_forget()
    entree_conjoint_prenom.place_forget()
    entree_conjointe_nom.place_forget()
    entree_conjointe_prenom.place_forget()
    entree_conjoint_nom.delete(0,END)
    entree_conjoint_prenom.delete(0,END)
    entree_conjointe_nom.delete(0,END)
    entree_conjointe_prenom.delete(0,END)
    txt_deces_adresse.place_forget()
    txt_deces_date.place_forget()
    txt_deces_ville.place_forget()
    txt_lieu_adresse.place_forget()
    txt_deces_date.place_forget()
    modify_prenom_mere.place_forget()
    modify_prenom_pere.place_forget()
    modify_prenom_mere.delete(0,END)
    modify_prenom_pere.delete(0,END)
    modify_deces_ville.place_forget()
    modify_deces_ville.delete(0,END)
    modify_deces_date.place_forget()
    modify_deces_date.delete(0,END)
    modify_deces_adresse.place_forget()
    modify_deces_adresse.delete(0,END)
    modify_naissance_adresse.place_forget()
    modify_naissance_adresse.delete(0,END)
    modify_naissance_ville.place_forget()
    modify_naissance_ville.delete(0,END)
    modify_naissance_date.place_forget()
    modify_naissance_date.delete(0,END)
    modify_nom.place_forget()
    modify_nom.delete(0,END)
    modify_prenom.place_forget()
    modify_prenom.delete(0,END)
    etape_bon.place_forget()
    etape_4bis.place_forget()
    etape_3bis.place_forget()
    etape_5bis.place_forget()
    txt_lieu_ville.place_forget()
    txt_lieu_adresse.place_forget()
    insertion_deces.place_forget()
    etape_2bis.place_forget()
    insertion_personne.place_forget()
    entre_insert_nom.place_forget()
    entre_insert_prenom.place_forget()
    entre_insert_pere_prenom.place_forget()
    entre_insert_pere_nom.place_forget()
    entre_insert_mere_prenom.place_forget()
    entre_insert_mere_nom.place_forget()
    entre_insert_lieu_ville.place_forget()
    entre_insert_lieu_adresse.place_forget()
    entre_insert_naissance_adresse.place_forget()
    entre_insert_naissance_ville.place_forget()
    entre_insert_naissance_date.place_forget()
    entre_insert_deces_adresse.place_forget()
    entre_insert_deces_date.place_forget()
    entre_insert_deces_ville.place_forget()
    texte_erreur.place_forget()
    entre_insert_nom.delete(0,END)
    entre_insert_prenom.delete(0,END)
    entre_insert_pere_prenom.delete(0,END)
    entre_insert_pere_nom.delete(0,END)
    entre_insert_mere_prenom.delete(0,END)
    entre_insert_mere_nom.delete(0,END)
    entre_insert_lieu_ville.delete(0,END)
    entre_insert_lieu_adresse.delete(0,END)
    entre_insert_naissance_adresse.delete(0,END)
    entre_insert_naissance_ville.delete(0,END)
    entre_insert_naissance_date.delete(0,END)
    entre_insert_deces_adresse.delete(0,END)
    entre_insert_deces_date.delete(0,END)
    entre_insert_deces_ville.delete(0,END)
    entre_recherche_nom.delete(0,END)
    entre_recherche_prenom.delete(0,END)
    entre_recherche_nom.place_forget()
    entre_recherche_prenom.place_forget()
    text_nom_pers.place_forget()
    text_prenom_pers.place_forget()
    texte_naissance_date.place_forget()
    texte_naissance_ville.place_forget()
    texte_pere.place_forget()
    texte_mere.place_forget()
    txt_rentrer_prenom.place_forget()
    txt_rentrer_nom.place_forget()
    insertion_mere.place_forget()
    insertion_pere.place_forget()
    insertion_naissance.place_forget()
    canevas_down.coords(img_retour_off,5000,15)
    canevas_down.coords(img_valider_off,5000,15)
    for i in range(len(liste_tempo_affichage)):
        liste_tempo_affichage[i].place_forget()

#creation de tous les bouton
rechercher_depart= Button(window, text="Rechercher", bg="yellow", bd=2,command=apparition_rechercher)
rechercher_depart.place(x=0,y=408)
inseret_depart = Button(window, text="Insérer", bg="yellow", bd=2,command=insert_depart)
inseret_depart.place(x=69,y=408)
liaison_depart=Button(window, text="Liaison",bg="yellow", bd=2,command=mariage_depart)
liaison_depart.place(x=115.1,y=408)

insertion_pere=Button(canevas_down, text="valider", bg="yellow", bd=2,command=inseret_pere)
insertion_mere=Button(canevas_down, text="valider", bg="yellow", bd=2,command=inseret_mere)
insertion_naissance=Button(canevas_down, text="valider", bg="yellow", bd=2,command=inseret_naissance)
insertion_deces=Button(canevas_down, text="valider", bg="yellow", bd=2,command=inseret_deces)
insertion_personne=Button(canevas_down,text="valider",bg="yellow", bd=2,command=inseret_personne)

etape_2bis=Button(canevas_down,text="Etape naissance",bg="red", bd=2,command=etape_naissance)
etape_3bis=Button(canevas_down,text="Etape deces",bg="red", bd=2,command=etape_deces)
etape_4bis=Button(canevas_down,text="Etape pére",bg="red", bd=2,command=etape_pere)
etape_5bis=Button(canevas_down,text="Etape mére",bg="red", bd=2,command=etape_mere)
etape_bon=Button(canevas_down,text="nouvelle personne",bg="red", bd=2,command=apparition_inseret)


bouton_nom_prenom_mariage = Button(canevas_down,text=" valider !",bg="yellow", bd=2,command=insertion_nom_prenom_du_mariage)
bouton_date_adresse_ville_mariage = Button(canevas_down,text=" Valider les\ninformations !",bg="yellow", bd=2,command=insertion_date_adresse_ville_mariage)
etape_bis_1_mariage = Button(canevas_down,text="étape date !",bg="red", bd=2,command=etape_mariage_date_adresse_ville)
etape_bis_2_mariage= Button(canevas_down,text="revenir a l'étape\n de depart !",bg="red", bd=2,command=etape_mariage_nom_prenom)

bouton_save=Button(canevas_down,image=save,command=UPDATE_longue,bd=0)


texte_erreur = Label(canevas_down, fg = 'red',bg='#AEFF00')


#inisialisation des variables utiliser donc les différentes fonction
id_epoux=None
id_epouse=None
info_personne= None
id_personne_recherchee=None
numero_menu=None

#creation de la liste d'affiche temporaire
liste_tempo_affichage=[]
#creation de la liste feuille qui stock les nom et prenom des personne 
#qui doivent etre afficher dans l'arbre
liste_feuille=[]

#creation de touts les texte utiliser
text_nom_pers= Label(canevas_down,text = "Nom :" ,fg = 'red',bg='#AEFF00',font = ('', 13, ''))
text_prenom_pers = Label(canevas_down,text = "Prénom :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
texte_naissance_date = Label(canevas_down,text = "Année de naissance :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
texte_naissance_ville = Label(canevas_down,text = "Ville de naisance :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
texte_naissance_adresse=Label(canevas_down, fg='red', bg='#AEFF00')

texte_mere = Label(canevas_down,text = "Prenom mére :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
texte_pere = Label(canevas_down,text = "Prenom pére :",fg = 'red',bg='#AEFF00',font = ('', 13, ''))
txt_rentrer_prenom = Label(window,text = "rentrer le nom  :",fg = 'red',bg='#AEFF00',font = ('', 14, ''))
txt_rentrer_nom = Label(window,text = "rentrer le prénom :",fg = 'RED',bg='#AEFF00',font = ('', 14, ''))
txt_lieu_adresse = Label(canevas_down,text = "lieu de :",fg = '#3E2700',bg='#AEFF00',font = ('', 13, ''))
txt_lieu_ville= Label(canevas_down,text = "lieu de :",fg = '#3E2700',bg='#AEFF00',font = ('', 13, ''))

txt_deces_date=Label(canevas_down, fg='red', bg='#AEFF00')
txt_deces_adresse=Label(canevas_down, fg='red', bg='#AEFF00')
txt_deces_ville=Label(canevas_down, fg='red', bg='#AEFF00')


txt_modify_conjoint=Label(canevas_down, fg='red', bg='#AEFF00')
txt_modify_conjointe=Label(canevas_down, fg='red', bg='#AEFF00')
txt_modify_mariage_date=Label(canevas_down, fg='red', bg='#AEFF00')
txt_modify_mariage_ville=Label(canevas_down, fg='red', bg='#AEFF00')
txt_modify_mariage_adresse=Label(canevas_down, fg='red', bg='#AEFF00')

txt_validation_modification=Label(canevas_down,text="Modification enregistrer !",fg='red', bg='#AEFF00',font = ('', 13, ''))

#bind associer au deux canevas permettant de connaitre les zones de clique
#pour les feuilles de l'arbre(canvevas_up) et l'effet onclick sur l'etape rechercher
canevas_down.bind("<Button-1>", deplacement_souris)
canevas_down.bind("<Motion>", deplacement_valider)
canevas_up.bind("<Button-1>", deplacement_souris_up)
canevas_up.bind("<Motion>", deplacement_valider_up)


window.mainloop()