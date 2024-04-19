from metrics import get_kafka_metrics

def dynamic_load_balancing():
   kafka_metrics = get_kafka_metrics("example_topic")
   print("kafka_metrics", kafka_metrics)

dynamic_load_balancing()