import argparse  # import argparse for the cli args
import os  # import os for new line breaks
import threading  # import threading for multi threads

from mcstatus import JavaServer  # import mcstatus to check minecraft server status

# parse cli input
parser = argparse.ArgumentParser(description='minecraft server tester')
parser.add_argument("-i", "--input_file", type=str, help="IPs file")
args = parser.parse_args()
input_file = args.input_file


# set list for ips
masscan = []


# open file and create a list of lines
fileHandler = open(input_file, "r")
listOfLines = fileHandler.readlines()
fileHandler.close()

# grep only the ip from the lines
for line in listOfLines:
    if line.strip()[0] != "#":
        masscan.append(line.strip().split(' ', 4)[3])


# split the array for avery thread
def split_array(mas, n):
    return [mas[i::n] for i in range(n)]


# wait for threat input
threads = int(input('threads: '))

# limit the threads to the length of the ips
if len(masscan) < int(threads):
    threads = len(masscan)

# use the split function
split = list(split_array(masscan, threads))


# class for threads
class MyThread(threading.Thread):
    def __init__(self, threadid, name):
        threading.Thread.__init__(self)
        self.threadID = threadid
        self.name = name

    def run(self):
        print("Starting Thread " + self.name)
        check(self.name)
        print("Exiting Thread " + self.name)


# check the server via the mcstatus api

def check(threadname):
    for z in split[int(threadname)]:
        try:
            # check if server is online
            ip = z
            server = JavaServer(ip, 25565)
            status = server.status()
        except Exception as ex:
            # error behaviour
            print(f"er: {ex}")
        else:
            # print and save found server
            print("Found server: " + ip + " " + status.version.name + " " + str(status.players.online) + " " + str(
                status.players.max))
            text_file = open("out.txt", "a")
            text_file.write(f"ip: {str(ip)} ver: {str(status.version.name)} "
                            f"protokol: {str(status.version.protocol)} max: {status.players.max} "
                            f"now: {status.players.online} lat: {status.latency} "
                            f"description {status.description}")
            text_file.write(os.linesep)
            text_file.close()


# start the threads
for x in range(threads):
    MyThread(x, str(x)).start()
