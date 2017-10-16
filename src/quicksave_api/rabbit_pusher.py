# This file is a part of quicksave project.
# Copyright (c) 2017 Aleksander Gajewski <adiog@quicksave.io>.

import pika

import quicksave_api.env


class RabbitPusher(object):
    def __enter__(self):
        connection_parameters = pika.ConnectionParameters(host=quicksave_api.env.IO_QUICKSAVE_MQ_HOST,
                                                          port=quicksave_api.env.IO_QUICKSAVE_MQ_PORT)
        self.connection = pika.BlockingConnection(connection_parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=quicksave_api.env.REQUEST_QUEUE)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def push(self, bean):
        self.channel.basic_publish(exchange='',
                                   routing_key=quicksave_api.env.REQUEST_QUEUE,
                                   body=bean.to_string().encode())
