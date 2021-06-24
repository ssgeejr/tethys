#!/usr/bin/env python3

import csv, time, sys, getopt, glob, os
import mysql.connector
from mysql.connector import connect, Error
from pathlib import Path


dtkey = time.strftime('%m%y')
userDefinedKey = False

def fetchrefid(risk):
    result = -99;
    if risk == 'Critical': result = 0
    elif risk == 'High': result = 1
    elif risk == 'Medium': result = 2
    elif risk == 'Low': result = 3
    elif risk == 'None': result = -1
    return result


def fetchFileStack():
   global dtkey
   global userDefinedKey 
   working_dir = "/opt/apps/sc.data"
   os.chdir(working_dir)
   for file in glob.glob("*.csv"):
       print(file)
       old_file = os.path.join(working_dir,file)
       new_file = os.path.join(working_dir,file+'.old')
       print('Using data file: ', os.path.basename(old_file))
       loadRawData(old_file)

       if userDefinedKey:
           print('User Defined Key: ',dtkey)
       else:
           dtkey = Path(old_file).stem

       print('Using Filename Key: ',dtkey)

       print('New File: ',new_file)
       print('***** FILE LOAD COMPLETED - RENAMING TO *.old *****')
       # os.rename(old_file, new_file)

def loadRawData(datafile):
   global dtkey

   print('DTKEY: ',dtkey)

   return
   dt = time.strftime('%Y%m%d') 

   with open(datafile, mode ='r')as file:

   # reading the CSV file
       csvFile = csv.reader(file)
   
   # displaying the contents of the CSV file
       try:
           cnx = mysql.connector.connect(user='scorecard', 
           password='scorecard',
           host='127.0.0.1',
           database='scorecard')
           print(cnx)
           mycursor = cnx.cursor()
           sql = "insert ignore into rawdata(datakey,pluginid,host,riskid,rptdatekey,rptdate) values (%s, %s, %s, %s, %s, %s)"
           count = 0
           for lines in csvFile:
               if count > 0:
                   datakey = dtkey+lines[0]+lines[4] 
                   record = (datakey,lines[0],lines[4],fetchrefid(lines[3]),dtkey,dt)
           #        print(record)
                   #print(lines[0] + ' ' + lines[4] + ' ' + dt)
                   mycursor.execute(sql, record)
                   #if count > 10: return
                   if (count % 1000) == 0:
                       cnx.commit()
                       print("commiting another 1000 records: " , count)
               count+=1

           print("Total records loaded: " , count)
       except Error as e:
           print('Error at line: ', count)
           print('******** INPUT LINE **********')
           print(lines)
           print('******************************')
           print(e)
       


def main(argv):
   global dtkey
   global userDefinedKey
   try:
      opts, args = getopt.getopt(argv,"hp:",["pkey="])
   except getopt.GetoptError:
      print ('dataloader.py -p <date>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print ('dataloade.py -p <date>')
         sys.exit()
      elif opt in ("-p", "--pkey"):
         userDefinedKey = True 
         dtkey = arg
   print ('DTKEY: ', dtkey)
   fetchFileStack()

if __name__ == "__main__":
    main(sys.argv[1:])
