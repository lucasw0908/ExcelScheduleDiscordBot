def get_date(message):
    
    month = None
    date = None
    
    if "/" in message:
            
        try: 
            msglist = list(map(int, message.split("/")))
        
            if len(msglist) == 2:
                month = msglist[0]
                date = msglist[1]

        except: pass
        
    elif " " in message:
        
        try: 
            msglist = list(map(int, message.split(" ")))
        
            if len(msglist) == 2:
                month = msglist[0]
                date = msglist[1]

        except: pass
    
    return month, date