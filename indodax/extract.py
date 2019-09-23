'''
extract.py

desc:
 untuk mengekstrak kode voucher & csrf token

------------
 # kode_voucher(link_voucher)
  desc: untuk extract kode voucher indodax dari link konfirmasi pembuatan email
 
  input:
   - link_voucher = link konfirmasi pembuatan voucher
 
  return:
   - {'isError': 'False', 'voucher': kode voucher indodax}
     jika success
   - {'isError': 'True', 'error': 'kode voucher tidak ditemukan'}
     jika error
  
 # csrf_token()
  desc: untuk extract csrf token dari html
 
  input:
   - None
 
  return:
   - {'isError': 'False', 'voucher': csrf token}
     jika success
   - {'isError': 'True', 'error': 'csrf token not found'}
     jika error
  
'''


import requests
from bs4 import BeautifulSoup
import re

def kode_voucher(link_voucher):
    with requests.get(link_voucher) as link_confirm:
     try:
        soup = BeautifulSoup(link_confirm.text, "html.parser")
        soup_kode = soup.find('div', {'class':'alert alert-info'})
        if soup_kode.text != '\nDatabase tidak ada. ' or soup_kode.text != '\nData not found. ':
            extract_kode = (soup_kode.text).split(':')
            kode = extract_kode[1].replace(' ', '')
            return {'isError': False, 'voucher': kode}
        else:
            return {'isError': True, 'error': 'kode voucher tidak ditemukan'}
     except:
      pass
      

def csrf_token():
    csrf_rgx = "(?s)(?<='csrf_token' : ')(.*?)(?=')"
    with open('cok/idx_last_req_html.src', 'r') as f:
        src = f.read()
        try:
            csrf = str(re.findall(csrf_rgx, src)).split("'")[1]
            
        # jika index error silahkan lakukan cek_cookies, kemudian ulangi
        except IndexError:
            f.close()
            return {'isError': True, 'error': 'csrf token not found'}
    f.close()
    return {'isError': False, 'csrf': csrf}
    
