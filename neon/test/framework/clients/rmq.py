import threading

from kombu import Connection, Exchange, Queue


class RmqClient:

    conn: Connection

    def __init__(self, **kwargs):
        """Creates and stores the connection object in self.connection. As well as, it initializes 
        the channel and queue
        arguments:
            hostname: str = 'localhost', 
            userid: Any | None = None,
            password: Any | None = None,
            virtual_host: Any | None = None,
            port: Any | None = None,
            insist: bool = False,
            ssl: bool = False,
            transport: Any | None = None,
            connect_timeout: int = 5,
            transport_options: Any | None = None,
            login_method: Any | None = None,
            uri_prefix: Any | None = None,
            heartbeat: int = 0,
            failover_strategy: str = 'round-robin',
            alternates: Any | None = None,
            **kwargs: Any
        """
        self.conn = Connection(**kwargs)
        self.channel = None
        self.queue = {}

    def set_exchange(self, name, type='direct', durable=False, **kwargs):
        """Creates and stores the exchange object in self.exchange
        arguments:
            name (str),
            type (str),
            durable (bool),
            channel,
            auto_delete (bool),
            delivery_mode (enum):,
            arguments (Dict),
            no_declare (bool)
        """
        self.exchange = Exchange(name, type=type, durable=durable, **kwargs)

    def add_queue(self, name, routing_key=None, queue_arguments=None, **kwargs):
        """Creates and stores the queue object in self.queue dictionary along with the queue name
        arguments:
            name (str),
            routing_key (str),
            queue_arguments (Dict),
            exchange (Exchange, str),            
            channel,
            durable (bool),
            exclusive (bool),
            auto_delete (bool),            
            binding_arguments (Dict),
            consumer_arguments (Dict),
            no_declare (bool),
            on_declared (Callable),
            expires (float),
            message_ttl (float),
            max_length (int),
            max_length_bytes (int),
            max_priority (int)
        """
        self.queue[name] = Queue(name, exchange=self.exchange, routing_key=routing_key, queue_arguments=queue_arguments, **kwargs)

    def get_channel(self):
        """Initially, It checks whether the channe is created or not. If the channel is not created, 
        Creates and stores the channel object in self.channel
        """
        if self.conn.connection.connected:
            if not self.channel:
                self.channel = self.conn.channel()
                return self.channel

    def publish(self, queue_name=None, message=None, routing_key=None, headers=None, declare=None, **kwargs):
        """This method is used to publish the message to the exchange.        
        arguments:
            queue_name: Any | None = None,
            message: Any,            
            routing_key: Any | None = None,
            headers: Any | None = None,
            declare: Any | None = None,
            delivery_mode: Any | None = None,
            mandatory: bool = False,
            immediate: bool = False,
            priority: int = 0,
            content_type: Any | None = None,
            content_encoding: Any | None = None,
            serializer: Any | None = None,           
            compression: Any | None = None,
            exchange: Any | None = None,
            retry: bool = False,
            retry_policy: Any | None = None,            
            expiration: Any | None = None,
            timeout: Any | None = None,
            **properties: Any
        """
        if self.conn.connection.connected:
            exchange = self.exchange
            routing_key = routing_key or self.queue[queue_name].routing_key
            with self.conn.Producer() as producer:
                producer.publish(body=message,
                                 channel=self.get_channel(),
                                 exchange=exchange,
                                 routing_key=routing_key,
                                 headers=headers,
                                 declare=declare,
                                 **kwargs)

    def start_background_consumer(self, accept, process_media):
        """This method is used to initiate new thread for consumer
        arguments:
            accept: Any | None = None,
            process_media: call back method,
            **kwargs: Any
        """
        self.receiver_thread = threading.Thread(target=self.__background_consumer, args=(
            process_media,
            accept,
        ))
        self.receiver_thread.start()

    def __background_consumer(self, accept, process_media, **kwargs):
        """This method is used to consume the message from the queues in background        
        arguments:
            accept: Any | None = None,
            process_media: call back method,
            **kwargs: Any
        """
        while self.conn.connection.connected:
            channel = self.get_channel()
            queues = self.queue.values()
            with self.conn.Consumer(channel=channel, queues=list(queues), callbacks=[process_media], accept=[accept], **kwargs) as consumer:
                self.conn.drain_events()

    def single_consume(self, accept, process_media, **kwargs):
        """This method is used to consume the message from the queues.        
        arguments:
            accept: Any | None = None,
            process_media: call back method,
            **kwargs: Any
        """
        if self.conn.connection.connected:
            channel = self.get_channel()
            queues = self.queue.values()
            with self.conn.Consumer(channel=channel, queues=list(queues), callbacks=[process_media], accept=[accept], **kwargs) as consumer:
                self.conn.drain_events()

    def disconnect(self):
        """This method is to close the connection """
        if self.conn.connection.connected:
            self.conn.close()
