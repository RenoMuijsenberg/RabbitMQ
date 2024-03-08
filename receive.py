import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")


channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages...')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    print(' [*] Exiting consumer...')
    connection.close()
