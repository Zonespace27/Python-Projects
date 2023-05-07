class SignalNode():
    
    def __init__(self, name: str) -> None:
        self.name = name
        # Equivalent to signal_procs
        self.event_callbacks = {}
        # Equivalent to comp_lookup
        self.object_lookup = {}
    
    def register_event(self, target, event_type, func_to_callback, override):
        try:
            target_callbacks = self.event_callbacks[target]

        except KeyError:
            target_callbacks = {}

        lookup = target.object_lookup
        if not lookup:
            lookup = {}

        if ((event_type in list(target_callbacks.keys())) and not override):
            print(f"{event_type} overriden, set override = True to suppress this warning.")
        
        target_callbacks[event_type] = func_to_callback
        self.event_callbacks[target] = target_callbacks
        # Equivalent to looked_up
        lookup_list: list = []
        try:
            lookup_list = lookup[event_type]

        except KeyError:
            lookup[event_type] = self

        if (lookup_list == self):
            return
        
        elif (not isinstance(lookup_list, list)):
            lookup[event_type] = [lookup_list, self]
            
        else:
            lookup_list.append(self)
        
        target.object_lookup = lookup
    
    def unregister_event(self, target, event_or_events):
        lookup: dict = target.object_lookup
        if not (self.event_callbacks or self.event_callbacks[target] or lookup):
            return

        if not isinstance(event_or_events, list):
            event_or_events = [event_or_events]

        for event in event_or_events:
            if not self.event_callbacks[target][event]:
                continue

            if isinstance(lookup[event], list):
                lookup_event_len = len(lookup[event])



                if lookup_event_len == 2:
                    lookup[event] = (lookup[event] - self)[0]
                
                elif lookup_event_len == 1:
                    if not (self in lookup[event]):
                        continue
                    
                    lookup.pop(event)
                    if not len(lookup):
                        target.object_lookup = None
                        break
                
                elif lookup_event_len == 0:
                    if not (lookup[event] == self):
                        continue
                    
                    lookup.pop(event)
                    if not len(lookup):
                        target.object_lookup = None
                        break
                
                else:
                    lookup[event].remove(self)
        
        self.event_callbacks[target].pop(event_or_events)
        if not len(self.event_callbacks[target]):
            self.event_callbacks.pop(target)

    def _send_event(self, event, *args):
        target = self.object_lookup[event]
        
        if not isinstance(target, list): #finish me
            listening_object = target #Type me later
            try:
               # method_to_call = getattr(listening_object, listening_object.event_callbacks[self][event])
               method_to_call = listening_object.event_callbacks[self][event]

            except AttributeError:
                print(f"{listening_object.event_callbacks[self][event]} isn't an attribute of {listening_object}.") # Check if this runtimes either lmao
            
            arglist = []
            for i in range(len(args[0])):
                arglist.append(args[0][i])
            
            print(str(*arglist))
            
            return method_to_call(*arglist)

        # Basically, this exists to allow for objects to unregister in the event itself, but still let every other listening object recieve the event too
        queued_calls: list = []

        for listening_object in target: #fixme
            queued_calls[listening_object] = listening_object.event_callbacks[self][event]
        
        for listening_object in queued_calls:
            try:
                method_to_call = getattr(listening_object, listening_object.event_callbacks[self][event])

            except AttributeError:
                print(f"{listening_object.event_callbacks[self][event]} isn't an attribute of {listening_object}.") # Check if this runtimes either lmao      
            
            return method_to_call(*args)
    
    def send_event(self, target, event, *args):
        if not (target.object_lookup or (event in list(target.object_lookup.keys()))):
            return
        
        target._send_event(event, [target, *args])

    def print_name(self, source):
        print(self.name)
            
        
        


obj1 = SignalNode("1")
obj2 = SignalNode("2")
obj3 = SignalNode("3")
obj1.register_event(obj2, "foo", obj1.print_name, False)
obj3.send_event(obj2, "foo")