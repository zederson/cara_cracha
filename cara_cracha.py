#!/usr/bin/env python
# -*- coding: utf8 -*-

import os
import sys
import signal

try:
    import MFRC522
    import RPi.GPIO as GPIO
    import requests
    import json
except ImportError as ie:
    print("Problema ao importar modulo {0}").format(ie)
    sys.exit()

def check_user():
    if os.geteuid() != 0:
        print("Execute com sudo")
        print("Exemplo:\nsudo python {0}").format(__file__)
        sys.exit()

def finalizar_app(signal,frame):
    global continue_reading
    print("\nCtrl+C pressionado, encerrando aplicação...")
    continue_reading = False
    GPIO.cleanup()

def call_api(tag):
    url = 'http://192.168.1.106:3000/api/trigger/toggle.json'
    headers = { 'Content-Type': 'application/json', 'Accept': 'application/json', 'Key-Tag': tag }
    requests.put(url, headers=headers)

continue_reading = True

def main():

    check_user()
    signal.signal(signal.SIGINT, finalizar_app)
    MIFAREReader = MFRC522.MFRC522()
    print("Pressione Ctrl-C para encerrar a aplicação.")

    while continue_reading:
        MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        if status == MIFAREReader.MI_OK:
            tag = ""+str(uid[0])+"."+str(uid[1])+"."+str(uid[2])+"."+str(uid[3])+"."+str(uid[4])
            print("Tag UID: {0}").format(tag)
            call_api(tag)

if __name__ == "__main__":
    main()
