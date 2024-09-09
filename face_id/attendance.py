import csv
from datetime import datetime


#save attendance in csv file.
def attendance(name):
                
    with open('attendance_sheet.csv','r+') as f:
        
        mydata = f.readlines()
        namelist=[]
        for line in mydata:
            entry = line.split(';')
            namelist.append(entry[0])
            
        if name not in namelist:
            now = datetime.now()
            time_string = now.strftime('%H:%M:%S')
            date_string = now.strftime('%Y/%m/%d')

            f.writelines(f'\n{name};{date_string};{time_string}')

       
