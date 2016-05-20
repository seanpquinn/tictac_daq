import os
import collections
import time
import math
import subprocess

def utcFromString(x):
  split_x = x.split(',')
  int_x = map(int,split_x)
  right_order = [2,1,0,3,4,5]
  int_x = [int_x[i] for i in right_order]
  return int_x

secsInWeek = 604800 
secsInDay = 86400 
gpsEpoch = (1980, 1, 6, 0, 0, 0)  # (year, month, day, hh, mm, ss)

logfile = 'tic_tac_mutel.log'
eventfile = 'tic_tac_events_mutel.txt'

def gpsFromUTC(year, month, day, hour, minute, sec, leapSecs=17): 
  """converts UTC to GPS second

  Original function can be found at: http://software.ligo.org/docs/glue/frames.html

  GPS time is basically measured in (atomic) seconds since  
  January 6, 1980, 00:00:00.0  (the GPS Epoch) 

  The GPS week starts on Saturday midnight (Sunday morning), and runs 
  for 604800 seconds.  

  Currently, GPS time is 17 seconds ahead of UTC
  While GPS SVs transmit this difference and the date when another leap 
  second takes effect, the use of leap seconds cannot be predicted.  This 
  routine is precise until the next leap second is introduced and has to be 
  updated after that.

  SOW = Seconds of Week 
  SOD = Seconds of Day 

  Note:  Python represents time in integer seconds, fractions are lost!!! 
  """ 
  secFract = sec % 1 
  epochTuple = gpsEpoch + (-1, -1, 0) 
  t0 = time.mktime(epochTuple) 
  t = time.mktime((year, month, day, hour, minute, sec, -1, -1, 0))  
  # Note: time.mktime strictly works in localtime and to yield UTC, it should be 
  #       corrected with time.timezone 
  #       However, since we use the difference, this correction is unnecessary. 
  # Warning:  trouble if daylight savings flag is set to -1 or 1 !!! 
  t = t + leapSecs
  tdiff = t - t0
  gpsSOW = (tdiff % secsInWeek)  + secFract
  gpsWeek = int(math.floor(tdiff/secsInWeek))
  gpsDay = int(math.floor(gpsSOW/secsInDay))
  gpsSOD = (gpsSOW % secsInDay)
  gps_tuple = (gpsWeek, gpsSOW, gpsDay, gpsSOD)
  return int(gps_tuple[0] * secsInWeek + gps_tuple[1])

N = 749995494 # Precision oscillator frequency

def computeMicro(n1,n2):
  if n2>n1:
    micsec = float(n2-n1) / N
    micsec_str = "%.6f" %micsec
    return micsec_str.split('.')[1]
  else:
    micsec = float(N-n1+n2) / N
    micsec_str = "%.6f" %micsec
    return micsec_str.split('.')[1]

def sendT3(buf):
  N2 = buf.pop() #Last entry is TESTevent counter value (string)
  N2 = int(N2.split(' ')[-1]) #Format to int
  next = buf.pop() #Next entry unknown: could be GPS counter, or UTC timestamp
  if "GPS" in next:
    N1 = next #This entry will be GPS 1 PPS count
    N1 = int(N1.split(' ')[-1])
    utc_list = utcFromString(buf.pop()) #Format string as ymdhmmss list
    gps_sec = gpsFromUTC(*utc_list) #Find GPS second from list
    gps_sec += 1 #Since this PPS is for next timestamp
    Tmicro = computeMicro(N1,N2)
#    print "%i.%s"%(gps_sec,Tmicro)
    with open(logfile,'a',1) as F:
      F.write('%i.%s\n' %(gps_sec,Tmicro))
    return None
  else:
    utc_list = utcFromString(next)
    gps_sec = gpsFromUTC(*utc_list)
    N1 = buf.pop()
    N1 = int(N1.split(' ')[-1])
    Tmicro = computeMicro(N1,N2)
#    print "%i.%s"%(gps_sec,Tmicro)
    with open(logfile,'a',1) as F:
      F.write('%i.%s\n' %(gps_sec,Tmicro))
    return None

#Serial port on machine
dev_id = '/dev/ttyUSB0'
#dev_id = 'data_out.txt'

auger_south = ''

#Small data buffer
databuf = collections.deque([],3)

#Read serial, write time stamps to file
bufsize=1*10**3
with open(dev_id,'r') as f, open(eventfile,'a',-1) as ff:
  #Main loop
  #Configure serial port terminal appropriately. See README
  while True:
    data = f.readline() #Blocking read
#    print "%r" %data #Debugging
    ff.write(data)
    if len(data) > 18: #This prevents parsing of 'unhealthy messages'
      databuf.append(data)
       #Buffer should be fully populated
      if len(databuf)>2:
        #Buffer should be filled with parseable elements only
        blob = ''
        for i in databuf:
          blob = blob + i
        if "GPS" in blob and "2016" in blob and "TEST" in blob:
          sendT3(databuf)
        else:
          continue
      else:
        continue
    else:
      continue