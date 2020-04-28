# API dealing with facts about cats

The project is based on python flask package for API, Cassandra for database and hosted in Kubernetes cluster on AWS VM. The web app provides complete CRUD operations on the 240 records from an external API [cat-facts](https://alexwohlbruck.github.io/cat-facts/docs/).


## Main features

1. REST API with encryption enabled.
2. Communicate to an external REST API.
3. Support of external Cloud database (cassandra database).
4. Support for cloud scalability by containerising the application.
5. Implementation of security by adding HTTPS support.


#### GET Method:
The home page gives details of queries that could be used to interact with the API.
```
https://ec2-54-161-101-189.compute-1.amazonaws.com
```  

To get all records from the database.
```
https://ec2-54-161-101-189.compute-1.amazonaws.com/facts     
```

To access data from the external API in the browser, run the command
```
https://ec2-54-161-101-189.compute-1.amazonaws.com/facts/external`
```

#### POST Method:
To insert new record in the database, run the command like
```
curl -i -k -H "Content-Type: application/json" -X POST -d '{"id":245,"fact":"cats are cute","type":"cat","first_name":"first","last_name":"last","upvotes":10}' https://ec2-54-161-101-189.compute-1.amazonaws.com/facts/
```
On successful entry of record, user will get a response
```
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.3
Date: Mon, 27 Apr 2020 14:53:46 GMT

{
  "message": "created: /facts/245"
}
```

#### UPDATE Method:
To update an existing record in the database, run a command like
```
curl -i -k -H "Content-Type: application/json" -X PUT -d '{"id":245, "upvotes":30}' https://ec2-54-161-101-189.compute-1.amazonaws.com/facts/
```
On successful update, user will get a response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.3
Date: Mon, 27 Apr 2020 14:57:19 GMT

{
  "message": "updated: /facts/245"
}
```

#### DELETE Method:
To delete a record from the database, use the command
```
curl -i -k -H "Content-Type: application/json" -X DELETE -d '{"id":245}' https://ec2-54-161-101-189.compute-1.amazonaws.com/facts/
```
On successful deletion of record, the user will get a response
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 39
Server: Werkzeug/0.14.1 Python/3.7.3
Date: Mon, 27 Apr 2020 14:58:24 GMT

{
  "message": "deleted: /facts/245"
}
```


### Data from External API:
All contents of the app are in getdata directory in the project repo.      
1. For external api call, I created web app called get_data.py      
2. It can be run from terminal by running the command
```
cd getdata
python get_data.py
```
3. After running go to the URL
```
http://ec2-54-161-101-189.compute-1.amazonaws.com:8080/facts/      
```
4. This will show the contents from cat facts url on webpage and download it to a `json` file namely `facts.json`.     

5. I converted the json file to csv and simplified the column names i.e. removed spaces and making column name short.      


### Local Docker Registry:
I setup my own registry on local machine first we need microk8s installed.

1. Install the microk8s
```
sudo snap install microk8s --classic
```

5. Now start the microk8s Server
```
microk8s.start
```
6. Enable DNS to enable communication between different containers and pods
```
microk8s.enable dns
```
7. Now to setup registry at `localhost:32000` where we can push and pull images from. [Reference](https://itnext.io/microk8s-docker-registry-c3f401faa760).
```
microk8s.enable registry
```
8. Check the status
```
microk8s.status
microk8s.kubectl describe node
microk8s.ctr image list
```



### Setup of CASSANDRA Database:

1. Install Docker
```
apt install docker.io -y
```

2. Get latest cassandra for base image
```
docker pull cassandra:latest
```

3. Run the container by command
```
sudo docker run --name cassandra -p 9042:9042 -d cassandra:latest
```

4. To copy csv file in to cassandra database in the container, run the command
```
cd getdata
docker cp facts.csv cassandra:/home/facts.csv
```

5. To get the cassandra shell in container, run
```
docker exec -it cassandra cqlsh
```

6. To create database by the name facts. run
```
CREATE KEYSPACE facts WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
```

7. To create table in that database. run
```
CREATE TABLE facts.data (id text PRIMARY KEY, fact text, , type text, first_name text, last_name text, upvotes int);
```

8. To copy data into the newly created table. run
```
COPY facts.data (id, fact, type, first_name, last_name, upvotes) FROM '/home/facts.csv' WITH DELIMITER=',' AND HEADER=TRUE;
```

9. To check if the data is properly copied. run
```
Select * From facts.data;
```

10. To come out of the container, run
```
quit
```





### Building a cassandra docker image:
After doing the settings we need to make an image of cassandra. To do this first we need to make local registry.


1. First get the name of the container by running
```
docker ps -a
```

2. To save changes and make a new image by the name `localhost:32000/cassandra:v1`
```
docker commit cassandra localhost:32000/cassandra:v1
```

3. To check if the image is created, run
```
docker images
```

4. Now compress the newly created image
```
docker save localhost:32000/cassandra:v1 > ~/cassandra.tar
```

5. To copy my image into the registry
```
microk8s.ctr image import ~/cassandra.tar
```

### To implement https access

```
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

The command has the following output. On successful execution it will generate two files certificate (cert.pem) and key (key.pem). We can add them to our webapp directory and mention them in the `app.py` to add ssl feature. We also need to change the port from 8080 to 443 as https works on port 443.
```
Generating a 4096 bit RSA private key
...................................................................................................................++
..........................................................................................................................................................................................................................................................++
writing new private key to 'key.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) []:UK
State or Province Name (full name) []:London
Locality Name (eg, city) []:London
Organization Name (eg, company) []:QMUL
Organizational Unit Name (eg, section) []:computer science 
Common Name (eg, fully qualified host name) []:ec2-54-161-101-189.compute-1.amazonaws.com
Email Address []:ec18359@qmul.ac.uk
```


### Deployment of Application in Kubernetes:

We need to create a  cassandra-deployment.yaml file to specify all the settings and
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cassandra-deployment
  labels:
    app: app
spec:
  selector:
    matchLabels:
      app: app
  replicas: 2
  template:
    metadata:
      labels:
        app: app
    spec:
      containers:
      - name: app
        image: localhost:32000/cassandra:v1
        ports:
        - containerPort: 447
```

1. Now to deploy the image in Kubernetes
```
sudo microk8s.kubectl apply -f ./cassandra-deployment.yaml  
```
2. You can check the deployment by command
```
sudo microk8s.kubectl get deployment. Wait for sometime to start deployment.
```
3. The output is
```
NAME                   READY   UP-TO-DATE   AVAILABLE   AGE
cassandra-deployment   2/2     2            2           3m46s
```

4. To check the number of pods, run
```
microk8s.kubectl get pods
```
5. The output is
```
NAME                                    READY   STATUS    RESTARTS   AGE
cassandra-deployment-69bf5c75cc-c8kck   1/1     Running   0          5m29s
cassandra-deployment-69bf5c75cc-w2pkw   1/1     Running   0          5m30s
```


To create a service for external access
```
sudo microk8s kubectl expose deployment cassandra-deployment --type=LoadBalancer --port=443 --target-port=443
```

To check the services
```
sudo microk8s.kubectl get services
```
Th output is
```
NAME                   TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)         AGE
cassandra-deployment   LoadBalancer   10.152.183.4   <pending>     443:32519/TCP   5m42s
kubernetes             ClusterIP      10.152.183.1   <none>        443/TCP         94m
```


<!-- ### WEB APPLICATION:
All contents of web app are in the directory webapp directory in the project repo.

1. Web app created to run on port 443
2. Docker file added to run the app in container
3. Requirements.txt added to the repo containing web app dependencies
4. To make the image run the command
```
cd webapp
docker build . -t localhost:32000/myapp:v1
```
5. To check the created container run command
```
docker images
```
6. Now I will save the newly created image in .tar compressed file.
```
docker save localhost:32000/myapp:v1 > ~/myimage.tar
```
7. To copy the image to Registry
```
microk8s.ctr image import ~/myimage.tar
```

Now create a pod node-pod.yaml
```

apiVersion: v1
kind: Pod
metadata:
        name: api-pod
        labels:
                name: app
spec:
        containers:
                - name: app
                  image: localhost:32000/myapp:v1
                  ports:
                          - containerPort: 443

```

8. Now run this command to make a pod
```
microk8s.kubectl apply -f node-pod.yaml
```

9. To check all resources
```
microk8s.kubectl get all --all-namespaces
```

10. Now check the app by going to `https://0.0.0.0` in browser. -->










### Cleaning the setup:

27. To delete the setup
```
sudo microk8s.kubectl delete deployment cassandra-deployment
sudo microk8s.kubectl delete service/cassandra-deployment
```
<!-- sudo microk8s.kubectl delete pod/api-pod -->
