import requests
import bs4
import mysql.connector
from mysql.connector import Error
import os
msqs=True
Academie=['rouen','aix-marseille','amiens','besancon','bordeaux','caen','clermont-ferrand','corse','dijon','grenoble','guadeloupe','guyane','lille','limoges','lyon','martinique','mayotte','montpellier','nancy-metz','nantes','nice','orleans-tours','paris-creteil-versailles','poitiers','reims','rennes','reunion','strasbourg','toulouse']
Annee=['2020','2019','2018']
##Section=['S','ES','L']
Section=['S','ES','L']
Alphabet=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
##Fonction de generation des urls de pages privees de la lettre de recherche
def make_page(ACademie, ANnee, SEction): ##ACademie est une liste, ANnee est une liste et SEction est une liste
    page=[]
    Suivi=[]
    for academie in ACademie:
        for annee in ANnee:
            for section in SEction:
                token='http://etudiant.aujourdhui.fr/etudiant/resultats/bac/'
                token+=academie
                token+='/470-'
                ##token+='/430-'
                token+=section
                token+='/fr/'
                token+=annee
                token+='.html?q='
                page.append(token)
                info=academie
                info+=' '
                info+=section
                info+=' '
                info+=annee
                Suivi.append(info)
    return (page,Suivi)

##Fonction permettant de generer les urls contenant la lettre /de recherche
def get_pages(Token, alphabet):##Token est le debut de l'url et alphabet est une liste
        pages = []
        for lettre in alphabet:
            j = token + lettre
            pages.append(j)
        return pages
##Generation des ulrs des pages privees de la lettre de recherches
page = make_page(Academie,Annee,Section)
n=open('admis_bac/name2.txt','w')
n.close()
for t in range(len(page[0])):
    token=page[0][t]
    info=page[1][t]
    infs=info.split()
    Section=infs[1]
    ##Generation des urls de toutes les pages (recherche par ordre alphabetique)
    pages = get_pages(token,Alphabet)
    m=0
    ##Recuperation de l'academie et de l'annee dans l'adresse de la page
    academie=infs[0]
    year=infs[2]
    fname=academie
    fname+='_'
    fname+=year
    fname+='.txt'
    s=Section
    if s=='S':
        w=open('admis_bac/name2.txt','a')
        w.write(fname)
        w.write('\n')
        w.close()
        er='admis_bac/'
        er+=fname
        ##Ouverture du fichier en Ã©criture permettant d'Ã©viter les doublons si le programme
        ##a dÃ©jÃ  Ã©tÃ© executer
        erase=open(er,'w')
        erase.close()
    ##Fonction d'affichage pour suivre l'avancee du download
    print(info)
    fw='admis_bac/'
    fw+=fname
    filed=open(fw, 'a')
    for i in pages:
        ##Connection a la page
        reponse = requests.get(i)
        soup = bs4.BeautifulSoup(reponse.text, 'html.parser')
        ##Recherches dans le html source de la page 
        name_box = soup.find_all("td", {"class":"nom"})
        spe_box = soup.find_all("td",{"class":"specialite"})
        resultat_box = soup.find_all("td",{"class":"resultats"})
        for i in range(len(name_box)):
            flag=0
            name=''
            spe=''
            ad=''
            a=str(resultat_box[i])
            n=str(name_box[i])
            s=str(spe_box[i])
            ##Recuperation de la specialite
            for e in s:
                if e=='>':
                   flag+=1
                elif flag==2 and not(e=='<'):
                    spe+=e
                elif flag==2 and e=='<':
                    flag=0
                    break
            ##Recuperation du resultat
            for g in a:
                if g=='>':
                   flag+=1
                elif flag==3 and not(g=='<'):
                    ad+=g
                elif flag==3 and g=='<':
                    flag=0
                    break
            ##Les noms des personnes du rattrapage sont sous un format different
            if ad[0]=='R':  
                for e in n:
                    if e=='>':
                       flag+=1
                    elif flag==2 and not(e=='<'):
                        name+=e
                    elif flag==2 and e=='<':
                        flag=0
                        break
            else:
                for e in n:
                    if e=='>':
                       flag+=1
                    elif flag==3 and not(e=='<'):
                        name+=e
                    elif flag==3 and e=='<':
                        flag=0
                        break
            spe=Section
            ##Inscription de la combinaison nom et prenoms
            ##specialite 
            ##et Admission
            ##Dans le fichier de l'academie, de l'annee
            filed.write(name)
            filed.write("\n")
            filed.write(spe)
            filed.write("\n")
            filed.write(ad)
            filed.write("\n")
    filed.close()
