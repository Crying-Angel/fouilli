import requests
import bs4
import mysql.connector
from mysql.connector import Error
import os
try:
    os.mkdir('admis_bac')
except:
    print("Attention le dossier de destination existe déjà")
insmsql=input("Avez vous mysql server ? Y/N : ")
if insmsql=='Y' or insmsql=='y':
    msqs=True
    hst=input("Veuillez renseigner le nom de l'hôte: ")
    usr=input("Veuillez renseigner le nom de l'utilisateur: ")
    pw=input("Veuillez renseigner le mot de passe: ")
    rdb=input("Souhaitez vous utiliser une db existante ? Y/N")
    if rdb=='Y' or rdb=='y':
        db=input("Veuillez renseigner la db")
    else:
        db="bac"
        def create_server_connection(host_name, user_name, user_password):
            connection = None
            try:
                connection = mysql.connector.connect(
                    host=host_name,
                    user=user_name,
                    passwd=user_password
                )
                print ("MYSQL Database connection successful")
            except Error as err:
                print(f"Error : '{err}'")
            return connection

        def create_database(connection, query):
            cursor = connection.cursor()
            try:
                cursor.execute(query)
                print("Database created successfully")
            except Error as err:
                print(f"Error: '{err}'")
        connection = create_server_connection(hst, usr, pw)
        create_database_query= "CREATE DATABASE bac"
        create_database(connection, create_database_query)

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
    create_bac_table = """
    CREATE TABLE admis_bac (
      id INT PRIMARY KEY,
      nom VARCHAR(240) NOT NULL,
      prenom VARCHAR(240) NOT NULL,
      deuxieme_prenom VARCHAR(240),
      troisieme_prenom VARCHAR(240),
      section VARCHAR(240),
      admission VARCHAR(240),
      academie VARCHAR(240),
      annee VARCHAR(20)
      );
      """
    connection=created_db_connection(hst, usr, pw, db)
    execute_query(connection, create_bac_table)
else:
    msqs=False
Academie=['rouen','aix-marseille','amiens','besancon','bordeaux','caen','clermont-ferrand','corse','dijon','grenoble','guadeloupe','guyane','lille','limoges','lyon','martinique','mayotte','montpellier','nancy-metz','nantes','nice','oreleans-tours','paris-creteil-versailles','poitiers','reims','rennes','reunion','strasbourg','toulouse']
Annee=['2017']
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
n=open('admis_bac/name.txt','w')
n.close()
for t in range(len(page[0])):
    token=page[0][t]
    info=page[1][t]
    ##Generation des urls de toutes les pages (recherche par ordre alphabetique)
    pages = get_pages(token,Alphabet)
    m=0
    academie=''
    year=''
    ##Recuperation de l'academie et de l'annee dans l'adresse de la page
    for k in token:
        if k=='/':
            m+=1
        elif m==6:
            academie+=k
        elif m==9 and k!='.':
            year+=k
        elif m==9 and k=='.':
            break
    fname=academie
    fname+='_'
    fname+=year
    fname+='.txt'
    kf=0
    s=' '
    for k in info:
        if k==' ':
            kf+=1
        elif kf==1:
            s+=k
    if s=='S':
        w=open('admis_bac/name.txt','a')
        w.write(fname)
        w.write('\n')
        w.close()
        er='admis_bac/'
        er+=fname
        ##Ouverture du fichier en écriture permettant d'éviter les doublons si le programme
        ##a déjà été executer
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
        host=hst,
        user=usr,
        password=pw,
        database=db
    )
    mycursor = mydb.cursor() 
    connection=created_db_connection(hst, usr, pw, db)
    q1 = """
    SELECT COUNT(id)
    FROM admis_bac;
    """
    r= read_query(connection, q1) ##Id en non-auto-icrement donc on compte manuelment
    e=int(r[0][0])
    print(e)
    e+=1
    f=open("admis_bac/name.txt", "r")
    l=f.readlines()
    ##Boucle qui permet d'inserer de la data provenant de plusieur fichier en une seule execution
    for h in l :
        name=h.strip()
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
        fw='admis_bac/'
        fw+=name
        file= open(fw, "r")
        Lines=file.readlines()
        filed=open("admis_bac/temp.txt", "w")
        c=1
        ##Conversion du fichier en un fichier exploitable pour l'insertion
        for line in Lines:
            text=line.strip()
            if len(text)>=4:
                if c%3==1:
                    res = []
                    temp = ''
                    text+='aa'
                    d=0
                    for i in range(len(text)-2):
                        ele=text[i]
                if ele == ' ' and text[i+2].islower() and d<3:
                        res.append(temp)
                        temp = ''
                        d+=1
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
        print(text)
file.close()
filed.close()


##Phase d'insertion
file= open("admis_bac/temp.txt", "r")
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
    elif (c==2 or c==3 or c==4) and (line[0]=='S' or line[0]=='E' or line[0]=='L'):
        s=line.strip()
    elif (line[0]=='A' and line[1]=='d' and line[2]=='m' and line[3]=='i' and line[4]=='s') or (line[0]=='R' and line[1]=='a'):
        ad=line.strip()
        c=0
        sql="INSERT INTO admis_bac ( id, nom, prenom, deuxieme_prenom, troisieme_prenom, section, admission, academie, annee) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val=(e, n, p, p2, p3, s, ad, a, y)
        mycursor.execute(sql, val)
        mydb.commit()
        print (e, "record inserted.", a , y)
        e+=1
        p2=' '
        p3=' '
file.close()

