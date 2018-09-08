import time
import serial
import csv
import datetime

port_name = '/dev/ttyUSB1'
port_baud = 38400
time_out = 2
old_rfid = '0'


def getrfid():

	try:
		ser = serial.Serial(port_name, port_baud, timeout=time_out)
		ser.flushOutput()
		ser.flushInput()
		if ser.isOpen() == True:
			ser.close()
		ser.open()
		while ser.read(1) != '\xaa':
			pass
		text = ser.read(4)
		ser.close()
		return text
		# text = ser.read(1)
		# if text == '\xaa':
		# 	text = ser.read(4)
		# 	ser.close()
		# 	return text
		# else:
		# 	ser.close()
		# 	return None
	except:
		return None

def write_log(action,value,status):
	try:
		with open('/home/pi/Practice/AGV/Setting/logreadRFID.csv', mode='a') as log:
			log_his = csv.writer(log, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			log_his.writerow([datetime.datetime.now(), action,value, status])
	except:
		print 'File already open'

def getScanDelay():
	try:
		with open('/home/pi/Practice/AGV/Setting/settingtime.txt', 'r') as File:
			time_setting = File.read()
			write_log('read_time_setting', time_setting, 'done')
			File.close()
			return time_setting
	except:
		print 'File timesetting.txt already open '
		write_log('read_time_setting', rfid, 'File can not open')
		return 0.5

while True:
	rfid = getrfid()
	if rfid == None:
		write_log('rfid_connect', 'error', 'Can not connect to rfid reader')
	print(rfid)
	if rfid != old_rfid and rfid != None:
		old_rfid = rfid
		try:
			with open('/home/pi/Practice/AGV/Setting/rfid.csv','w+') as File:
				File.write('rfid='+rfid)
				write_log('write_rfid_to_csvfile',rfid,'done')
				File.close()
		except:
			print 'File rfid.csv already open '
			write_log('write_rfid_to_csvfile', rfid, 'File can not open')

	time.sleep(0.5)