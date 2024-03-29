from Appium_test.appium_sync.multi_appium import appium_start
from Appium_test.appium_sync.multi_devices import appium_desire
from Appium_test.appium_sync.check_port import *
from time import sleep
import multiprocessing

devices_list=['127.0.0.1:62001', '127.0.0.1:62025']

def start_appium_action(host, port):
    """检测端口是否被占用，如果没有被占用则启动appium服务"""
    if check_port(host,port):
        appium_start(host,port)
        return True
    else:
        print('appium %s start fail' %port)


def start_devices_action(udid, port):
    """先检测appium服务是否启动成功，启动成功则再启动App，否则释放端口"""
    host='127.0.0.1'
    if start_appium_action(host,port):
        appium_desire(udid, port)
    else:
        release_port(port)

def appium_start_sync():
    """并发启动appium服务"""
    print("=====appium_start_sync===")
    appium_process = []
    for i in range(2):
        host = '127.0.0.1'
        port = 4723 + 2 * i
        appium = multiprocessing.Process(target=appium_start,
                                         args=(host, port))
        appium_process.append(appium)

    for appium in appium_process:
        appium.start()
    for appium in appium_process:
        # 执行完成后关闭进程
        appium.join()

    sleep(5)

def devices_start_sync():
    """并发启动设备"""
    print('=====devices_start_sync=====')
    # 构建desired进程组
    desired_process = []

    # 加载desired进程
    for i in range(len(devices_list)):
        port = 4723 + 2 * i
        desired = multiprocessing.Process(target=appium_desire,
                                          args=(devices_list[i], port))
        desired_process.append(desired)


    # 启动多设备执行测试
    for desired in desired_process:
        desired.start()
    for desired in desired_process:
        desired.join()

if __name__ == '__main__':
    appium_start_sync()
    devices_start_sync()


