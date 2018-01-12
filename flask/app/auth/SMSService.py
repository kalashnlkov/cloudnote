# coding: utf-8
import sys
import urllib.request
import urllib.parse
import urllib.error
import base64
import hmac
from hashlib import sha1
import time
import uuid
import json
import ssl

from flask import current_app as app


server_address = 'https://dysmsapi.aliyuncs.com'
# 定义参数


def percent_encode(encodeStr):
    encodeStr = str(encodeStr)
    res = urllib.parse.quote(encodeStr.encode('utf8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def compute_signature(parameters, access_key_secret, quiet=False):
    sortedParameters = sorted(list(parameters.items()),
                              key=lambda parameters: parameters[0])
    canonicalizedQueryString = ''
    for (k, v) in sortedParameters:
        canonicalizedQueryString += '&' + \
            percent_encode(k) + '=' + percent_encode(v)
    stringToSign = 'GET&%2F&' + percent_encode(canonicalizedQueryString[1:])
    # print("stringToSign:  " + stringToSign)
    h = hmac.new((access_key_secret + '&').encode(encoding="utf-8"),
                 stringToSign.encode('utf-8'), sha1)
    signature = base64.encodestring(h.digest()).strip()
    
    return signature
    


def compose_url(user_params):
    timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time()))
    parameters = {
        'Format': 'JSON',
        'AccessKeyId': AccessKeyId,
        'SignatureVersion': '1.0',
        'SignatureMethod': 'HMAC-SHA1',
        'SignatureNonce': str(uuid.uuid1()),
        'RegionId': 'cn-hangzhou',
        'Timestamp': timestamp
    }
    for key in list(user_params.keys()):
        parameters[key] = user_params[key]
    signature = compute_signature(parameters, AccessKeySecret)
    parameters['Signature'] = signature
    url = server_address + "/?" + urllib.parse.urlencode(parameters)
    return url


def make_request(user_params):
    url = compose_url(user_params)
    request = urllib.request.Request(url)
    try:
        context = ssl._create_unverified_context()
        conn = urllib.request.urlopen(request, context=context)
        response = conn.read().decode('utf-8')
    except urllib.error.HTTPError as e:
        print((e.read().strip()))
        raise SystemExit(e)
    try:
        obj = json.loads(response)
        return obj
    except ValueError as e:
        raise SystemExit(e)
    json.dump(obj, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')


def sendSMS(phonenumber, code):
    user_params = {'Action': 'SendSms',
                   'Version': '2017-05-25',
                   'SignName': 'Cloud笔记',
                   'TemplateCode': 'SMS_120120689',
                   'TemplateParam': '{"code":"default code"}',
                   }
    # send phonenumber and the verify code.
    user_params['PhoneNumbers'] = str(phonenumber)
    user_params['TemplateParam'] = str({'code': code})
    return make_request(user_params)
