#!/usr/bin/env python3
import minimalmodbus
import time

"""
用途：由于此寄存器最大存储65535，电量使用达到655度时为自动归0，为了避免发生后导致数据错误，每天定时手动进行重置。
脚本执行时间：每天23：59通过crontab执行

"""
#电量寄存器地址，这个地址是第一个，重置地址和读取地址不一样
engaddr=("0044","004B","0052","0059","0060","0067","006E","0075")
#等待每分钟的数据采集完成
time.sleep(15)
#初始串口模块
instrument = minimalmodbus.Instrument('/dev/ttyS0', 1)  # port name, slave address (in decimal)
instrument.serial.baudrate = 9600
instrument.timeout=0.1
#重置寄存器数据，防止溢出
try:
    for addr in engaddr:
#        instrument.read_register(int(addr,16),2)
        time.sleep(0.1)
        instrument.write_register(int(addr,16),0)
except Exception:
    pass
    