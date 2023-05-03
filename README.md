# kafka-cdc-windows-mysql
<ins>**Assumptions**</ins>:
1. The steps are advised for a Windows instance
2. MySQL client (can be downloaded from [this](https://dev.mysql.com/downloads/mysql/) link) is installed on the machine and the connection is established through `localhost`
3. All the MySQL database activities with respect to the setup of users & controls are available under mysql folder within the project
4. [Kafka](https://kafka.apache.org/downloads) & [Debezium](https://debezium.io/documentation/reference/stable/install.html) python connectors for the required database (MySQL in this instance) are expected to be installed for this project to work (as part of the Pipfile execution)
5. `Kafka` services is expected to be up and running along with the `Zookeeper` services before we can ask from this code to connect to Kafka producers & consumers
6. Also, the `debezium` connector for mysql is in the running state to capture the CDC from MySQL `binlogs`
7. The mysql db password is stored as an environment variable (`os.environ`)

<ins>**Project overlays**</ins>:
1. This repo has the CDC events captured by Debezium from a windows hosted MySQL db through its binlog onto a kafka-topic. 
2. Then writing the output from the kafka-topic (tied to a specific db from mysql) to a flat file
3. It doesn't use any docker containers/images
4. Since it's done on a single node, this isn't for distributed processing of kafka messages