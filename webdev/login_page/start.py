import os
import subprocess
from time import sleep

if __name__ == "__main__":
    try:
        os.chdir('frontend')
        p_front = subprocess.Popen(['python', '-m', 'http.server', '80'],
                                   stdout=open('frontend.log', 'w'), stderr=subprocess.STDOUT, bufsize=0)
        print('Frontend started')
        os.chdir('../backend')
        p_back = subprocess.Popen(['uvicorn', 'main:app', '--reload'],
                                  stdout=open('backend.log', 'w'), stderr=subprocess.STDOUT, bufsize=0)
        print('Backend started')
        while True:
            sleep(10)
    except KeyboardInterrupt:
        print('Stopping processes')
        p_front.kill()
        p_back.kill()
