class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message, data):
        for subscriber in self.subscribers:
            subscriber.receive(message, data)
class Subscriber:
    def __init__(self, name):
        self.name = name

    def receive(self, message):
        print(f"{self.name}"+"received message:"
              +f"{message}")

# publisher = Publisher()

# subscriber_1 = Subscriber("Subscriber 1")
# subscriber_2 = Subscriber("Subscriber 2")

# publisher.subscribe(subscriber_1)
# publisher.subscribe(subscriber_2)

# publisher.publish("Hello World")