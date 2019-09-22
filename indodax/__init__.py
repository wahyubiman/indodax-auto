
# global var url indodax
URL_INDODAX = 'https://indodax.com/voucher'
URL_REDEEM_VOUCHER = 'https://indodax.com/ajax/deposit_coupon'

# global var header untuk login pertama kali dan persisten sesi dalam loop
HEADER = {
    "Host": "indodax.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "cache-control": "max-age=0",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Android 8.0.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"

}

# global var header untuk redeem voucher indodax
HEADER_REDEEM = {
    "Host": "indodax.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "origin": "https://indodax.com",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "referrer": "https://indodax.com/voucher",
    "user-agent": "Mozilla/5.0 (Android 8.0.0; Mobile; rv:68.0) Gecko/68.0 Firefox/68.0"
}
