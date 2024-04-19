from metrics import get_kafka_metrics
from load_predict import predict_load_state

def dynamic_load_balancing():
   kafka_metrics = get_kafka_metrics("example_topic")
   print("kafka_metrics", kafka_metrics)
   load_state = predict_load_state(kafka_metrics)
   print("load_state", load_state)

dynamic_load_balancing()
