import os
import requests
import time 
import psutil
import logging

logging.basicConfig(filename='client.log', level=logging.INFO)
logging.info('Client started')

SERVER_URL = 'http://ya.ru'
response = {}


while True:
    response['host_information'] = os.uname()
    response['battery'] = psutil.sensors_battery().percent  
    response['network'] = []
    response['disk'] = []
    for key in psutil.net_if_stats().keys():
        
        network_dict = {
                key : "Up" if psutil.net_if_stats()[key].isup else "Down",
                'mtu': psutil.net_if_stats()[key].mtu
                }
        response['network'].append(network_dict)
    response['memory'] = {
        'memory_total': psutil.virtual_memory().total,
        'memory_used': psutil.virtual_memory().used,
        'memory_percent': psutil.virtual_memory().percent
    }        
    
    response['cpu'] = {
        'cpu_cores': psutil.cpu_count(),
        'cpu_physical_cores': psutil.cpu_count(logical=False),
        'cpu_freqency': {
            'min': psutil.cpu_freq().min,
            'max': psutil.cpu_freq().max,
            'current': psutil.cpu_freq().current
        },
        'load_average': {
            '1 min': psutil.getloadavg()[0],
            '5 min': psutil.getloadavg()[1],
            '15 min': psutil.getloadavg()[2]
        }
    }

    for disk in psutil.disk_partitions():
        response['disk'].append(
            {
                'device': disk.device,
                'mountpoint': disk.mountpoint,
                'file_system_type': disk.fstype,
                'total': psutil.disk_usage(disk.mountpoint).total,
                'used': psutil.disk_usage(disk.mountpoint).used,
                'percent': psutil.disk_usage(disk.mountpoint).percent,

            }
        )
    send_msg = requests.post(SERVER_URL, data=response)
    if send_msg.status_code == 200:
        logging.info('message send, status_code = 200')
    else:
        logging.error(f'message sending failed, status_code = {send_msg.status_code}')
    time.sleep(60)