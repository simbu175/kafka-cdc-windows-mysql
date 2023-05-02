import json
import time
import pandas
from kafka import KafkaConsumer
from kafka import KafkaProducer
from kafka import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.errors import KafkaError
import configparser
from config import py_config
from mysql import db_wrapper

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

kafka_config_file = py_config.kafka_config
kafka_con = configparser.ConfigParser()
kafka_con.read(kafka_config_file)
kafka_bootstrap_servers = kafka_con.get('kafka', 'bootstrap_servers')
kafka_broker_id = kafka_con.get('kafka', 'broker.id')
kafka_num_network_threads = kafka_con.get('kafka', 'num.network.threads')
kafka_num_io_threads = kafka_con.get('kafka', 'num.io.threads')
kafka_socket_send_buffer_bytes = kafka_con.get('kafka', 'socket.send.buffer.bytes')
kafka_socket_receive_buffer_bytes = \
    kafka_con.get('kafka', 'socket.receive.buffer.bytes')
kafka_socket_request_max_bytes = kafka_con.get('kafka', 'socket.request.max.bytes')
kafka_log_dirs = kafka_con.get('kafka', 'log.dirs')
kafka_num_partitions = kafka_con.get('kafka', 'num.partitions')
kafka_num_recovery_threads_per_data_dir = \
    kafka_con.get('kafka', 'num.recovery.threads.per.data.dir')
kafka_offsets_topic_replication_factor = \
    kafka_con.get('kafka', 'offsets.topic.replication.factor')
kafka_transaction_state_log_replication_factor = \
    kafka_con.get('kafka', 'transaction.state.log.replication.factor')
kafka_transaction_state_log_min_isr = \
    kafka_con.get('kafka', 'transaction.state.log.min.isr')
kafka_log_retention_hours = kafka_con.get('kafka', 'log.retention.hours')
kafka_log_retention_check_interval_ms = \
    kafka_con.get('kafka', 'log.retention.check.interval.ms')
kafka_zookeeper_connect = kafka_con.get('kafka', 'zookeeper.connect')
kafka_zookeeper_connection_timeout_ms = \
    kafka_con.get('kafka', 'zookeeper.connection.timeout.ms')
kafka_group_initial_rebalance_delay_ms = \
    kafka_con.get('kafka', 'group.initial.rebalance.delay.ms')

msg_bytes = b'raw_byes'
msg_str = msg_bytes.decode('utf-8')
msg_dict = {'message': msg_str}
msg_json = json.dumps(msg_dict)

producer = KafkaProducer(
    bootstrap_servers=[kafka_bootstrap_servers],
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Asynchronous by default
future = producer.send(py_config.database_kafka_topic, msg_json.encode('utf-8'))

try:
    record_metadata = future.get(timeout=10)
except KafkaError as e:
    # Decide what to do if produce request failed...
    print(e)

# Successful result returns assigned partition and offset
print(record_metadata.topic)
print(record_metadata.partition)
print(record_metadata.offset)

consumer = KafkaConsumer(
    py_config.database_kafka_topic,
    bootstrap_servers=[kafka_bootstrap_servers],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=py_config.kafka_group_id,
    value_deserializer=lambda x: json.loads(x.decode('utf-8')))

consumer.subscribe([py_config.database_kafka_topic])

for message in consumer:
    message_data = message.value
    # process the message_data as per your requirement

# Create a Kafka admin client
admin_client = KafkaAdminClient(bootstrap_servers='localhost:9092')
#
topic_config = {
    'cleanup.policy': 'delete',
    'compression.type': 'gzip',
    'retention.ms': '86400000',
    'segment.bytes': '1073741824'
}

# Create a new Kafka topic
new_topic = NewTopic(name='my-topic', num_partitions=3, replication_factor=1, config=topic_config)
admin_client.create_topics(new_topics=[new_topic])

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
