import pika # type: ignore
import pika.exceptions # type: ignore

rabbitmq_host = "localhost"

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    print(f"Connected to RabbitMQ")
    connection.close()
except pika.exceptions.AMQPConnectionError as e:
    print(f"Failed to Connect to RabbitMQ: {e}")