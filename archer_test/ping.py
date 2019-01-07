import json
import subprocess
from subprocess import CalledProcessError
__author__ = 'Sasha'


def write_to_file(response):
    with open('ip.txt', 'w') as log:
        json.dump(response, log, indent=2)


def main(host, count):
    try:
        response = subprocess.check_output(
            ['ping', '-c', count, host],
            stderr=subprocess.STDOUT,
            universal_newlines=True)

        response_time_list = []
        for line in response.splitlines():

            lost = 0
            if line.startswith('PING'):
                host = line.split('(')[0].split(' ')[1]
                ip = line.split('(')[1].split(')')[0]
            if line.find('icmp_seq=') > 0:
                time = line.split('time=')[1].split(' ')[0]
                response_time_list.append(float(time))
            if line.find('no answer yet') > 0:
                lost += 1

        avg_time = sum(response_time_list)/int(len(response_time_list))
        try:
            loss_percent = lost / (sum(response_time_list) + lost) * 100
        except ZeroDivisionError:
            loss_percent = 0

        data = {'host': host, 'ip': ip, 'average_time': avg_time, 'loss': str(loss_percent) + '%'}
        write_to_file(data)
    except CalledProcessError as e:
        print e.output

if __name__ == "__main__":
    main('www.google.com', '5')
