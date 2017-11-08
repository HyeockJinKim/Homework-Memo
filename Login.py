import codecs


class Login:
    def __init__(self):
        self.login_data = []

    def login(self, id_val, pw_val):
        self.login_data.append(id_val)
        self.login_data.append(pw_val)

    def load_login_data(self):
        decoder = codecs.getdecoder('hex')
        file = open('./loginData.bin', 'rb')
        id_pw_value = bytes(decoder(file.read())[0]).decode()
        file.close()
        self.login_data.append(id_pw_value.split('\n')[0])
        self.login_data.append(id_pw_value.split('\n')[1])

    def save_login_data(self):
        encoder = codecs.getencoder('hex')
        id_pw_value = encoder(str(self.login_data[0]+ '\n' + self.login_data[1]).encode())[0]
        file = open('./loginData.bin', 'wb')
        file.write(id_pw_value)
        file.close()