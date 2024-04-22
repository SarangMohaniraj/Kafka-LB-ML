import docker

def reassign_partitions(topic_names, broker_ids, broker_main_server):
    client = docker.from_env()
    container_name_or_id = f'kafka{broker_ids[0]}'
    script_path = "/kafka_lb/partition_reassign.sh"
    script_args = f'{topic_names} {broker_ids} {broker_main_server}'
    full_command = f'{script_path} {script_args}'
    try:
        container = client.containers.get(container_name_or_id)
        exit_code, output = container.exec_run(cmd=full_command, demux=True)
        if exit_code == 0:
            if output[0]:
                print(f"Script Output:\n{output[0].decode('utf-8')}")
            if  output[1]:
                print(f"Script Output Err :\n{output[1].decode('utf-8')}")
        else:
            print(f"Script failed with exit code {exit_code} output: {output}")
    except docker.errors.NotFound:
        print(f"Container '{container_name_or_id}' not found.")
    except docker.errors.APIError as e:
        print(f"Error executing script in container: {e}")

if __name__ == "__main__":
    reassign_partitions("topic1,topic2", "1,2,3", "localhost:9092")
