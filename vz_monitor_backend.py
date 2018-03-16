import paramiko
import json

SSHPort = 22


class ConnectBySSH:
    client = paramiko.SSHClient()

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        ConnectBySSH.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ConnectBySSH.client.connect(hostname=self.host, username=self.user, password=self.password, port=SSHPort)
        return ConnectBySSH.client

    def __del__(self):
        ConnectBySSH.client.close()


class ExecuteCommand:
    def __init__(self, host, user, password):
        self.connect = ConnectBySSH(host, user, password)

    def check_ve_is_available(self, ve_name):
        connect = self.connect.connect()
        stdin, stdout, stderr = connect.exec_command('prlctl list -o name ' + ve_name)
        data = stdout.read()
        listq = data.split()
        dictq = dict(zip(listq[::2], listq[1::2]))
        if dictq == {}:
            print 'There is no ve with this name on node'
        else:
            return True

    def list_ve(self):
        connect = self.connect.connect()
        stdin, stdout, stderr = connect.exec_command("prlctl list -o name,status | sed '1d'")
        data = stdout.read()
        listq = data.split()
        dictq = dict(zip(listq[::2], listq[1::2]))
        print(dictq)

    def stop_ve(self, ve_name):
        connect = self.connect.connect()
        if not ExecuteCommand.check_ve_is_available(self, ve_name):
            return
        stdin, stdout, stderr = connect.exec_command('prlctl stop ' + ve_name + ' && ' + 'prlctl list -a ' + ve_name)
        data = stdout.read()
        print(data)

    def start_ve(self, ve_name):
        connect = self.connect.connect()
        if not ExecuteCommand.check_ve_is_available(self, ve_name):
            return
        stdin, stdout, stderr = connect.exec_command('prlctl start ' + ve_name + ' && ' + 'prlctl list -a ' + ve_name)
        data = stdout.read()
        print(data)

    def set_vnc_password(self, ve_name, vnc_password):
        connect = self.connect.connect()
        if not ExecuteCommand.check_ve_is_available(self, ve_name):
            return
        stdin, stdout, stderr = connect.exec_command('prlctl stop ' + ve_name + ' && ' + 'prlctl set ' + ve_name +
                                                     ' --vnc-mode auto --vnc-passwd ' + vnc_password + ' && '
                                                     + 'prlctl start ' + ve_name)
        stdout.read()
        stdin, stdout, stderr = connect.exec_command('prlctl list -i -j ' + ve_name)
        data = stdout.read()
        j = json.loads(data[1:len(data) - 2])

        while True:
            try:
                if j["Remote display"]["port"]:
                    port = j["Remote display"]["port"]
                    break
            except KeyError:
                pass
            stdin, stdout, stderr = connect.exec_command('prlctl list -i -j ' + ve_name)
            data = stdout.read()
            j = json.loads(data[1:len(data) - 2])
        print 'Connect to VNC:', 'Compute node', self.connect.host, 'port', port, 'VNC password', vnc_password


ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').set_vnc_password('ATest-dc84b23d647a.aqa.int.zone', '1q2w3e4r')
# ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').check_ve_is_available('ATest-dc84b23d647a.aqa.int.zone')
# ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').list_ve()
# ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').stop_ve('!srv-6564eea3df74.aqa.int.zone')
# ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').start_ve('!srv-6564eea3df74.aqa.int.zone')
