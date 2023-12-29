import numpy as np
import calendar

__calendar_position = []
row = ["D", "E", "F", "G", "H", "I", "J"] #a week has 7 days
col = ["5", "7", "9", "11", "13"] #a month has 5 weeks

for c in col:
    for r in row:
        __calendar_position.append(r+c)
        
position = np.reshape(np.asarray(__calendar_position), (5, 7))

def position_transform(*, month: int, date: int, year: int=2024) -> str:
    
    for ic, c in enumerate(calendar.monthcalendar(year, month), 0):
        for ir, r in enumerate(c, 0):
            if r == date + 1:  # date + 1 means that the first day of the calendar is sunday.
                p = position[ic][ir]
                
    if p is None:
        return None
    else: 
        return p
    

MONTHS = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}