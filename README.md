# Projet_8

## Ressources
* Tableau Trello: https://trello.com/b/NTdWO5qf/projet-8-plateforme-purbeurre
* Site: https://ocpurbeurre.herokuapp.com

## Installation
### Installez votre environnement virtuel avec Pipenv
    Pipenv est très facile d'utilisation. Une fois le projet téléchargé, ouvrez votre invite de commande et jusqu'au dossier racine du projet.  
    Une fois arrivé, assurez-vous que Pipenv est bien installé en tapant la commande "pipenv". Si ce n'est pas le cas, tapez la commande "pip install pipenv".  
    Pour activer votre environnement de travail, lancez la commande "pipenv shell". Si c'est la première fois que vous utilisez le projet, tapez ensuite "pipenv install" afin de télécharger les modules python nécessaire au bon fonctionnement du projet.

### Installer ocpurbeurre
    Avant la première utilisation de l'application, n'oubliez pas de rassembler tous les fichiers statiques dans un même dossier, grâce à la commande "python manage.py collectstatic."  
    Enfin, Il faut que vous installiez la base de données. Commencez par télécharger PostgreSQL, puis revenez à votre application (n'oublier d'activer votre environnement virtuel) et lancer la commande "python manage.py migrate" afin d'initialiser la base de donnée. Vous pourrez ensuite la remplir grâce à la commande "python manage.py fill".  

### Lancer ocpurbeurre
    Après avoir activé votre environnement virtuel, vous pouvez lancer votre application grâce à la commande "gunicorn ocpurbeurre.wsgi".  
    Le site sera disponible sur l'adresse local de votre ordinateur.