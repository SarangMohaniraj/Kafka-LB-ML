import schedule
import time
from dynamic_lb import dynamic_load_balancing, predict_load_state_by_kafka_metrics

def job():
    print("I'm alive...")

load_state_historical_data = []

def load_balancing():
    global load_state_historical_data
    load_state_historical_data.append(predict_load_state_by_kafka_metrics())
    if len(load_state_historical_data)>5:
        load_state = max(load_state_historical_data,key=load_state_historical_data.count)
        dynamic_load_balancing(load_state=load_state)
        load_state_historical_data = []

schedule.every(10).seconds.do(job)
schedule.every(10).seconds.do(load_balancing)

# schedule.every(10).seconds.do(job_with_argument, name="Peter")

while True:
    schedule.run_pending()
    time.sleep(1)