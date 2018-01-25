#! /usr/bin/env python

import subprocess as sp
import xml.etree.ElementTree as ET
import re
import os
from src import sns

class CUDAMon:
    def __init__(self):
        self.gpus = []

    def check_gpu(self):
        self._get_nvidia_smi()
        self._is_card_running()
        self._is_card_temp_ok()

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
                card_arch = '{}_{}'.format(decimal.findall(card)[0], "TI")

            gpu_item = { "bus": pcie_bus, "card": card, "card_arch": card_arch, "fan_speed": fan_speed, "gpu_util": gpu_util, "memory_util": memory_util, "temp": temp, "temp_units": "Celcius", "power": power, "power_units": "Watts"  }

            self.gpus.append(gpu_item)

    def _is_card_running(self):
        for gpu in self.gpus:
            if gpu['gpu_util'] < os.getenv('GPU_UTIL_{}'.format(gpu['card_arch']), 90):
                sns.publish('GPU {} is less than {}% utilization, verify it is still running'.format(gpu['card'], gpu['gpu_util']))

    def _is_card_temp_ok(self):
        for gpu in self.gpus:
            if gpu['temp'] > os.getenv('GPU_TEMP_{}'.format(gpu['card_arch']), 75):
                sns.publish('GPU {} is too hot, running {} {}'.format(gpu['card'], gpu['temp'], gpu['temp_units']))
