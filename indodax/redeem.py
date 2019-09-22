'''
redeem.py

desc:
 modul untuk redeem voucher indodax
'''

import requests
import json
import re
from datetime import datetime
from http.cookiejar import MozillaCookieJar
from . import HEADER_REDEEM, URL_REDEEM_VOUCHER, status, extract

# init requests.Session
session = requests.Session()

def prepare(link_voucher):
    '''
    desc:
     prepare sebelum redeem voucher
     
    input:
     - link_voucher = link voucher dari email yang di kirim indodax
     
    output:
     - jika error akan keluar kode error sesuai error nya dimana,
       apakah dari token csrf atau dari kode vouchernya
    '''
    cek = status.read('status.json', 'indodax', 'live')
    
    # cek kode voucher apakah valid
    if cek:
        kode = extract.kode_voucher(link_voucher)
        csrf = extract.csrf_token()
        
        if kode['isError'] :
            return kode
        else:
            if csrf['isError']:
                return csrf
            else:
                return {'isError': False, 'csrf': csrf['csrf'], 'kode': kode['voucher']}

def redeem(csrf, kode):
    '''
    desc:
     untuk meredeem voucher menggunakan method post dengan csrf & kode voucher
     
    input:
     - csrf = token csrf
     - kode = kode voucher indodax
     
    output:
     - jika success output jumlah voucher yang di gunakan
     - jika error output error nya di mana
    '''
    # load & menggabungkan cookies dari file cookies sebelumnya
    satu = MozillaCookieJar()
    dua = MozillaCookieJar()
    satu.load('cok/idx_redeem.cok')
    dua.load('cok/idx_last_req.cok')
    redeem_cookies = requests.cookies.merge_cookies(satu, dua)
    
    # menyiapkan data post
    payload = F"csrf_token={csrf}&deposit_coupon={kode}"
    
    redeem_sess = session.post(URL_REDEEM_VOUCHER, headers=HEADER_REDEEM, data=payload, cookies=redeem_cookies)
    
    hasil = redeem_sess.json()
    
    
    
    if hasil['is_error'] == False:
        return {'isError': False, 'success': hasil['success']}
            
    # kembalikan voucher jika terjadi error
    else:
        return {'isError': True, 'error': hasil['error']}
    
def start(link_voucher):
    '''
    desc:
     mulai redeem voucher setelah melakukan prepare
     
    input:
     - link_voucher = link voucher dari email yang di kirim indodax
     
    output:
     - jumlah yang berhasil di redeem jika success
     - kode error jika mengalami error 
    '''
    pre = prepare(link_voucher)
    
    if pre['isError']:
        return pre
    else:
        redeem_voucher = redeem(pre['csrf'], pre['kode'])
        if redeem_voucher['isError'] == False:
            status.write('status.json', 'indodax', 'last_redeem', str(datetime.utcnow()))
            return {'isError': False, 'success': redeem_voucher['success']}
        else:
            return redeem


