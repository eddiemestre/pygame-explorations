# Event class, may be used at some point... TBD

class EventChannel:
    def __init__(self):
        self.subscribers = {}
    
    def addEvent(self, event):
        if event not in self.subscribers:
            self.subscribers[event] = []
        else:
            raise ValueError("Event already in Event Channel")
    
    def subscribe(self, event, subscriber):
        if event in self.subscribers:
            if subscriber not in self.subscribers[event]:
                self.subscribers[event].append(subscriber)
            else:
                raise ValueError(f"{subscriber} already subscribed to {event}")
        else:
            self.addEvent(event)
            self.subscribe(event, subscriber)
    
    def unsubscribe(self, event, unsubscriber):
        if event in self.subscribers:
            if unsubscriber in self.subscribers[event]:
                self.subscribers[event].remove(unsubscriber)
            else:
                raise ValueError(f"{unsubscriber} not subscribed to {event}")
    
    def publish(self, event):
        if event in self.subscribers:
            for sub in self.subscribers[event]:
                print(f'publishing {event} for entity {sub}')
                sub.update(event)
        else:
            raise ValueError(f"{event} is not in EventChannel")

class TestEntity:
    def __init__(self, name=None):
        self.name = name
        self.attack = 1
    
    def update(self, event):
        if event == 'updateName':
            print('updating Name')
            self.name = "Charlie"
        if event == 'updateAttack':
            print('updating Attack')
            self.attack += 1
            
        # what will eventually happen is update looks at the game data, sees which
        # attributes for this Entity that need to be updated, and tries to update
        # them. if an attribute doesn't exist. It throws an error. 
            