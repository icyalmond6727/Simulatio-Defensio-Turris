class EventBus:
    """
    Central hub for the Observer Pattern.
    Allows systems to subscribe to events and other systems to emit them, 
    decoupling publishers from subscribers.
    """
    
    def __init__(self):
        """
        Initializes the dictionary mapping event types to lists of callback functions.
        """
        self.listeners = {}

    def subscribe(self, event_type, listener):
        """
        Registers a callback function to a specific event type.
        
        Args:
            event_type (str): The name of the event to listen for.
            listener (callable): The function to execute when the event occurs.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
            
        self.listeners[event_type].append(listener)

    def emit(self, event_type, *args, **kwargs):
        """
        Triggers all callback functions registered to the given event type.
        
        Args:
            event_type (str): The name of the event being triggered.
            *args, **kwargs: Additional arguments to pass to the listeners.
        """
        if event_type in self.listeners:
            # Iterating over a copy of the list to prevent modification issues during execution
            for listener in list(self.listeners[event_type]):
                listener(*args, **kwargs)