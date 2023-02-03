#print calender using python?
import calendar
import re

y = int(input('please enter year:'))
m = (int(input('please enter month:')))
d = 15
h = calendar.month(y, m, 4) # 3 is the width of the date column, not the day-date
print()
print(h)
print()

# replace all numbers before your day, take care of either spaces or following \n

'''for day in range(d):
    # replace numbers at the start of a line
    pattern = rf"\n{day} "
    h = re.sub(pattern, "\n  " if day < 10 else "\n   ", h)
    # replace numbers in the middle of a line
    pattern = rf" {day} "
    h = re.sub(pattern, "   " if day < 10 else "    ", h)
    # replace numbers at the end of a line
    pattern = rf" {day}\n"
    h = re.sub(pattern, "  \n" if day < 10 else "   \n", h)'''


#//Source: https://stackoverflow.com/questions/62861105


