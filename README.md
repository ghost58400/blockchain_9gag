# Blockchain 9gag

This is the repository for the project "blockchain 9gag".


## Installation

* First, you have to [install Docker](https://docs.docker.com/install/) on your machine if it is not already.
* Run:
```
sudo docker build -t blockchain_9gag ~/blockchain_9gag
```
*(replace ~/blockchain_9gag with the directory where you cloned the repository)*


## Running a new Docker Container
* Simply run the following command to create a new container:
```
sudo docker run -p 80:80 -p 1234:1234 -it blockchain_9gag
```
* If you want to create a container in detached mode, run:
```
sudo docker run -p 80:80 -p 1234:1234 -dit blockchain_9gag
```
* To join a detached container, get its ID by running:
```
sudo docker ps
```
Then run:
```
sudo docker attach [ID]
```

* To quit a container, press Ctrl+P and Ctrl+Q.
To quit and remove a container, press Ctrl+D.


## Delete the local Docker repo
* Run the following command to delete the build image:
```
sudo docker rmi blockchain_9gag
```
If the following error occur : (*Error response from daemon: conflict: unable to remove repository reference "blockchain_9gag" (must force) - container [xxxxxxxxxxxx] is using its referenced image yyyyyyyyyyyy*),
remove your running containers (this action cannot be undone!):
```
sudo docker rm xxxxxxxxxxxx
```

* Clean old build images :
```
sudo docker system prune
```


## Utilisation de l'interface web
* Lancez un conteneur docker pour démarrer votre propre noeud sur la blockchain.
* L'interface web est accessible sur [localhost](127.0.0.1)
* Pour créer une nouvelle chaîne, utilisez le menu déroulant *Chain* et sélectionnez *Create chain*. Pour rejoindre une chaîne existante, sélectionnez *Connect*.
* Une fois connecté à une chaîne, il devient possible de poster du contenu et de voir celui des autres directement sur la page d'accueil.
* Le menu déroulant *Group* permet de gérer les groupes et les posts de groupes. Un post de groupe est un post chiffré sur la blockchain déchiffrable uniquement par les membres dudit groupe.
Pour créer un groupe, utilisez l'option *Create*. Pour rejoindre un groupe avec l'option *Join*, il faut au préalable avoir été invité par un membre du groupe avec l'option *Invite*. Il devient ensuite possible de faire des posts de groupes chiffrés via l'option *Post* du menu déroulant *Groups*.
