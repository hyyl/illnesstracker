
from datetime import *
from dateutil.parser import *
from dateutil.relativedelta import *
import re
import calendar


#reduce SQL injection vulnerability
def noninject(prompt):
    return ''.join(x for x in prompt if (x.isalnum or x==" " or x=='-' or x=="." or x==":") )



def getdate():
    NOW=datetime.now()
    DATE_FORMAT="%a %b %d %Y at %H:%M"
    try:
        retval=parse(raw_input('date and time of illness? '), ignoretz=True, fuzzy=True, default=NOW)
    except ValueError:
        print "datefailed"
    try:
        print retval.strftime(DATE_FORMAT)
        return retval.strftime(DATE_FORMAT)
    except ValueError:
        print "Please clarify your input."
        getdate()

def getduration(e_date,inpstring):
    regexstring='(days)+|(day)+|(d)+|(hours)+|(hour)+|(hr)+|(hrs)+|(h)+|(minutes)+|(minute)+|(mins)+|(min)+|(m)+'
    durarr=filter(None,re.split(regexstring,inpstring,flags=re.IGNORECASE))
    length=len(durarr)
    e_date=datetime.strptime(e_date,"%a %b %d %Y at %H:%M")
    if length%2!=0 or length>6 or length==0: #strings that don't match won't work
        return ValueError
    else:
        if length==6:
            return e_date+relativedelta(days=+int(durarr[0]),hours=+int(durarr[2]),minutes=+int(durarr[4]))
        elif length==4:
            if 'm' not in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]),hours=+int(durarr[2]))
            if 'h' not in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]),minutes=+int(durarr[2]))
            if 'd' not in inpstring:
                return e_date+relativedelta(hours=+int(durarr[0]),minutes=+int(durarr[2]))
        elif length==2:
            if 'd' in inpstring:
                return e_date+relativedelta(days=+int(durarr[0]))
            if 'h' in inpstring:
                return e_date+relativedelta(hours=+int(durarr[0]))
            if 'm' in inpstring:
                return e_date+relativedelta(minutes=+int(durarr[0]))

#WRITE: add a new entry to a given table.
def addentries(tablename,c):
    e_date=getdate()
    DATE_FORMAT="%a %b %d %Y at %H:%M"
    while True:
        try:
            e_duration_input=raw_input('duration of illness')
            e_duration=getduration(e_date,e_duration_input).strftime(DATE_FORMAT)
            break
        except ValueError:
            print "Please clarify your input in days, hours, and/or minutes"
    while True:
        try:
            rating=int(raw_input('Rating of illness? 1-10 '))
            if rating>=1 and rating <=10:
                break
        except ValueError:
            print "Please state your input as a number"

    othernotes=noninject(raw_input('anything else to say? '))
    newentry=[e_date,e_duration,rating,othernotes]
    print "You were sick at", e_date, "until", e_duration, "with an intensity of", rating, ". Also,", othernotes+"."

    c.execute("INSERT INTO {tn} VALUES(?,?,?,?)".format(tn=tablename),newentry)
