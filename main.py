#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import os
import xmltodict
from pathlib import Path

API_KEY = ""
params = {"crtfc_key": API_KEY}
URL = "https://opendart.fss.or.kr/api/corpCode.xml"


def bind_params(params: dict):
    url_params = []
    for key in params:
        url_params.append(key + '=' + params[key])
    return url_params


def has_corpfile():
    dirpath = os.getcwd()

    if Path(dirpath + '/CORPCODE.xml').is_file():
        return True
    else:
        return False

    # 파일존재 체크 다른 방법들..
    # if os.path.isfile(dirpath + '/CORPCODE.xml'):
	#     return True
    # else:
    #     return False
    # try:
    #     open(dirpath + '/CORPCODE.xml', 'r')
    #     return True
    # except FileNotFoundError:
    #     return False


def get_corp_xml(url, params):

    if has_corpfile():
        dirpath = os.getcwd()
        return open(dirpath + '/CORPCODE.xml', 'r').read()
    else:
        url = url + '&'.join(bind_params(params))
        resp = urlopen(url)

        # zip으로 저장할경우
        # f = open( 'corpCode.zip', 'wb' )
        # f.write(resp.read())
        # f.close()

        # zip파일내용을 풀어 저장한다.
        zipfile = ZipFile(BytesIO(resp.read()))
        print(zipfile.namelist())
        for name in zipfile.namelist():
            z = zipfile.open(name)
            with open(name, 'w') as codefile:
                for l in z.readlines():
                    codefile.write(l.decode())
        dirpath = os.getcwd()
        return open(dirpath + '/CORPCODE.xml', 'r').read()


""" Biz Start """

url = 'https://opendart.fss.or.kr/api/corpCode.xml?'
params = {
  'crtfc_key': '',  # API 인증키
}

corp_xml = get_corp_xml(url, params)

corp_dict = xmltodict.parse(corp_xml)

print(type(corp_dict))

print(corp_dict)
