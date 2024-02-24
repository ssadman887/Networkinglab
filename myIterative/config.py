# config.py

IP = 'localhost'
LOCAL_PORT =  8000
ROOT_PORT =  8001
TLD_PORT =  8002
AUTH_PORT =  8003
BUFFER_SIZE =  1024
FORMAT = "utf-8"

root_records = {
    'bd': TLD_PORT,
    'com': TLD_PORT,
}

tld_records = {
    'cse.du.ac.bd': AUTH_PORT,
    'google.com': AUTH_PORT,
}

auth_records = {
    'cse.du.ac.bd': '192.0.2.3',
    'google.com': '142.250.193.110',
    'ns1.cse.du.ac.bd':'192.0.2.1',
    'ns2.cse.du.ac.bd':'192.0.2.2',
    'mail.cse.du.ac.bd':'192.0.2.4'
}
