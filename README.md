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
sudo docker run -it blockchain_9gag
```
* If you want to create a container in detached mode, run:
```
sudo docker run -dit blockchain_9gag
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
