# Class publisher that should handle the addition and calling of various
class Publisher:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, subscriber):
        self.subscribers.append(subscriber)

    def publish(self, message):
        for subscriber in self.subscribers:
            subscriber.receive(message)