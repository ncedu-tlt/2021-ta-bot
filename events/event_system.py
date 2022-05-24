from events.events import Events

class EventSystem:
    
    @staticmethod
    def register_handler(event: str, func: callable):
        functions = Events.event_handlers.get(event)

        if functions is None:
            Events.event_handlers[event] = [func] 
        else:
            functions.append(func)

    @staticmethod
    async def bind_event(command: str, event: str):
        isBinded = False

        if bool(len(Events.event_handlers[event])):
            isBinded = True

            Events.event_triggers[command] = event 

            print(f"Command '{command}' has been binded with event '{event}' ->",  Events.event_triggers)
        
        return isBinded

    @staticmethod
    async def call_event(command):
        if bool(len(Events.event_triggers[command])):
            print(f"CALLING EVENT: {Events.event_triggers[command]}")
            return Events.event_triggers[command]

    @staticmethod
    async def isCommand(word: str):
        if bool(len((Events.event_triggers[word]))):
            print("is command")
            return True
        else:
            print("not is command")
            return False

    
    @staticmethod
    async def dispatch(event: str, data):
        functions = Events.event_handlers.get(event)

        if functions is None:
            raise ValueError(f"Unknown event {event}")
       
        for func in functions:
            await func(data)
