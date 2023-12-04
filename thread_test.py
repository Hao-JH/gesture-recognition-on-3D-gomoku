import threading
import time

x = 0

# 定义函数f1，每隔一秒给x+1
def f1():
    global x
    while True:
        x += 1
        time.sleep(0.1)
        if x > 20:
            break
        

# 定义函数f2，每隔两秒输出一次x，按下回车键结束循环
def f2():
    global x
    while True:
        print(x)
        if x >20:
            break
        time.sleep(0.2)

# 创建线程
thread1 = threading.Thread(target=f1)
thread2 = threading.Thread(target=f2)

# 启动线程
thread1.start()
thread2.start()

# 等待线程结束
thread1.join()
thread2.join()