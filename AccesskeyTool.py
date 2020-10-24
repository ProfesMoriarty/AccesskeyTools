#!/usr/bin/env python
#coding=utf-8

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkrds.request.v20140815.DescribeDBInstancesRequest import DescribeDBInstancesRequest
from aliyunsdkecs.request.v20140526.DescribeInstancesRequest import DescribeInstancesRequest
from aliyunsdkrds.request.v20140815.DescribeBackupsRequest import DescribeBackupsRequest
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')

region_list = ['cn-hangzhou', 'cn-shanghai', 'cn-shanghai-finance-1', 'cn-qingdao', 'cn-beijing', 'cn-zhangjiakou',
               'cn-huhehaote', 'cn-wulanchabu', 'cn-north-2-gov-1', 'cn-shenzhen', 'cn-shenzhen-finance-1', 'cn-heyuan',
               'cn-chengdu', 'cn-hongkong', 'ap-southeast-1', 'ap-southeast-2', 'ap-southeast-3', 'ap-southeast-5',
               'ap-northeast-1', 'ap-south-1', 'eu-central-1', 'eu-west-1', 'us-west-1', 'us-east-1', 'me-east-1']

AccessKeyId = 'xxx'
AccessKeySecret = 'xxx'

#查询所有RDS信息
def queryAllRDS():
    print("-------------- RDS 查询中 --------------")
    for region in region_list:
        try:
            client = AcsClient(AccessKeyId, AccessKeySecret, region)

            request = DescribeDBInstancesRequest()
            request.set_accept_format('json')

            response = client.do_action_with_exception(request)
            #print(response)
            result = json.loads(response)
            if result['TotalRecordCount'] > 0:
                #print  region +  " 查询到 " + result['TotalRecordCount'] + "台RDS"
                print("%s 查询到 %d 台RDS：" % (region , result['TotalRecordCount']))
                print("--------------------------------------")
                for item in result['Items']['DBInstance']:
                    print("RDS名:%s" % (item['DBInstanceId']))
                    print("类型:%s" % (item['Engine']))
                    print("当前状态:%s" % (item['DBInstanceStatus']))
                    print("描述信息:%s" % (item['DBInstanceDescription']))
                    print("创建时间:%s" % (item['CreateTime']))
                    print("过期时间:%s" % (item['ExpireTime']))
                    print("--------------------------------------")

            else:
                #{"TotalRecordCount":0,"PageRecordCount":0,"RequestId":"42F62ACF-266D-49C7-8ED5-07AA6A7C00B0","PageNumber":1,"Items":{"DBInstance":[]}}
                print("%s 未查询到RDS信息" % (region))
        except Exception as e:
            print(e)
            print("查询 %s 出现错误" % (region))
    print("-------------- RDS 查询完成 --------------")
        
#查询所有ECS信息
def queryAllECS():
    print("-------------- ECS 查询中 --------------")
    for region in region_list:
        try:
            client = AcsClient(AccessKeyId, AccessKeySecret, region)

            request = DescribeInstancesRequest()
            request.set_accept_format('json')

            response = client.do_action_with_exception(request)
            #print(response)
            result = json.loads(response)
            if result['TotalCount'] > 0:
                #print  region +   " 查询到 " + str(result['TotalCount']) + "台ECS"
                print("%s 查询到 %d 台ECS：" % (region , result['TotalCount']))
                print("--------------------------------------")
                for item in result['Instances']['Instance']:
                    print("实例名:%s" % (item['InstanceName']))
                    print("当前状态:%s" % (item['Status']))
                    if(len(item['PublicIpAddress']['IpAddress'])):
                        print("公网IP:%s" % (item['PublicIpAddress']['IpAddress'][0]))
                    else:
                        print("公网IP:%s" % (item['EipAddress']['IpAddress']))
                    print("内网IP:%s" % (item['VpcAttributes']['PrivateIpAddress']['IpAddress'][0]))
                    print("系统:%s" % (item['OSName']))
                    print("CPU:%d" % (item['Cpu']))
                    print("内存:%d" % (item['Memory']))
                    print("创建时间:%s"% (item['StartTime']))
                    print("过期时间:%s"% (item['ExpiredTime']))
                    print("--------------------------------------")

            else:
                print ("%s 未查询到ECS信息" % (region))
        except Exception as e:
            print(e)
            print("查询 %s 出现错误" % (region))
    print("-------------- ECS 查询完成 --------------")


#查询RDS备份信息
def queryRdsBackup(rdsId,rdsRegion):
    client = AcsClient(AccessKeyId, AccessKeySecret, rdsRegion)

    request = DescribeBackupsRequest()
    request.set_accept_format('json')

    request.set_DBInstanceId(rdsId)

    response = client.do_action_with_exception(request)
    print(response)

#执行命令
def runCommand():
    print("test")

if __name__ == "__main__":
    queryAllECS()
    queryAllRDS()
    
