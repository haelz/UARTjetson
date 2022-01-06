import csv  
from datetime import datetime
import time
import os.path
import serial

filepath= 'dhtdata.csv'
exist=os.path.isfile(filepath)
header = ["Timestamp","Temperature","Humidity"]
csvfile = open(filepath, 'a')
writer = csv.DictWriter(csvfile,delimiter=",",lineterminator='\n', fieldnames = header)

serial_port = serial.Serial(
    port="/dev/ttyTHS1",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)
# Wait a second to let the port initialize
time.sleep(1)

#if file not exist write header
if not exist:
    writer.writeheader()
    
try:
    #serial_port.write("UART test\r\n".encode())
    while True:
        if serial_port.inWaiting() > 0:
            data = serial_port.readline()
            print(data)
             
            # split the data
            split=data.decode("utf-8").split(";")
            temp = split[0]
            hum = split[1]
            now = datetime.now()
            #change timeformat
            t = now.strftime('%Y-%m-%d %H:%M:%S')
            
            #write the data
            writer.writerow({"Timestamp":t, "Temperature":temp, "Humidity":hum})
except KeyboardInterrupt:
    print("Exiting Program")
    
except Exception as exception_error:
    print("Error occurred. Exiting Program")
    print("Error: " + str(exception_error))

finally:
    serial_port.close()
    csvfile.close()
    pass

