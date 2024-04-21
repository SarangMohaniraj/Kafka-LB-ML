import json

def get_cluster_properties(properties_path="config/cluster-properties.json"):
    with open(properties_path) as f:
        cluster_properties = json.load(f)
        return cluster_properties
    
def update_cluster_properties(new_cluster_properties, properties_path="config/cluster-properties.json"):
    with open(properties_path, 'w') as f:
        json.dump(new_cluster_properties, f)