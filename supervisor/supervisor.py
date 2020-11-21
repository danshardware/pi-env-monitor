import time
from datetime import timedelta
import subprocess
import threading, time, signal
import display
import sensors
import os
from sampleRing import sampleRing
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime
WAIT_TIME_SECONDS = 1

def getStatusText():
    if os.name == 'nt':
        return "10.10.10.10 900/2048MB"

    # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
    # IP Address
    cmd = "hostname -I"
    IP = subprocess.check_output(cmd, shell = True )
    IP = IP.decode('utf-8').strip()

    # CPU Load
    #cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
    #CPU = subprocess.check_output(cmd, shell = True )

    # Memory Usage
    cmd = "free -m | awk 'NR==2{printf \"%s/%sMB\", $3,$2 }'"
    MemUsage = subprocess.check_output(cmd, shell = True )
    MemUsage = MemUsage.decode('utf-8')

    # Disk Usage
    #cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
    #Disk = subprocess.check_output(cmd, shell = True )
    
    return str(IP) + ' ' + MemUsage

def everySecond():
    # runs once per second
    # Sample the data and add to our buffer
    data = sensors.sample()

    # store the data
    temperatureSamples.push(data.temperature)
    humiditySamples.push(data.temperature)
    pressureSamples.push(data.pressure)

    # write it to the display 
    display.displayStatus(data.temperature, data.humidity, getStatusText())

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Gather the data we are sending back
        data = {
            "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        }
        try:
            data["temperature"] = temperatureSamples.stats()
            data["humidity"] = humiditySamples.stats()
            data["pressure"] = pressureSamples.stats()
        except:
            self.send_header("Content-type", "text/plain")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b'Server error')
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('UTF-8'))

class ProgramKilled(Exception):
    pass

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        
    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)


def signal_handler(signum, frame):
    raise ProgramKilled

def startWebServer(port=8081):
    httpd = HTTPServer(('localhost', port), SimpleHTTPRequestHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=everySecond)
    job.start()
    
    temperatureSamples = sampleRing(300)
    humiditySamples = sampleRing(300)
    pressureSamples = sampleRing(300)

    # start the web server
    webServer = threading.Thread(name='webServer',
        target=startWebServer)
    webServer.setDaemon(True)
    webServer.start()

    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print ("Program killed: running cleanup code")
              job.stop()
              break
