from events.event_system import EventSystem

def filter(words: list):
    def wrapper(function):
        async def gift_wrap(message, *args, **kwargs):     
            print("<filter>")

            isPassed = True
            
            for word in words:
                if word == message.text:
                    isPassed = False
                    
                    try:
                        if await EventSystem.isCommand(word):
                            
                            event_name = await EventSystem.call_event(word)

                            await EventSystem.dispatch(event_name, message)
              
                    except:
                        print("Not binded events")
                
            
            if isPassed:
                try:                    
                    await function(message, *args, **kwargs)
                    
                except:                   
                    print(f"UNKNOWN WORD '{message.text}'")

            print("</filter>")
        return gift_wrap
    return wrapper
