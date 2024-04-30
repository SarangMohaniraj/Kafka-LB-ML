# Kafka-LB-ML

This project implements intelligent load balancing for Apache Kafka clusters using machine learning techniques to optimize resource allocation and throughput. It dynamically adjusts Kafka configurations and partitions based on real-time metrics and predictive analytics. The system enhances cluster performance and reliability by automating the scaling and management of Kafka brokers and topics. Machine learning models predict load fluctuations, enabling proactive adjustments. This approach ensures high availability and efficient processing of large data streams across distributed environments.

# Kafka Metrics Monitoring

| Metric Name                        | MBean Path                                                        | Description                                                             | Importance                                       |
|------------------------------------|-------------------------------------------------------------------|-------------------------------------------------------------------------|--------------------------------------------------|
| **JVM Memory Usage**               | `java.lang:type=Memory`                                           | Reports on heap and non-heap memory usage of the JVM.                   | Critical for ensuring efficient memory management and avoiding memory-related issues. |
| **CPU Usage**                      | `java.lang:type=OperatingSystem`                                  | Measures the CPU load caused by the Kafka process.                      | Essential for monitoring the impact of Kafka on system resources and overall performance. |
| **Total Time for Requests**        | `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=Produce` + `kafka.network:type=RequestMetrics,name=TotalTimeMs,request=FetchConsumer` | Combined processing time for produce and fetch requests, reflecting operational efficiency. | Important for assessing and optimizing request handling performance. |
| **Messages Per Second**            | `kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec`      | Tracks the rate at which messages are processed, indicating throughput. | Key for understanding and managing cluster throughput and performance. |

This table focuses on the most crucial metrics for monitoring Kafka's performance through JMX. These metrics help in managing Kafka's memory usage, CPU impact, operational efficiency, and throughput, ensuring the cluster operates at optimal levels.

# Machine Learning for Dynamic Load Balancing in Kafka Clusters

This application uses machine learning techniques to dynamically balance loads across Kafka clusters. It specifically utilizes a Random Forest classifier to predict the load state of Kafka nodes based on real-time CPU and memory usage metrics. The data for these metrics is fetched using Google BigQuery from a large dataset that mimics a typical Kafka cluster environment. The Random Forest model is trained to categorize the load into three states: under-loaded, optimally loaded, and over-loaded, which allows for proactive resource management and rebalancing decisions. The model's performance is evaluated through accuracy metrics, demonstrating its effectiveness in predicting the operational state of Kafka nodes.

# Local setup
1. Setup Kafka cluser
   ```
   docker compose up -d
   ```
2. Create virtualenv
   ```
   virtualenv env
   ```
3. Activate virtualenv
   ```
   source env/bin/activate
   ```
4. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
5. Start the dynamic load balancing scheduler
   ```
   python dynamic_lb_scheduler.py
   ```

# Evaluation
The OpenMessaging Benchmark Framework rigorously tests throughput and performance to ensure the system's effectiveness under various operational conditions. To evaluate how intelligent load balancing compares to a traditional Kafka cluster, we analyze the performance of a standard Kafka cluster against that of a Kafka cluster enhanced with intelligent load balancing.
1. Clone the OpenMessaging benchmark repository:
   ```
   git clone https://github.com/openmessaging/openmessaging-benchmark
   ```

2. Analyze the performance of the base Kafka cluster using the workload of your choice:
   ```
   sudo bin/benchmark --drivers driver-kafka/kafka-throughput.yaml workloads/100-topic-1kb-4p-4c-500k.yaml
   ```
   Rename the generated report file as `baseline-report.json`

3. Start the Kafka Cluster integrated with intelligent load balancing by following the instructions in the Local Setup:

4. Analyze the performance of the Kafka cluster integrated with our model:
   ```
   sudo bin/benchmark --drivers driver-kafka/kafka-throughput.yaml workloads/100-topic-1kb-4p-4c-500k.yaml
   ```
   Rename the generated report file as `ml-report.json`

5. Compare the reports by generating charts with the following command:
   ```
   python bin/create_charts.py baseline-report.json ml-report.json
   ```
