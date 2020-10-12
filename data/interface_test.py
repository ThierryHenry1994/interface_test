# -*- coding: utf-8 -*-
import json

import requests
import csv


# 获取用户token
def get_token(url, login_data):
    url = url

    login_data = login_data
    headers = {
        'Content-Type': 'application/json;charset=UTF-8'
    }

    response = requests.request("POST", url, headers=headers, data=login_data)

    json_obj = json.loads(response.text)
    if json_obj["info"]:
        token_raw = json_obj["info"]["accessToken"]
    token = token_raw.split(" ")[1]
    print(token)
    return token


def get_data_from_excel(excel_file):
    p_list = []
    f = csv.reader(open(excel_file, 'r'))
    for i in f:
        p_list.append(i)

    return p_list


def interface_test(param_list, token):
    # print (param_list)
    for i in range(len(param_list)):
        url = param_list[i][0]
        data = param_list[i][1].replace("\\", "")
        headers = {'access_token': token,
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json;charset=UTF-8',
                   }
        response = requests.request("POST", url, headers=headers, data=data.encode("utf-8"))
        print(response.content.decode('utf-8'))


if __name__ == '__main__':

    str1 = '{"result":1,"resCode":200,"msg":"成功","info":null}'
    str2 = '"resCode":200'
    name = str1.find(str2)
    print name


