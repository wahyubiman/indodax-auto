'''
check.py

desc:
 untuk fix format cookies.tx & check apakah sesi kuki masih valid

nb:
 * jalankan modul ini untuk pertama kali saja, karena akan menimbulkan sesi expired
   jika di jalankan berulang karena modul ini hanya mengedit file cookies.txt
   dan mengecek apakah cookies valid atau tidak,
   untuk loop sesi agar tetap aktif gunakan modul live.py
'''

import sys
import requests
from datetime import datetime
from http.cookiejar import MozillaCookieJar
import os
import re
from . import HEADER, URL_INDODAX, status

# set utc & write to status.json
# harus set waktu ke utc dengan datetime.utcnow()
status.write('status.json', 'indodax', 'start', str(datetime.utcnow()))
# create dir untuk save cookies
if not os.path.exists('cok'):
    os.makedirs('cok')
    
# init requests.Session
session = requests.Session()
session.cookies = MozillaCookieJar('cok/idx_last_req.cok')

def fix_cookies(cookies_path):
    '''
    desc: untuk fix cookies dari cookies.tx ke format netscape
   
    input:
     - cookies_path = lokasi file cookies.txt
 
    output:
     - 2 file cookies untuk cek sesi & redeem voucher
       cok/idx_fix.cok, cok/idx_redeem.cok
    '''
    first_load_cookies = open('cok/idx_fix.cok', 'w')
    edit_cookies_for_redeem = open('cok/idx_redeem.cok', 'w')
    first_load_cookies.write("# HTTP Cookie File")
    first_load_cookies.write('\n')
    try:
        with open(cookies_path, 'r') as f:
            for line in f:
                if line.startswith("#HttpOnly_"):
                    line = line[len("#HttpOnly_"):]
                    
                if line.startswith("#") or line.startswith("\n"):
                    edit_cookies_for_redeem.write(line)
                else:
                    pisah = re.split(r'\t+', line)
                    if pisah[5] == 'btcid' or pisah[5] == 'ex' or pisah[5] == 'cu' or pisah[5] == 'll' or pisah[5] == 'tz' or pisah[5] == 'un':
                        pass
                    elif line.startswith(".indodax") or line.startswith("indodax"):
                        edit_cookies_for_redeem.write(line)
                
                if line.startswith(".indodax") or line.startswith("indodax"):
                    first_load_cookies.write(line)
        
        f.close()
        edit_cookies_for_redeem.close()
        first_load_cookies.close()
        
    finally:
        #os.remove(cookies_path)
        pass
        
        
def is_valid(cookies_path):
    '''
    desc: untuk check sesi dari cookies file apakah valid / tidak

    input:
     - cookies_path = lokasi file cookies.txt
 
    output:
     - {'isError': 'False', 'kode': 'session valid'}
       sesi cookies valid
     - {'isError': 'True', 'kode': 'session habis perlu login'}
       sesi expired
     - {'isError': 'True', 'kode': 'error tidak diketahui'}
       error tidak di ketahui
    '''
    fix_cookies(cookies_path)
    
    fix = MozillaCookieJar()
    fix.load('cok/idx_fix.cok')
    
    cek_sess = session.get(URL_INDODAX, headers=HEADER, cookies=fix)
    if cek_sess.url == 'https://indodax.com/login':
        status.write('status.json', 'indodax', 'status', 'down')
        status.write('status.json', 'indodax', 'live', False)
        return {'isError': True, 'error': 'session habis perlu login'}
    elif cek_sess.url == 'https://indodax.com/voucher':
        session.cookies.save()
        status.write('status.json', 'indodax', 'status', 'up')
        status.write('status.json', 'indodax', 'live', True)
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
	is_valid(sys.argv)
