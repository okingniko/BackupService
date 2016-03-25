#!/usr/bin/env python
# -*- coding=utf-8 -*-
#
# Author: zrwang(zrwang1993@126.com)
# Program:
#   1. Backup(Upload) files to the specified server.
#   2. Download necessary files from server.
#   3. Tips: Appropriate setting can be seen at ./MainConf.json(default conf file)
#            Output log can be seen at ./backup.log(default backup log file)
# Changelog:
#   1. 3/23/2016 Initialization and Add Backup Mode.
# TODO:
#   1. Add Download Mode.
#   2. Add CMD Argument parsing Or Add Graphical interface.
#   3. Etc.
# Contribution: xxli(testing)
#

import paramiko
import os
import json
import logging

class Backup():
    def __init__(self, conf_file='./MainConf.json',log_file='./backup.log'):
        self.conf_file = conf_file
        self.log_file = log_file

    def setlogger(self, log_file):
        log_fmt = '%(levelname)s - %(asctime)s - %(message)s'
        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format=log_fmt)

    def run(self):
        self.setlogger(self.log_file)
        with open(self.conf_file, 'r') as f:
            data = json.load(f)
        # Process each configure for backup_conf
        for back_conf in data['backup_conf']:
            local_dir = back_conf['local_dir'].encode('utf-8')
            # local host can be any platform.
            if os.path.isdir(local_dir) and local_dir[-1] != os.sep:
                local_dir += os.sep
            local_files = back_conf['local_files']

            server_ip = back_conf['server_ip'].encode('utf-8')
            server_port = 22
            remote_dir = back_conf['remote_dir'].encode('utf-8')
            # remote server under linux environ.
            if remote_dir[-1] != '/':
                remote_dir += os.sep

            user_name = back_conf['user_name']
            user_passwd = back_conf['user_password']
            # print type(local_dir), server_ip, server_port, type(remote_dir), user_name, user_passwd

            try:
                t = paramiko.Transport((server_ip, server_port))
                t.connect(username=user_name, password=user_passwd)
                sftp = paramiko.SFTPClient.from_transport(t)
    
                # if remote_dir not exist, make it.
                try:
                    sftp.normalize(remote_dir)
                except Exception as e:
                    sftp.mkdir(remote_dir)
    
                # backup local files
                for localf in local_files:
                    remote_file = os.path.join(remote_dir, os.path.split(localf)[1])
                    try:
                        sftp.put(localf, remote_file)
                    except Exception as e:
                        logging.error("Backup localfile %s: %s", localf, e)
                        print "ERROR: Backup localfile %s: %s" % (localf, e)
                    logging.info("Backup localfile %s to %s on %s ...", localf, remote_file, server_ip)
                    print "INFO: Backup localfile %s to %s on %s ..." % (localf, remote_file, server_ip)
    
                # backup files under local_dir(recursively).
                for root, dirs, files in os.walk(local_dir):
                    for f in files:
                        local_file = os.path.join(root, f)
                        relative_path = local_file.replace(local_dir,'').replace('\\', '/')
                        remote_file = os.path.join(remote_dir, relative_path)
                        # print local_file, type(relative_path), remote_file
                        try:
                            sftp.put(local_file, remote_file)
                        except Exception as e:
                            remote_curr_dir = os.path.split(remote_file)[0]
                            sftp.mkdir(remote_curr_dir)
                            logging.info("Create directory %s on %s ...",remote_curr_dir, server_ip)
                            print "INFO: Create directory %s on %s ..." % (remote_curr_dir, server_ip)
                            sftp.put(local_file, remote_file)
    
                        logging.info("Backup localfile %s to %s on %s ...",local_file, remote_file, server_ip)
                        print "INFO: Backup localfile %s to %s on %s ..." % (local_file, remote_file, server_ip)
                t.close()
            except Exception as e:
                logging.error("Remote host %s %s",server_ip, e)
                print "ERROR: Remote host %s %s" % (server_ip, e)

class Download:
    def __init__(self, conf_file='./MainConf.json'):
        pass

    def run(self):
        print "Download Method are under construction..."
        pass

def printintro():
    print '''
             * ,MMM8&&&.            *
                  MMMM88&&&&&    .
                 MMMM88&&&&&&&
     *           MMM88&&&&&&&&
                 MMM88&&&&&&&&
                 'MMM88&&&&&&'
                   'MMM8&&&'      *
          |\___/|
          )     (             .              '
         =\     /=
           )===(       *
          /     \
          |     |
         /       \
         \       /
  _/\_/\_/\__  _/_/\_/\_/\_/\_/\_/\_/\_/\_/\_
  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |
  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |
  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |
  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |

  Please Choose the Number of the method:
    1. Backup
    2. Download
    3. :-)
  '''

def main():
    printintro()
    try:
        num = int(input("The number: "))
    except Exception as e:
        print "ERROR: %s" % e

    if num == 1:
        backup = Backup()
        backup.run()
    elif num == 2:
        download = Download()
        download.run()
    elif num == 3:
        print "If you have any idea, Please contact me at zrwang1993@126.com"
    else:
        print "Please follows the instructions..."

    print "More details can be seen at 'backup.log'..."

if __name__ == '__main__':
    main()
