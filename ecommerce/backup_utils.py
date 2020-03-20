import os
import subprocess
import sys
from django.conf import settings

def run_shell_command(command):
    proc_list = []
    proc = subprocess.Popen(command, 
        shell=True, 
        stdin=sys.stdin, 
        stdout=subprocess.PIPE, 
        stderr=sys.stderr) 
    stdout = proc.communicate()[0]
    proc_list.append(proc)
    proc.wait(timeout=500)
    return 

def backup_and_download_live_db():
    print("Tapping heroku for live db...")
    backups_dir = os.path.join(settings.BASE_DIR, "backups")
    os.makedirs(backups_dir, exist_ok=True)
    path = os.path.join(settings.BASE_DIR, "data", "dumps", 'latest.dump')
    proc_list = []
    # chained command for backup and downloading 
    command = f'heroku pg:backups:capture -a salt-eu; heroku pg:backups:download -o data/dumps/latest.dump -a salt-eu' 
    command_done = run_shell_command(command)
    return "Done"

def load_in_local_backup_db():
    print("Loading previous database.")
    path = os.path.join(settings.BASE_DIR, "data", "dumps", 'latest.dump')
    if not os.path.exists(path):
        backup_and_download_live_db()
        print("Backup didn't exist. Run again after it does.")
        return
    command = f'pg_restore --verbose --clean --no-acl --no-owner -h localhost -U roma -d saltdb -p 5433 data/dumps/latest.dump' 
    command_done = run_shell_command(command)
    return "Done"