##Partie du code permettant l'insertion dans la db 
if msqs:
    import mysql.connector
    from mysql.connector import Error
    def created_db_connection(host_name, user_name, user_password, db_name):
        connection = None
        try:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("MySQL Database connection successful")
        except Error as err:
            print(f"Error: '{err}'")

        return connection
    def execute_query(connection, query):
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            print("Query successful")
        except Error as err:
            print(f"Error: '{err}'")
    def read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as err:
            print(f"Error: '{err}'")
    ##Set-up pour l'insertion dans la db
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Zc:!Er45{ty89",
        database="bac"
    )
    mycursor = mydb.cursor() 
    connection=created_db_connection("localhost", "root", "Zc:!Er45{ty89", "bac")
    q1 = """
    SELECT COUNT(id)
    FROM admis_bac;
    """
    r= read_query(connection, q1) ##Id en non-auto-icrement donc on compte manuelment
    e=int(r[0][0])
    print(e)
    e+=1
    f=open("name.txt", "r")
    l=f.readlines()
    ##Boucle qui permet d'inserer de la data provenant de plusieur fichier en une seule execution
    for h in l :
        name=h.strip()
        print(name)
        flag=0
        a=''
        y=''
        ##Récupération des paramètres d'académie et de date sur le nom du fichier
        for d in name:
            if d=='.':
                break
            if d=='_':
                flag+=1
            elif flag==0:
                a+=d
            elif flag==1:
                y+=d
        file= open(name, "r")
        Lines=file.readlines()
        filed=open("e1.txt", "w")
        c=1
        ##Conversion du fichier en un fichier exploitable pour l'insertion
        for line in Lines:
            text=line.strip()
            if len(text)>=4:
                if c%3==1:
                    res = []
                    temp = ''
                    text+='aa'
                    for i in range(len(text)-2):
                        ele=text[i]
                        if ele == ' ' and text[i+2].islower():
                                res.append(temp)
                                temp = ''
                        else :
                                temp += ele
                    res.append(temp)

                    for k in range (len(res)):
                        filed.write(res[k])
                        filed.write("\n")
                else:
                    filed.write(text)
                    filed.write("\n")
                c+=1
        file.close()
        filed.close()
        ##Phase d'insertion
        file= open("e1.txt", "r")
        Lines=file.readlines()
        c=0
        p2=' '
        p3=' '
        for line in Lines:
            if c==0:
                n=line.strip()
                c+=1
            elif c==1:
                p=line.strip()
                c+=1
            elif c==2 and line[0].islower():
                p2=line.strip()
                c+=1
            elif c==3 and line[0].islower():
                p3=line.strip()
                c+=1
            elif (c==2 or c==3 or c==4) and (line[0]=='S' or line[0]=='E' or line[0]=='L' or line[0]=='B'):
                s=line.strip()
            elif (line[0]=='A' and line[1]=='d' and line[2]=='m' and line[3]=='i' and line[4]=='s'):
                ad=line.strip()
                c=0
                sql="INSERT INTO admis_bac ( id, nom, prenom, deuxieme_prenom, troisieme_prenom, section, admission, academie, annee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                val=(e, n, p, p2, p3, s, ad, a, y)
                mycursor.execute(sql, val)
                mydb.commit()
                e+=1
                p2=' '
                p3=' '
                print(e,' recorde insterted')
        file.close() 
