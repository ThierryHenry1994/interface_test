# -*- coding: utf-8 -*-
import json

import requests
import xlrd
import write_result
import fire


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
    # print(token)
    return token


def get_data_from_excel(excel_file):
    param_list = []
    workbook = xlrd.open_workbook(excel_file)
    my_sheet = workbook.sheet_by_index(0)
    n_rows = my_sheet.nrows
    for i in range(1, n_rows):
        param_list.append(my_sheet.row_values(i))
    return param_list


def interface_test(param_list, token):
    result_list = []
    for i in range(len(param_list)):
        url = param_list[i][0]
        data = param_list[i][1].replace("\\", "")
        headers = {'access_token': token,
    'Authorization': 'Bearer '+token,
    'Content-Type': 'application/json;charset=UTF-8'
                   }
        response = requests.request("POST", url, headers=headers, data=data.encode("utf-8"))
        result = judge_result(response.content, expect=param_list[i][2])
        # 接口地址， 接口名称，是否通过, 备注
        if result != "success":
            info = response.content
        else:
            info = ""
        result_list.append((url, param_list[i][3], result, info))

    return result_list


def judge_result(raw, expect):
    if str(raw).find(expect) != -1:
        return "success"
    else:
        return "failed"


def get_test_case(case):
    case_list = []
    for i in case:
        _case = i.split("-")[1]
        case_list.append(_case)
    return case_list


def test(test_case):
    result_list = []
    login_url = "http://192.168.1.106/qxgl-center/Mh001LoginCtrl/handleLogins"
    loin_data = "{\"userName\":\"Z3VvanVu\",\"userPwd\":\"Y3NzMTIzNDU=\"}"
    test_token = get_token(login_url, loin_data)
    test_file_list = get_test_case(test_case)
    # excel = './data/test.xlsx'
    for test_file in test_file_list:
        folder = './'+test_file+"/test.xlsx"
        param = get_data_from_excel(folder)
        _result = interface_test(param, test_token)
        result_list.append(_result)

    write_result.write_whole_html_file(u"冒烟测试", result_list)


if __name__ == '__main__':
    fire.Fire(test)
