#coding:utf-8

import threading
import re
from Queue import Queue

SHARE_Q = Queue()
_WORKER_THREAD_NUM = 10



class MyThread(threading.Thread) :

    def __init__(self, func) :
        super(MyThread, self).__init__()
        self.func = func

    def run(self) :
        self.func()


def getpopinfo():
    global SHARE_Q
    thread_id_sub_str = ''
    user_info = ''
    subject_info = ''
    time_info = ''
    ip_info = ''
    while not SHARE_Q.empty():
        line_num = SHARE_Q.get()
        # print 'start' + str(line_num) + '\n'
        file_in_t = open('C:\\git\\getpopinfo\\console.log', 'r')
        file_out_t = open('C:\\git\\getpopinfo\\result.txt','a')
        m=0
        for line in file_in_t:
            m = m + 1
            if line_num == m:
                thread_id_sub_str = thread_id_sub = re.search('\[(.*?)\-',line,0).group(1)
                # print thread_id_sub_str + 'start' + str(m) + '\n'


            if  thread_id_sub_str != '' and thread_id_sub_str in line:

                if 'R:  USER' in line:
                    user_info = re.search('R:(.*?)\n',line,0).group(1)

                if 'POP3 CITask StateMachine' in line:
                    time_info = re.search('\](.*?)POP3',line,0).group(1)
                    ip_info = re.search('(\d+\.\d+\.\d+\.\d+)',line,0).group(1)

                if 'S:  Subject:' in line:
                    subject_info = re.search('S:(.*?)<CRLF>',line,0).group(1)
                    print user_info + ',' + time_info + ',' + ip_info + ',' + subject_info+'\n'


                if 'R:  QUIT' in line:
                    # print thread_id_sub_str + 'end ' + str(m) + '\n'

                    # file_out_t.write(subject_info+','+user_info+','+time_info+','+ip_info)
                    # file_out_t.write('\n')

                    file_in_t.close()
                    file_out_t.close()
                    return 0


def main():
    global SHARE_Q
    threads = []
    file_in = open('C:\git\getpopinfo\console.log','r')
    n = 0
    for line in file_in:
        n = n + 1
        if 'Lotus Notes POP3 server version' in line:
            SHARE_Q.put(n)


    for i in xrange(_WORKER_THREAD_NUM):
        thread = MyThread(getpopinfo)
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()