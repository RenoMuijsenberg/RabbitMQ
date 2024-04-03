import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)

for i in range(100):
    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=f"Hello World! {i}",
        properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))

connection.close()
