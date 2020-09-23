#!/usr/bin/env python3
import minimalmodbus
import os
import datetime
from influxdb import InfluxDBClient
import time


#变量定义列表，第一路电压，第一路电流，第一路功率，第一路电能消耗，第一路功率因数，第一路频率，第二路电压……
name=['vol1', 'cur1', 'pow1', 'ene1001', 'ene1002', 'q1', 'fre1', 'vol2', 'cur2', 'pow2', 'ene2001', 'ene2002', 'q2', 'fre2', 'vol3', 'cur3', 'pow3', 'ene3001', 'ene3002', 'q3', 'fre3', 'vol4', 'cur4', 'pow4', 'ene4001', 'ene4002', 'q4', 'fre4', 'vol5', 'cur5', 'pow5', 'ene5001', 'ene5002', 'q5', 'fre5', 'vol6', 'cur6', 'pow6', 'ene6001', 'ene6002', 'q6', 'fre6']
#与变量对应的寄存器地址
addr={'vol1': '0040', 'cur1': '0041', 'pow1': '0042', 'ene1001': '0043', 'ene1002': '0044', 'q1': '0045', 'fre1': '0046', 'vol2': '0047', 'cur2': '0048', 'pow2': '0049', 'ene2001': '004A', 'ene2002': '004B', 'q2': '004C', 'fre2': '004D', 'vol3': '004E', 'cur3': '004F', 'pow3': '0050', 'ene3001': '0051', 'ene3002': '0052', 'q3': '0053', 'fre3': '0054', 'vol4': '0055', 'cur4': '0056', 'pow4': '0057', 'ene4001': '0058', 'ene4002': '0059', 'q4': '005A', 'fre4': '005B', 'vol5': '005C', 'cur5': '005D', 'pow5': '005E', 'ene5001': '005F', 'ene5002': '0060', 'q5': '0061', 'fre5': '0062', 'vol6': '0063', 'cur6': '0064', 'pow6': '0065', 'ene6001': '0066', 'ene6002': '0067', 'q6': '0068', 'fre6': '0069'}
#获取后的数据字典
data_values={}

# 首先连接influxdb，需要提前创建好数据库（参考下面的创建库的命令和查询库的）

'''
# 创建数据库
database_name='pwcl'

#检测数据库是否已经存在，意义不大
for dbname in client.get_list_database():
    if dbname['name']=='pwcl':
       print("database is exist!")
       break

client.create_database('database_name')


   
# 查询数据库
client.get_list_database()
'''
#初始化库连接
client = InfluxDBClient(host='10.100.0.112', port=8086, username='youruser', password='youpassword',database='pwcl')

#influxdb数据结构定义
w_json = [{
    "measurement": 'F7itroom',
    "time": '',
    "tags": {
        
        },
    "fields": {

        }
    }]

#initialize 初始化串口数据，ttyS0为树莓派板载的串口，如果是USB转接串口，要改为USBS* 
instrument = minimalmodbus.Instrument('/dev/ttyS0', 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600


## Read data from collector at F7  ##
for i in range(0,len(name)-1):
#    print(addr[name[i]],int(addr[name[i]],16))
    try:
        data_values[name[i]] = round((instrument.read_register(int(addr[name[i]],16), 1))/10,2)
        time.sleep(0.1) #不加延迟会取不全数据
    except Exception:
        data_values[name[i]] = None
        pass

'''
#打印收集到的数据，用于调试
for i in range(0,len(name)-1):
    print(name[i],data_values[name[i]],sep='\t')

'''
# 示例数据
#data_values={'vol1': 231.3, 'cur1': 16.28, 'pow1': 26.75, 'ene1001': 0.0, 'ene1002': 397.72, 'q1': 7.12, 'fre1': 50.0, 'vol2': 231.49, 'cur2': 14.78, 'pow2': 23.16, 'ene2001': 0.0, 'ene2002': 341.65, 'q2': 6.79, 'fre2': 50.0, 'vol3': 233.09, 'cur3': 15.81, 'pow3': 26.47, 'ene3001': 0.0, 'ene3002': 387.86, 'q3': 7.2, 'fre3': 50.0, 'vol4': 231.12, 'cur4': 0.0, 'pow4': 0.0, 'ene4001': 0.0, 'ene4002': 0.0, 'q4': 0.0, 'fre4': 50.0, 'vol5': 231.3, 'cur5': 0.0, 'pow5': 0.0, 'ene5001': 0.0, 'ene5002': 0.0, 'q5': 0.0, 'fre5': 50.0, 'vol6': 232.81, 'cur6': 0.0, 'pow6': 0.0, 'ene6001': 0.0, 'ene6002': 0.0, 'q6': 0.0}


# 获取当前的时间
current_time=datetime.datetime.utcnow().isoformat("T")

#组装数据
w_json[0]['time']=current_time
w_json[0]['fields']=data_values

# 写入数据库
if not(client.write_points(w_json)):
    print("store data fail")

