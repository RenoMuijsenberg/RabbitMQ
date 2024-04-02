import os
import pika
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='test', exchange_type='fanout')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

channel.queue_bind(exchange='test', queue=queue_name)

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def filter_work(message):
    filter_message = [
        {
            "role": "system",
            "content": """You are a used as a filtering system, if the question is not about world war 2,
                       you should return 'false' if it is about world war 2, return 'true'. No Yapping!"""

        },
        {
            "role": "user",
            "content": message.decode()
        }
    ]

    filter_response = client.chat.completions.create(
        messages=filter_message,
        model="gpt-3.5-turbo"
    )

    return filter_response.choices[0].message.content


def worker_work(message):
    worker_message = [
        {
            "role": "system",
            "content": """You are used as a worker in a pub/sub system. Your only job is to answer questions about 
            world war 2. First give your answer back in plain text."""
        },
        {
            "role": "user",
            "content": message.decode()
        }
    ]

    worker_response = client.chat.completions.create(
        messages=worker_message,
        model="gpt-3.5-turbo"
    )

    return worker_response.choices[0].message.content


def callback(ch, method, properties, body):
    filter_result = filter_work(body)

    if filter_result == "true":
        print(worker_work(body))
    else:
        print("Question is not about world war 2, ignoring...")


print(' [*] Waiting for logs. To exit press CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
