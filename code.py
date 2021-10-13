import requests
import json
import urllib3
urllib3.disable_warnings()
def update():
  b=0
  dt= requests.get('https://static.pipezero.com/covid/data.json')
  dt_json=dt.json()
  chet=dt_json['total']['internal']["death"]
  nhiem=dt_json['total']['internal']["cases"]
  khoi=dt_json['total']['internal']["recovered"]
  dang=nhiem-chet-khoi
  return chet,nhiem,khoi,dang
def sim(ms):
    
    re="https://api.simsimi.net/v2/?text="+ms+"&lc=vn"
    dt=requests.get(re)
    dt_json=dt.json()
    return dt_json['success']
