import argparse
import threading
import time
import os
from mcstatus import JavaServer

parser = argparse.ArgumentParser(description='minecraft server tester')
parser.add_argument("-i", "--input_file", type=str, help="IPs file")
args = parser.parse_args()

masscan = []

input_file = args.input_file


fileHandler = open(input_file, "r")
listOfLines = fileHandler.readlines()
fileHandler.close()

for line in listOfLines:
    if line.strip()[0] != "#":
        masscan.append(line.strip().split(' ', 4)[3])


def split_array(mas, n):
    return [mas[i::n] for i in range(n)]


threads = int(input('threads: '))

time.sleep(2)

if len(masscan) < int(threads):
    threads = len(masscan)

split = list(split_array(masscan, threads))

exitFlag = 0


class MyThread(threading.Thread):
    def __init__(self, threadid, name):
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.name = name

    def run(self):
        print("Starting Thread " + self.name)
        print_time(self.name)
        print("Exiting Thread " + self.name)


def print_time(threadname):
    for z in split[int(threadname)]:
        if exitFlag:
            threadname.exit()
            print("1")
        try:
            ip = z
            server = JavaServer(ip, 25565)
            status = server.status()
        except Exception as ex:
            print(ex)
        else:
            print("Found server: " + ip + " " + status.version.name + " " + str(status.players.online) + " " + str(
                status.players.max))
            text_file = open("out.txt", "a")
            text_file.write(f"ip: {str(ip)} ver: {str(status.version.name)} "
                            f"protokol: {str(status.version.protocol)} max: {status.players.max} "
                            f"now: {status.players.online} lat: {status.latency} "
                            f"description {status.description}")
            text_file.write(os.linesep)
            text_file.close()


for x in range(threads):
    MyThread(x, str(x)).start()
