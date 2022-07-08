from email import message
import hmac
import hashlib
import json
key = b'pvqnA16kBFMk4hDs2z50XFVOWrv5PLlA'

message = {"use_zpdl":"true","result":"success","download_url":"https://dl.boxcloud.com/zip_download/zip_download", "ProgressReportingKey":"E931C4F834BEE8EAC2FCB447F981D6E3","d":"145087168984","ZipFileName":"207%20-%20Living.zip","Timestamp":1652167857}
jdata = json.dumps(message).encode('utf-8')
hmac_msg = hmac.new(key, jdata, hashlib.sha256)
print("hmac : ", hmac_msg.hexdigest())
