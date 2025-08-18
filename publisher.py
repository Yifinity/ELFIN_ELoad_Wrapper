class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message, data):
        for subscriber in self.subscribers:
            subscriber.receive(message, data)
