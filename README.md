# kafka-cdc-windows-mysql
Assumptions:
1. The steps are advised for a Windows machine
2. MySQL client is installed on the machine and the connection is established through `localhost`
3. All the users and passwords created are outside the scope of this activity
4. Kafka & Debezium python connectors are expected to be installed for this project to work
5. Kafka is expected to be up and running along with the Zookeeper services for this project to work 
6. Also the debezium connector for mysql is in the running state to capture the CDC from MySQL binlogs.

Project overlays:
1. This repo has the CDC events captured by Debezium from a windows hosted MySQL db through its binlog onto a kafka-topic. 
2. Then writing the output from the kafka-topic (tied to a specific db from mysql) to a flat file
3. It doesn't use any docker or containers but only the physical installation of the same
4. Since it's done on a single laptop (node) this isn't recommended for distributed processing of incoming messages (or scaling up/down the kafka brokers or topics as applicable)
