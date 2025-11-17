Novabank

**GUIDE D'INSTALLATION**
via terminal -> .\env\Scripts\Activate.ps1 
                pip install -r requirements.txt
                python manage.py makemigrations
                python manage.py migrate
                python manage.py runserver  

**A PROPOS**

Application de gestion de comptes bancaires simulés qui a principalement pour objectif de gérer les dépôts, retraits et de consulter l'historique des opérations (dépôts et retraits).

Nous avons deux rôles d'utilisateurs tels que l'admin (pour gérer les clients et leurs comptes bancaires) et les clients (pour simuler l'acquisition des opérations).

**DÉMONSTRATION**

1/ Accueil pour choisir si nous sommes client ou admin, dont chaque utilisateur a ses propres interfaces de login.

2/ -login admin (usernale et password)
   -login client (Email, password, numéro de compte généré par l'admin aprés creation de compte)

3/**entré vers dashboard_admin -> Nous avons l'interface d'accueil "admin" dont on peut visualiser la représentation graphique par courbe des dépôts et retraits effectués par les clients en fonction du temps. | L'admin peut gérer les clients en effectuant le CRUD dans la section "clients". | Il peut accepter ou rejeter les transactions des clients en attente dans la section "opérations". | Déconnexion

  ** entré vers dashboard_client -> Nous avons l'interface d'accueil pour visualiser et s'informer par rapport aux services et les sièges de NOVABANK. Dans la section Historique, nous pouvons voir les dernières opérations du client et Cet historique est considéré comme reçu ou facture. | dans la section opération , chaques clients peuvent effectuer les depots (par cheques et especes) et retraits 

**TECH STACK**

FRAMEWORK FULLSTACK : DJANGO soit FRONT -> HTML,CSS,JS 
                                        &
                                  BACK  -> Python
BDD : SQLITE

OUTILS : MATPLOTLIB (Géneration du courbe graph), SVG (Carte interactive)

