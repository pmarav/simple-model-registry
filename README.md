# Installation
Install Docker following: https://docs.docker.com/engine/install/
```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```
Clone the repository

# Usage
To start the server and the database run the following:
```bash
git clone https://github.com/pmarav/simple-model-registry.git
cd simple-model-registry
docker compose up --build
```

# API
The API which was developed using fastapi can be tested from the Swagger UI by visiting http://127.0.0.1:8000/docs

![image](https://github.com/user-attachments/assets/c2aa165f-42e6-47db-8e79-a1f9f4e0fe3e)

## /models POST endpoint
![image](https://github.com/user-attachments/assets/adae36bf-14b5-40cd-b842-061d37f7421d)

The server stores uploaded files in the /var/lib/models directory. To ensure data persistence even if the container is removed or restarted, an external volume is used.
The metadata is stored in the postgresql database.

![image](https://github.com/user-attachments/assets/8fe5447f-bded-45b3-8217-19ca49eaa919)

## /models GET endpoint
A GET request to this endpoint returns a list of dictionaries, where each dictionary contains the metadata of an uploaded pickle file.

![image](https://github.com/user-attachments/assets/d2ae9e37-d832-4236-8949-69c765da9a88)

## /models/{name} GET endpoint
This endpoint returns a json which contains the metadata of the endpoint named {name}.

![image](https://github.com/user-attachments/assets/f10a8523-d080-46ad-a627-25e9202cc62d)

# Database
PostgreSQL is used for storing the metadata of the uploaded models. More specifically, the Dockerfile creates a database called "modelmetadata" and a table called "models". Furthermore, a user "psqluser" has been created to be used by the application. Finally, an external volume is also used for the database to achieve persistence even if the container is removed or restarted. To view the contents of the database run the following (The password for the psqluser user is "psqluser123!" and can also be found in the .env file which has been left in the repository for testing purposes):

```bash
sudo apt install postgresql -y
psql -U psqluser -h localhost -d modelmetadata # Use the password "psqluser123!" when prompted.
\dt
select * from models;
```
![image](https://github.com/user-attachments/assets/91f13b21-ae47-465f-9393-a3c0b7d179c8)












