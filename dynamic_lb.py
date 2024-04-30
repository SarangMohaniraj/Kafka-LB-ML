from metrics import get_kafka_metrics
from load_predict import predict_load_state
from cluster_props_handler import get_cluster_properties, update_cluster_properties
from create_brokers import create_kafka_broker
from reasssign import reassign_partitions
from confluent_kafka.admin import AdminClient

def predict_load_state_by_kafka_metrics():
   kafka_metrics = get_kafka_metrics()
   load_state = predict_load_state(kafka_metrics)
   return load_state

def dynamic_load_balancing(load_state):
   match load_state:
      case 'under-loaded':
         print("Under loaded, keep monitoring")
      case 'optimally loaded':
         print("optimally loaded, keep monitoring")
      case'over-loaded':
         # Create additional broker to handle the load
         properties_path = "config/cluster-properties.json"
         cluster_properties = get_cluster_properties(properties_path)
         new_cluster_properties = create_kafka_broker(cluster_properties, network_name="dynamic-lb-kafka_default")
         update_cluster_properties(new_cluster_properties)

         # Reassign the partitions
         topic_names = get_kafka_topics(new_cluster_properties)
         broker_ids = ",".join([str(broker["id"]) for broker in new_cluster_properties["brokers"]])
         reassign_partitions(",".join(topic_names[:10]), broker_ids, new_cluster_properties["brokers_servers"][0])

def get_kafka_topics(cluster_properties):
   bootstrap_servers = ",".join(cluster_properties["brokers_servers"])
   admin_client = AdminClient({'bootstrap.servers': bootstrap_servers})
   topic_names = []
   topics = admin_client.list_topics().topics
   for topic in topics:
      topic_names.append(topic)
   return topic_names