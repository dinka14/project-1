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


def execute(host, user, password, command):
    connect = ConnectBySSH(host, user, password)
    stdin, stdout, stderr = connect.connect().exec_command(command)
    data = stdout.read()
    print(type(data))


execute('smoke.int.zone', 'root', '1q2w3e', 'ls')
