# API dealing with facts about cats

The project is based on python flask package for API, Cassandra for database and hosted in Kubernetes cluster on AWS VM. The web app provides complete CRUD operations on the 240 records from an external API [cat-facts](https://alexwohlbruck.github.io/cat-facts/docs/).


## Main features

1. REST API with encryption enabled.
2. Communicate to an external REST API.
3. Support of external Cloud database (cassandra database).
4. Support for cloud scalability by containerising the application.
5. Implementation of security by adding HTTPS support.


##### GET Method:
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

##### POST Method:
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

##### UPDATE Method:
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

##### DELETE Method:
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

<!-- ### WEB APPLICATION:
All contents of web app are in the directory webapp directory in the project repo.

1. Web app created to run on port 8080
2. Docker file added to run the app in container
3. Requirements.txt added to the repo containing web app dependencies
4. To make the image run the command `docker build -t myproject:v1 .`
5. To check the created container run command `docker images`
6. To run the image into a container, run the command `docker run -d -p 8080:8080 myproject:v1`
7. Now check the app by going to `http://0.0.0.0:8080` in browser. -->


### Data from External API:
All contents of the app are in getdata directory in the project repo.      
1. For external api call, I created web app called get_data.py      
2. It can be run from terminal by running the command
```
python get_data.py
```
3. After running go to the URL
```
http://ec2-54-161-101-189.compute-1.amazonaws.com/facts/      
```
4. This will show the contents from cat facts url on webpage and download it to a `json` file `facts.json`.     

5. I converted the json file to csv and simplified the column names i.e. removed spaces and making column name short.      

### LOCAL Docker registry:
I setup my own registry on local machine by command `microk8s.enable registry`. This setup the registry at `localhost:32000` where we can push and pull images. [Reference](https://itnext.io/microk8s-docker-registry-c3f401faa760).


### Setup of CASSANDRA Database:

1. Get latest cassandra for base image
```
docker pull cassandra:latest
```

2. Run the container by command
```
sudo docker run --name cassandra -p 9042:9042 -d cassandra:latest
```

3. To copy csv file in to cassandra database in the container, run the command
```
docker cp facts.csv cassandra:/home/facts.csv`
```

4. To get the cassandra shell in container, run
```
docker exec -it cassandra cqlsh
```

5. To create database by the name facts. run
```
CREATE KEYSPACE facts WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1};
```

6. To create table in that database. run
```
CREATE TABLE facts.data (id text PRIMARY KEY, fact text, , type text, first_name text, last_name text, upvotes int);
```

7. To copy data into the newly created table. run
```
COPY facts.data (id, fact, type, first_name, last_name, upvotes) FROM '/home/facts.csv' WITH DELIMITER=',' AND HEADER=TRUE;
```

8. To check if the data is properly copied. run
```
Select * From facts.data;
```

9. To come out of the container, run
```
quit()
```



<!--

10. To find all details about the cassandra, run
`kubectl describe svc cassandra`

11. Now run the web app container created in step 4 in kubernetes. run
`kubectl run myproject --image=nginx --port=80`

12. Now expose our cluster to external world requests
`kubectl expose deployment myproject --type=LoadBalancer`

13. To scale the cassandra cluster,
`kubectl scale rc cassandra --replicas=2`

14. To get more details, run command
`kubectl get pods` -->

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

### Building a cassandra docker image:
After doing the settings we need to make an image of cassandra. To do this first we need to make local registry.
1. Install the microk8s
```
sudo snap install microk8s --classic --channel=1.18/stable
```

2. Now enable the registry
```
sudo microk8s enable registry
```

3. Now build the docker image
```
sudo docker build . -t localhost:32000/cassandra:registry
```
4.
```
sudo docker push localhost:32000/cassandra:registry
```

### Deployment of Application in Kubernetes:

We need to create a  cassandra-deployment.yaml file to specify all the settings and
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cassandra-deployment
  labels:
    app: Coursework
spec:
  selector:
    matchLabels:
      app: Coursework
  replicas: 2
  template:
    metadata:
      labels:
        app: Coursework
    spec:
      containers:
      - name: coursework
        image: localhost:32000/mycassandra:registry
        ports:
        - containerPort: 80
```

Now to deploy the image in Kubernetes
```
sudo microk8s.kubectl apply -f ./cassandra-deployment.yaml  
```
You can check the deployment by command
```
sudo microk8s.kubectl get deployment
```
To create a service for external access
```
sudo microk8s kubectl expose deployment cassandra-deployment --type=LoadBalancer --port=443 --target-port=443
```



### Cleaning the setup:

27. To delete the setup
`sudo microk8s.kubectl delete deployment cassandra-deployment`
