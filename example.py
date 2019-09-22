'''
contoh menggunakan modul indodax redeem voucher

----------------
creator : wahyu biman
github : https://github.com/wahyubiman
fb : https://www.facebook.com/kemped
telegram : https://t.me/wahyubiman
'''

# import modul yg diperlukan
import json
import time
from random import randrange as random
from random import randrange as random
import core.indodax.check as indodax_check
import core.indodax.status as status
import core.indodax.live as indodax_live
import core.indodax.redeem as indodax_redeem
from datetime import datetime

'''
- modul ini membutuhkan file cookies.txt dari hasil export cookies
- setelah login indodax berhasil,
  silahkan extract cookies nya menggunakan addon mozilla export cookies
- bisa menggunakan firefox android/desktop untuk export
- bisa menggunakan export cookies dengan chrome/browser lain
  asalkan cookies nya dengan format netscape
'''

# check cookies apakah valid
cek = indodax_check.is_valid('cookies.txt')
n = 0
link = 'https://indodax.com/wc1/5417352edcb7a3310b2ba13f15f10f1e6f823cac9dac609e973bcb6abd99fa7e'

if cek['isError'] == False:
    print(cek['success'])
    print('')
    # jika tidak error run indodax_live.start() untuk menjaga cookies agar tidak expired
    # loop untuk menjaga cookies agar tidak expired
    # bisa menggunakan while atau mode threading
    # jangan lupa gunakan sleep agar tidak terblock
    while True:
        time.sleep(random(1, 5))
        live = indodax_live.start()
        print(live['success'])
        if live['isError']:
            # handle cookies expired
            # jika error silakan dump cookies lagi :)
            print(cek['error'])
            break
        
        # redeem voucher
        # harus dari link konfirmasi pembuatan email untuk menghindari salah kode
        # tidak bisa menggunakan format BTC-IDR agar tidak di banned :p
        if n == 8:
            redeem = indodax_redeem.start(link)
            if redeem['isError'] == False:
                print(redeem['success'])
            else:
                print(redeem['error'])
        
        if n == 15:
            break
        n += 1
else:
    print(cek['error'])





