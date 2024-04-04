import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test', exchange_type='fanout')


message = input("Enter question: ")
channel.basic_publish(exchange='test', routing_key='', body=message)
print(f" [x] Sent: {message}")

connection.close()
