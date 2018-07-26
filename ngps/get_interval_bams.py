import ConfigParser as cp
import subprocess as sp
import csv
import os
from time import sleep

def request_file(config, filename, request_name):
    cmd = '''java -jar ~/sw/bin/EGA/EgaDemoClient.jar -p {USER} {PASSWORD} -rf {FILE} -re {ENCRYPTION_KEY}  -label {REQUEST_NAME}'''.format(
        USER=config.get('LOGIN','userName'), 
        PASSWORD=config.get('LOGIN','passWord'),
        FILE=filename, ENCRYPTION_KEY=config.get('KEYS','ENCRYPTION_KEY'),
        REQUEST_NAME=request_name)

    proc = sp.Popen(cmd, shell=True)
    proc.wait()
    sleep(10)

def download_request(config, request_name, stream_no):
    cmd = '''java -jar ~/sw/bin/EGA/EgaDemoClient.jar -p {USER} {PASSWORD} -dr {REQUEST_NAME} -nt {STREAMS}'''.format(
        USER=config.get('LOGIN','userName'), 
        PASSWORD=config.get('LOGIN','passWord'), REQUEST_NAME=request_name, STREAMS=stream_no)

    proc = sp.Popen(cmd, shell=True)
    proc.wait()

def decrypt_file(config, file_path):
    cmd = '''java -jar ~/sw/bin/EGA/EgaDemoClient.jar -p {USER} {PASSWORD} -dc {FILEPATH} -dck {ENCRYPTION_KEY}'''.format(
        USER=config.get('LOGIN','userName'), 
        PASSWORD=config.get('LOGIN','passWord'), FILEPATH=file_path, 
        ENCRYPTION_KEY=config.get('KEYS','ENCRYPTION_KEY'))

    proc = sp.Popen(cmd, shell=True)
    proc.wait()


def create_file_dict(file_path):
    dir_path = os.path.split(file_path)[0]
    rtn_dct = {}
    with open(file_path, 'r') as inf:
        for line in inf:
            if 'EGAF' in line:
                fname = (line.split(' ')[6])
                rtn_dct[fname] = os.path.join(dir_path, fname)
    return rtn_dct, dir_path
                
def main():
    fdct, dir_path = create_file_dict('/scratch/ngps/interval/file_list_ega')
    config = cp.ConfigParser()
    config.read('/efs/jmcg/unchecked_in_auth/ega_security.cfg')

    keys = list(fdct.keys())
    request_name = 'First_ten_request'
    


    for i in range(10):
        current_file = keys[i]

        request_file(config, current_file, request_name)

    download_request(config, request_name, 15)

    files_to_decrypt = [f for f in os.listdir(dir_path) if '_EGAR' in f]

    for fp in files_to_decrypt:
        decrypt_file(config, fp)


if __name__ == '__main__':
    main()

