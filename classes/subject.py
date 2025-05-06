class Subject:
    def __init__(self, state={}):
        self._observers = []
        self._state = state

    def subscribe(self, observer):
        self._observers.append(observer)
    
    def unsubscribe(self, observer):
        self._observers.append(observer)
    
    def notify(self):
        for obs in self._observers:
            obs.update(self._state)

    def set_state(self, new_state):
        self._state = new_state
        self.notify()    

    def get_state(self):
        return self._state