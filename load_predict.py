import os
import joblib
import pandas as pd

def load_model(load_path):
    try:
        model = joblib.load(load_path)
        print(f"Model loaded from {load_path}")
        return model
    except Exception as e:
        print(e)

def create_dataframe(data):
    data = {
        'cpu_usage': float(data["java.lang:type=OperatingSystem"]["ProcessCpuLoad"]),
        'memory_usage' : float(data["java.lang:type=Memory"]["HeapMemoryUsage"]["used"]) ,
        'time_duration': (float(data["kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce"]["Count"])+ float(data["kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer"]["Count"]))/1000, #time is in ms
        'memory_accesses_per_instruction': float(data["kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec"]["Count"])
        }
    dataframe = pd.DataFrame(data, index=[0])
    return dataframe

def predict_load_state(data, datadir ="./"):
    #Loading the saved model
    model = load_model(load_path = f'{datadir}trained_model.pkl')
    dataframe =create_dataframe(data)
    prediction = model.predict(dataframe)
    print(f"prediction {prediction}")
    return prediction