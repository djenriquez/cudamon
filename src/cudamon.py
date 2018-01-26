#! /usr/bin/env python

import subprocess as sp
import xml.etree.ElementTree as ET
import re
import os
import logging
from src import sns

class CUDAMon:
    def __init__(self):
        self.gpus = []
        self.sns = sns.SNS()

        self._get_nvidia_smi()
        logging.info('Cards detected: ')
        for gpu in self.gpus:
            logging.info(gpu['card'])

    def check_gpus(self):
        logging.debug('Checking GPUs')
        self._get_nvidia_smi()

        running = self._is_card_running()
        cool = self._is_card_temp_ok()

        if running and cool:
            self.sns.reset_alert()
        else:
            self.sns.alert()

    def _get_nvidia_smi(self):
        data = sp.check_output(['nvidia-smi', '-q', '-x'])
        root = ET.fromstring(data)

        self.gpus = []

        decimal = re.compile('\d+\.*\d*')
        card_r = re.compile('\d+\s*\S*')

        for gpu in root.iter('gpu'):
            pcie_id = gpu.attrib['id']
            product_brand = gpu.find('product_brand').text

            card = gpu.find('product_name').text
            pcie_bus = gpu.find('pci').find('pci_bus').text
            fan_speed = decimal.findall(gpu.find('fan_speed').text)[0]
            gpu_util = decimal.findall(gpu.find('utilization').find('gpu_util').text)[0]
            memory_util = decimal.findall(gpu.find('utilization').find('memory_util').text)[0]
            temp = decimal.findall(gpu.find('temperature').find('gpu_temp').text)[0]
            power = decimal.findall(gpu.find('power_readings').find('power_draw').text)[0]
            card_arch = card_r.findall(gpu.find('product_name').text)[0]

            if 'ti' in card_arch.lower():
                card_arch = '{}_{}'.format(decimal.findall(card)[0], 'TI')

            gpu_item = { 'bus': pcie_bus, 'card': card, 'card_arch': card_arch, 'fan_speed': fan_speed, 'gpu_util': gpu_util, 'memory_util': memory_util, 'temp': temp, 'temp_units': 'Celcius', 'power': power, 'power_units': 'Watts'  }

            self.gpus.append(gpu_item)

    def _is_card_running(self):
        logging.debug('Checking GPU utilzation')
        all_running = True
        for gpu in self.gpus:
            config_util = os.getenv('GPU_UTIL_{}'.format(gpu['card_arch']), 90)
            if float(gpu['gpu_util']) < float(config_util):
                self.sns.publish('GPU {} is running {}% utilization, needs {}%. Verify it is still running.'.format(gpu['card'], gpu['gpu_util'], config_util))
                all_running = False

        if not all_running:
            logging.warn('Low GPU utilization detected')

        return all_running

    def _is_card_temp_ok(self):
        logging.debug('Checking GPU Temperatures')
        all_cool = True
        for gpu in self.gpus:
            config_temp = os.getenv('GPU_TEMP_{}'.format(gpu['card_arch']), 75)
            if float(gpu['temp']) > float(config_temp):
                self.sns.publish('GPU {} is too hot, running {} {}, needs {} {}.'.format(gpu['card'], gpu['temp'], gpu['temp_units'], config_temp, gpu['temp_units'] ))
                all_cool = False

        if not all_cool:
            logging.warn('High GPU temperature detected')

        return all_cool
