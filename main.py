# -*- coding: utf-8 -*-

from colorama import init, Fore
from datetime import datetime
from sys import exit
from os import system
import subprocess
import json
from requests import get

init(True)

title = '''
         ██    ██    ██                                    
       ██      ██  ██                                      
       ██    ██    ██                                      
         ██  ██      ██                                    
         ██    ██    ██                                    
                                                        
     ████████████████████                                  
     ██                ██████                              
     ██                ██  ██      coffee shop multi-tool ☕️                           
     ██                ██  ██          by luca denhez                       
     ██                ██████                              
       ██            ██                                    
   ████████████████████████                                
   ██                    ██                                
     ████████████████████
'''

print(Fore.RED + title + '\n')

class Coffee:
    def __init__(self):
        self.q = ''
    @classmethod
    def time(self):
        return '[' + datetime.now().strftime('%H:%M:%S') + ']'
    
    @classmethod
    def start(self):
        print(' Enter the command \'help\' for a commands list.\n')

    @classmethod
    def ask(self):
        print(self.time() + ' > ', end = '')
        self.q = input()
        self.invoke()
    
    @classmethod
    def invoke(self):
        if self.q == 'help':
            self.help()
        elif self.q == 'exit':
            exit()
        elif self.q == 'wifi':
            self.wifi()
        elif self.q == 'cip':
            self.currentIP()
        elif 'cip' not in self.q and 'ip' in self.q:
            try:
                ip = self.q.split(' ')[1]
                self.ip(ip)
            except IndexError:
                print('\n Unknown schema, IP follows command with a space\n')
                self.ask()
            except Exception as ex:
                print('\n An error occured\n')
                print(ex)
                self.ask()
        elif 'ping' in self.q:
            try:
                ip = self.q.split(' ')[1]
                self.ping(ip)
            except IndexError:
                print('\n Unknown schema, IP follows command with a space\n')
                self.ask()
            except Exception as ex:
                print('\n An error occured\n')
                print(ex)
                self.ask()
        elif self.q == 'coffee':
            print('\n☕️\n')
        elif 'savewifi' in self.q:
            try:
                mode = self.q.split(' ')[1]
                self.saveWifi(mode)
            except IndexError:
                print('\n Unknown schema, file type follows command with a space\n')
                self.ask()
            except Exception as ex:
                print('\n An error occured\n')
                print(ex)
                self.ask()
        else:
            print('\n Unknown command entered\n')
            self.ask()
    
    @classmethod
    def help(self):
        print('')
        print(' wifi - Get lots of info about current connected WiFi\n')
        print(' savewifi [json] [text] - Save WiFi information to json or text file\n')
        print(' ip [ip address] - Gets info about IP address provided\n')
        print(' cip - Gets info about your IP address\n')
        print(' ping [ip address] - Pings IP address provided\n')
        print(' coffee - ☕️\n')
        print(' exit - Exit multi-tool')
        print('')
    
    @classmethod
    def wifi(self):
        process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
        info, err = process.communicate()
        process.wait()
        
        info = info.decode(encoding='UTF-8')

        print('\nWiFi Information:\n')
        print(' WiFi Name: ' + info.split('\n')[12].split(':')[1].strip())
        print(' Security Type: ' + info.split('\n')[10].split(':')[1].strip())
        print(' Router MAC Address: ' + info.split('\n')[11].split('BSSID:')[1].strip())
        print(' Connection Strength: ' + info.split('\n')[0].split(':')[1].strip() + ' RSSI (0 to -100, the greater the stronger)')
        print('')
        
    @classmethod
    def currentIP(self):
        response = get('http://ip-api.com/json/?fields=status,country,region,city,zip,timezone,isp,lat,lon,query,proxy').json()

        if response['status'] == 'success':
            for key in response:
                if key == None:
                    key = 'Not Available'

            print('\nIP Information:\n')
            print(' Current IP: ' + response['query'])
            print(' Country: ' + response['country'])
            print(' Region: ' + response['city'] + ', ' + response['region'])
            print(' Zip Code: ' + response['zip'])
            print(' Timezone: ' + response['timezone'])
            print(' Internet Provider (ISP): ' + response['isp'])
            print(' Lat & Lon: ' + str(response['lat']) + ', ' + str(response['lon']))
            print('\n Using Proxy? ' + str(response['proxy']))
            print('')
        else:
            print('\nIP Information: Unavailable')
            print('')
    
    @classmethod
    def ip(self, ip):
        response = get('http://ip-api.com/json/' + ip + '?fields=status,country,region,city,zip,timezone,isp,lat,lon,proxy').json()

        if response['status'] == 'success':
            for key in response:
                if key == None:
                    key = 'Not Available'

            print('\nInformation for IP: ' + ip + ':\n')
            print(' Country: ' + response['country'])
            print(' Region: ' + response['city'] + ', ' + response['region'])
            print(' Zip Code: ' + response['zip'])
            print(' Timezone: ' + response['timezone'])
            print(' Internet Provider (ISP): ' + response['isp'])
            print(' Lat & Lon: ' + str(response['lat']) + ', ' + str(response['lon']))
            print('\n Using Proxy? ' + str(response['proxy']))
            print('')
        else:
            print('\nInformation for IP: ' + ip + ' unavailable')
            print('')
    
    @classmethod
    def ping(self, ip):
        print('')
        system('ping -c 5 ' + ip)
        print('')
    
    @classmethod
    def saveWifi(self, mode):
        process = subprocess.Popen(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport','-I'], stdout=subprocess.PIPE)
        info, err = process.communicate()
        process.wait()
    
        info = info.decode(encoding='UTF-8')
        
        response = get('http://ip-api.com/json/?fields=status,country,region,city,zip,timezone,isp,lat,lon,query,proxy').json()

        if mode == 'json':
            data = {}
            
            if response['status'] == 'success':
                for key in response:
                    if key == None:
                        key = 'unavailable'

                data['ssid'] = info.split('\n')[12].split(':')[1].strip()
                data['security'] = info.split('\n')[10].split(':')[1].strip()
                data['router-mac'] = info.split('\n')[11].split('BSSID:')[1].strip()
                data['strength-rssi'] = info.split('\n')[0].split(':')[1].strip()
                data['connected-ip'] = response['query']
                data['country'] = response['country']
                data['city'] = response['city']
                data['region'] = response['region']
                data['zip-code'] = response['zip']
                data['time-zone'] = response['timezone']
                data['isp'] = response['isp']
                data['latitude'] = response['lat']
                data['longitude'] = response['lon']
                data['proxy'] = response['proxy']
            else:
                data['connected-ip'] = 'unavailable'

            with open('wifi.json', 'w') as f:
                json.dump(data, f, indent = 4)
            
            print('\nDone writing to ' + mode + ' file\n')
            
        elif mode == 'text':
            with open('wifi.txt', 'w') as f:
                f.write('SSID: ' + info.split('\n')[12].split(':')[1].strip() + '\n')
                f.write('Security: ' + info.split('\n')[10].split(':')[1].strip() + '\n')
                f.write('MAC Address of Router: ' + info.split('\n')[11].split('BSSID:')[1].strip() + '\n')
                f.write('Connection Strength (RSSI): ' + info.split('\n')[0].split(':')[1].strip() + '\n')
                f.write('Connected IP: ' + response['query'] + '\n')
                f.write('Country: ' + response['country'] + '\n')
                f.write('City: ' + response['city'] + '\n')
                f.write('Region: ' + response['region'] + '\n')
                f.write('Zip Code: ' + response['zip'] + '\n')
                f.write('Time Zone: ' + response['timezone'] + '\n')
                f.write('Internet Service Provider (ISP): ' + response['isp'] + '\n')
                f.write('Latitude & Longitude: ' + str(response['lat']) + ', ' + str(response['lon']) + '\n')
                f.write('Using Proxy? ' + str(response['proxy']))

                print('\nDone writing to ' + mode + ' file\n')
        else:
            print('\n Unknown schema, file type follows command with a space\n')
 
Coffee.start()

while True:
    Coffee.ask()
