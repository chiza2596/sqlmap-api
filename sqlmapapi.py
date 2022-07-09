#!/usr/bin/python
# !-*-coding:utf-8 -*-
# data: 2022/5/24 20:07
import requests
import json
import time

def sqlmapapi(url):
    data = {
        'url': url
    }
    headers = {
        'Content-Type': 'application/json'
    }
    task_url = 'http://127.0.0.1:8775/task/new'
    res = requests.get(task_url)
    task_id = res.json()['taskid']
    # print(task_id)
    if 'success' in res.content.decode('utf-8'):
        print('task creat success!')
        task_scan_url = 'http://127.0.0.1:8775/option/' + task_id + '/set'
        scan_res = requests.post(task_scan_url, data=json.dumps(data), headers=headers).content.decode('utf-8')
        # print(scan_res)
        if 'success' in scan_res:
            print('set success!')
            task_start_url = 'http://127.0.0.1:8775/scan/' + task_id + '/start'
            start_res = requests.post(task_start_url, data=json.dumps(data), headers=headers).content.decode('utf-8')
            #print(start_res)
            if 'success' in start_res:
                #print('start success!')
                while 1:
                    task_status_url = 'http://127.0.0.1:8775/scan/' + task_id + '/status'
                    task_status_res = requests.get(task_status_url).content.decode('utf-8')
                    #print(task_status_res)
                    if 'running' in task_status_res:
                        print(url+'\033[1;36m-->scan running!')
                        print('\033[0m')
                        pass
                    else:
                        task_data_url = 'http://127.0.0.1:8775/scan/' + task_id + '/data'
                        task_data_res = requests.get(task_data_url).content.decode('utf-8')
                        print(task_data_res)
                        with open(r'scan_result.txt','a+') as f:
                            f.write(url+'\n')
                            f.write(task_data_res+'\n')
                            f.write('*************************************************************sqlmapapi scan finish*******************************************************************'+'\n')
                            f.close()
                            task_delete_url = 'http://127.0.0.1:8775/task/' + task_id + '/delete'
                            task_delete = requests.get(task_delete_url)
                        break
                print(url+'\033[31m---->扫描完成，扫描结果已生成，请注意查看！')
                print('\033[0m')
                time.sleep(3)

if __name__ == '__main__':
    for url in open('url.txt'):
        url=url.replace('\n','')
        sqlmapapi(url)
