'''
live.py

desc:
 untuk menjaga sesi indodax dari expired, silahkan loop module ini

nb:
 * run module check.py terlebih dahulu sebelum menggunakan modul ini,
   karena modul ini membutuhkan cookies yang sudah di edit dari modul check.py
'''

import requests
from datetime import datetime
from http.cookiejar import MozillaCookieJar
import os
from . import HEADER, URL_INDODAX, status

# create dir untuk save cookies
if not os.path.exists('cok'):
    os.makedirs('cok')
    
# init requests.Session
session = requests.Session()
session.cookies = MozillaCookieJar('cok/idx_last_req.cok')

def start():
    '''
    desc: untuk menjaga sesi cookies indodax agar tetap aktif

    input:
     - None
 
    output:
     - {'isError': 'False', 'kode': 'session valid'}
       sesi cookies valid
     - {'isError': 'True', 'kode': 'session habis perlu login'}
       sesi expired
     - {'isError': 'True', 'kode': 'error tidak diketahui'}
       error tidak di ketahui
    '''
    # load & menggabungkan cookies dari file cookies sebelumnya
    satu = MozillaCookieJar()
    dua = MozillaCookieJar()
    satu.load('cok/idx_redeem.cok')
    dua.load('cok/idx_last_req.cok')
    live_cookies = requests.cookies.merge_cookies(satu, dua)
    
    cek_sess = session.get(URL_INDODAX, headers=HEADER, cookies=live_cookies)
    
    if cek_sess.url == 'https://indodax.com/login':
        status.write('status.json', 'indodax', 'status', 'down')
        status.write('status.json', 'indodax', 'live', False)
        return {'isError': True, 'error': 'session habis perlu login'}
    
    elif cek_sess.url == 'https://indodax.com/voucher':
        session.cookies.save()
        status.write('status.json', 'indodax', 'status', 'up')
        status.write('status.json', 'indodax', 'last_update', str(datetime.utcnow()))
        f = open('cok/idx_last_req_html.src', 'w')
        f.write(cek_sess.text)
        f.close
        return {'isError': False, 'success': 'session valid'}
    
    else:
        status.write('status.json', 'indodax', 'status', 'down')
        status.write('status.json', 'indodax', 'live', False)
        return {'isError': True, 'error': 'error tidak diketahui, perlu check'}




if __name__ == '__main__':
    start()
