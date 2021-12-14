from .import Checksum 
from django.conf import settings 
import json,requests 

MID = settings.MID 
MKEY = settings.MKEY
headers = {
  "Content-type":"application/json"
}



def initiateTransaction(amount,orderId):
  paytm_dict = {
    "body":{
    "requestType"   : "Payment",
    "mid"           : MID,
    "websiteName"   : "WEBSTAGING",
    "orderId"       : orderId,
    "callbackUrl"   : "http://localhost:8000/paytm-callback/",
    "txnAmount"     : {
        "value"     :amount,
        "currency"  : "INR",
    },
    "userInfo"      : {
        "custId"    : "CUST_001",
    },
    }
  }
  
  url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={MID}&orderId={orderId}"
  signature = Checksum.generateSignature(json.dumps(paytm_dict["body"]),MKEY)
  
  paytm_dict["head"] ={"signature":signature} 
  data =  json.dumps(paytm_dict)
  r = requests.post(url,data=data,headers=headers).json()
  
  if r["body"]["resultInfo"]["resultCode"] == "0000" :
    return r["body"]["txnToken"]
 
  return 0 


 
  
    
  
  
  
 

