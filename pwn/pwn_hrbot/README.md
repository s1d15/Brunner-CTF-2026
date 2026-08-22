# HRBot

Hello and welcome to the `pwn` category! This challenge is designed to introduce you to one of the most know topics of binary exploitation: buffer overflows!

In this simple case, the HRBot will guide you along the way when you attempt to exploit the program.

I sincerely hope you have fun! If you need any pointers on how to get started, follow the next steps or view the resources at the end of the file.

The challenge is built with many hints in the output to avoid having to reverse engineer the binary, too much.

## 1. Run the Program Normally

Try running the program normally first and use it like a normal employee:

```bash
./hrbot
```

Choose option `1`, then type a short message:

```text
1
hello HR
```

You should see HRBot print a case ID, log your case, and then fire you anyway.
Very efficient.

## 2. Make It Crash

Notice how the program says the input is limited to 64 characters?
Let's try figuring out whether this limit is actually enforced.

Try sending around 100 characters instead now.
Notice the last extra line?  
`zsh: segmentation fault  ./hrbot`

This means we made the program crash - which is good news!
Our input was written to a fixed-sized buffer in the code, but we wrote more than
it could contain and our input *overflowed* into nearby memory and broke something important.

## 3. What Is Happening?

When a function runs, it stores local variables on the *stack*.
In simple terms, the stack for the vulnerable function looks like this:

```text
lower addresses

[ case_notes buffer: 64 bytes   ]
[ other saved function data     ]
[ return address                ]

higher addresses
```

The program asks for "64 characters", but internally it uses the unsafe function
`gets()`. `gets()` is unsafe and does not know when to stop.
If you type more than 64 bytes, your input continues past the buffer
and starts overwriting the saved data after it.

The most important thing after the buffer is the **return address**.

The return address tells the CPU where to jump when the current function is
finished. If we overwrite it, we can choose where the program jumps next.

That is the core idea of this challenge:

```text
overflow buffer -> overwrite return address -> jump to hidden win function
```

## 4. The Hidden Function

The binary contains a hidden function named `win_func` which prints the flag.
We want to make the program jump to this function, so we need its address.

You can see function names and addresses with `objdump -d` - we can for instance find the function `fire_employee`:

```bash
objdump -d ./hrbot | grep fire_employee
```

You should see something like:

```text
0000000000401305 <fire_employee>:
```

The number on the left is the address of the function:

```text
fire_employee_addr = 0x401305
```

Now go find the address for `win_func`!

## 5. Find the Padding Length

To overwrite the return address, we need to know how far away in memory it is
from the buffer.

We know we need at least 64 input bytes to fill the buffer. But what comes
after that? How many extra bytes do we need before we reach the return address?

It is very common to use a **debugger** for this. A debugger lets you run a program, pause it, inspect registers, and see what happened when it crashed.

For this challenge, we did the debugging for you and found that the return address comes 24 bytes after the buffer ends.

The final payload should look like:

```text
padding_to_fill_buffer + padding_between_buffer_and_return + address_of_win_func
```

In Python, that means:

```python
payload = b"A" * 64 + b"B" * 24 + p64(<win_func_addr>)
```

Why `p64()`? This is a 64-bit program, so addresses are 8 bytes long. `p64()` automatically
packs the number in the byte order the CPU expects.

## 7. Complete solve.py

The provided `solve.py` uses **pwntools**.

Pwntools is a Python library made for CTF pwn challenges. It helps you:

- start a local process;
- connect to a remote challenge server;
- wait for program output;
- send input at the right time;
- pack addresses with helpers like `p64()`.

Install it with:

```bash
python3 -m pip install --user pwntools
```

If your system blocks global Python package installs, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
python3 -m pip install pwntools
```

You can quickly check that it works:

```bash
python3 -c "from pwn import *; print(p64(0x401256))"
```

Open `solve.py`. You should see three values marked with `TODO`:

```python
BUFFER_SIZE = 0
OFFSET = 0
WIN_FUNC = 0x0
```

You should now be able to fill these in!

Then run the exploit locally:

```bash
python3 solve.py LOCAL
```

If everything works, you should see the redacted local flag:

```text
FLAG: brunner{REDACTED}
```

## 8. Run It Remotely

Start your challenge instance and update the host/port in `solve.py` if needed:

```python
host = "<your-instance>.challs.brunnerne.xyz"
remote(host, 1337, ssl=True)
```

Then run:

```bash
python3 solve.py REMOTE
```

The remote server has the real `flag.txt`.

## Resources

Here are some more guides on ret2win and pwn!

- [ir0nstone](https://ir0nstone.gitbook.io/notes/binexp/stack/ret2win)
- [Hacktricks](https://hacktricks.wiki/en/binary-exploitation/stack-overflow/ret2win/index.html)

Tools:

- [pwndbg](https://github.com/pwndbg/pwndbg)
- [pwntools](https://docs.pwntools.com/en/stable/intro.html)
- [Ghidra](https://github.com/nationalsecurityagency/ghidra)
