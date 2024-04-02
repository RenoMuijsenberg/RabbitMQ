import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test', exchange_type='fanout')

for i in range(1000):
    message = f"Hello World! {i}"
    channel.basic_publish(exchange='test', routing_key='', body=message)
    print(f" [x] Sent {message}")

connection.close()
