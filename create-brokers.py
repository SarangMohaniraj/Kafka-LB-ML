import docker
import json


def get_cluster_properties(properties_path="config/cluster-properties.json"):
    with open(properties_path) as f:
        cluster_properties = json.load(f)
        return cluster_properties


def get_new_broker_config():
    cluster_properties = get_cluster_properties()
    zookeeper_connect = ",".join(cluster_properties["zookeeper_servers"])
    new_broker_id = (
        max([int(broker["id"]) for broker in cluster_properties["brokers"]]) + 1
    )
    new_port = (
        max([int(broker["port"]) for broker in cluster_properties["brokers"]]) + 1
    )
    replication_factor = 1
    print("new_port", new_port)
    return {
        "zookeeper_connect": zookeeper_connect,
        "new_broker_id": new_broker_id,
        "new_port": new_port,
        "replication_factor": replication_factor,
    }


def get_kafka_advertised_listeners(new_broker_id, new_port):
    return (
        "INTERNAL://kafka"
        + str(new_broker_id)
        + ":1"
        + str(new_port)
        + ",EXTERNAL://localhost:"
        + str(new_port)
        + ",DOCKER://host.docker.internal:2"
        + str(new_port)
    )


def create_kafka_broker(broker_config, network_name):
    client = docker.from_env()
    zookeeper_connect = broker_config["zookeeper_connect"]
    new_broker_id = broker_config["new_broker_id"]
    new_port = broker_config["new_port"]
    replication_factor = broker_config["replication_factor"]
    print("new_port", new_port)
    kafka_advertised_listeners = get_kafka_advertised_listeners(new_broker_id, new_port)
    print("kafka_advertised_listeners", kafka_advertised_listeners)

    # Environment configuration for the new Kafka broker
    environment = {
        "KAFKA_BROKER_ID": str(new_broker_id),
        "KAFKA_ZOOKEEPER_CONNECT": zookeeper_connect,
        "KAFKA_ADVERTISED_LISTENERS": kafka_advertised_listeners,
        "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": str(replication_factor),
        "KAFKA_LISTENER_SECURITY_PROTOCOL_MAP": "INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT",
        "KAFKA_INTER_BROKER_LISTENER_NAME": "INTERNAL",
        "KAFKA_LOG4J_LOGGERS": "kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO",
        "KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR": 1,
        "KAFKA_TRANSACTION_STATE_LOG_REPLICATION_FACTOR": 1,
        "KAFKA_TRANSACTION_STATE_LOG_MIN_ISR": 1,
        "KAFKA_JMX_PORT": 9999,
        "KAFKA_JMX_HOSTNAME": "${DOCKER_HOST_IP:-127.0.0.1}",
        "KAFKA_AUTHORIZER_CLASS_NAME": "kafka.security.authorizer.AclAuthorizer",
        "KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND": "true",
    }

    # Adjust the port mapping based on your requirements
    port_mapping = {f"{new_port}": f"{new_port}", f"2{new_port}": f"2{new_port}"}

    # Create and start the Kafka broker container
    container = client.containers.create(
        image="confluentinc/cp-kafka:7.3.2",
        environment=environment,
        ports=port_mapping,
        detach=True,
        name=f"kafka{new_broker_id}",
    )

    network = client.networks.get(network_name)
    network.connect(container, aliases=[f"kafka_{new_broker_id}"])
    container.start()

    print(f"Broker {new_broker_id} started, accessible on localhost:{new_port}")


broker_config = get_new_broker_config()
# Example: Create and start an additional broker
create_kafka_broker(broker_config, network_name="dynamic-lb-kafka_default")
