import paramiko

port = 22


class ConnectBySSH:
    client = paramiko.SSHClient()

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password

    def connect(self):
        ConnectBySSH.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ConnectBySSH.client.connect(hostname=self.host, username=self.user, password=self.password, port=port)
        return ConnectBySSH.client

    def __del__(self):
        ConnectBySSH.client.close()


class ExecuteCommand:
    def __init__(self, host, user, password):
        self.connect = ConnectBySSH(host, user, password)

    def list_ve(self,command):
        connect = self.connect.connect()
        stdin, stdout, stderr = connect.exec_command(command)
        data = stdout.read()
        print(data[77:])

    def stop_ve(self, ve_name):
        connect = self.connect.connect()
        stdin, stdout, stderr = connect.exec_command('prlctl stop ' + ve_name + ' && ' + 'prlctl list -a ' + ve_name)
        data = stdout.read()
        print(data)

    def start_ve(self, ve_name):
        connect = self.connect.connect()
        stdin, stdout, stderr = connect.exec_command('prlctl start ' + ve_name + ' && ' + 'prlctl list -a ' + ve_name)
        data = stdout.read()
        print(data)


ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').list_ve('prlctl list -a')
#ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').stop_ve('srv-6564eea3df74.aqa.int.zone')
#ExecuteCommand('smoke.int.zone', 'root', '1q2w3e').start_ve('srv-6564eea3df74.aqa.int.zone')