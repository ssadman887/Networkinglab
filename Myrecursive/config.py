# config.py

LOCAL_SERVER = {
    'IP': 'localhost',
    'PORT':  8000,
    'BUFFER_SIZE':  1024,
    'FORMAT': "utf-8",
    'TTL':  3,
    'ROOT_PORT':  8001
}

ROOT_SERVER = {
    'IP': 'localhost',
    'PORT':  8001,
    'BUFFER_SIZE':  1024,
    'FORMAT': "utf-8",
    'TTL':  6,
    'TLD_PORT':  8002,
    'ROOT_RECORDS': {
        'bd':  8002,
        'com':  8002
    }
}

TLD_SERVER = {
    'IP': 'localhost',
    'PORT':  8002,
    'BUFFER_SIZE':  1024,
    'FORMAT': "utf-8",
    'TTL':  3,
    'AUTH_PORT':  8003
}

AUTH_SERVER = {
    'IP': 'localhost',
    'PORT':  8003,
    'BUFFER_SIZE':  1024,
    'FORMAT': "utf-8",
    'AUTH_RECORDS': {
        'cse.du.ac.bd': '192.0.2.3',
        'google.com': '142.250.193.110',
        'ns1.cse.du.ac.bd': '192.0.2.1',
        'ns2.cse.du.ac.bd': '192.0.2.2',
        'mail.cse.du.ac.bd': '192.0.2.4'
    }
}
