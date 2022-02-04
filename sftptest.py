from paramiko import SSHClient, SFTPClient, Transport, RSAKey, AutoAddPolicy
import os

private = RSAKey.from_private_key_file("/Users/janjaap/.ssh/id_rsa")
username = 'deb7255'
host = 'savatarian.com'

localdir = "/Users/janjaap/PycharmProjects/test/"
remotedir = "/home/deb7255/test/"

#Even wat commentaar....
# En nog wat...
def get_files():
    files = []
    for r, d, f in os.walk(localdir):
        for file in f:
            localfile = os.path.join(r, file)
            remotefile = os.path.join(remotedir + r[len(localdir):], file)
            files.append({"localfile": localfile, "remotefile": remotefile})
    return files

def get_directories(localdir):
    directories = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(localdir):
        directories.append(remotedir + r[len(localdir):])
    return directories

def create_dirs(sftp, dir):
    try:
        sftp.chdir(dir)
    except IOError:
        sftp.mkdir(dir)
        print("directory created: ", dir)


def sftp_client():
    con = Transport('savatarian.com', 22)
    con.connect(None, username=username, pkey=private)
    sftp = SFTPClient.from_transport(con)
    return sftp


def ssh_client():
    # Create an instance
    ssh = SSHClient()
    # Load system HostKeys key
    ssh.load_system_host_keys()
    # Automatically add a policy to save the host name and key information of the remote host. If not added, the host not recorded in the local knowledge hosts file will not be able to connect. It is rejected by default
    ssh.set_missing_host_key_policy(AutoAddPolicy())
    #Connect to remote host
    ssh.connect(host, port=22, username=username, pkey=private)
    #Executive order
    stdin, stdout, stderr = ssh.exec_command('pwd')
    print(stdout.read().decode('utf-8'))
    #Close connection
    ssh.close()

if __name__ == '__main__':
    # ssh_client()
    # sftp_client()
    sftp = sftp_client()
    # print(directories)
    for d in get_directories(localdir):
        create_dirs(sftp, d)
    print(get_files())
    for t in get_files():
        sftp.put(t["localfile"], t["remotefile"])
        print("Tranferred: ", t["localfile"]), t["remotefile"]
