S = 22263691028918788395010325066307464924652601045336492930678310479674861811846
M = 9**5 + 2

q0 = (2 * S) // (M - 2)
for q in range(q0 - 10, q0 + 10):
    for bit in [0, 1]:
        n = 2 * (S + q) + bit
        if n//2 - n//M == S:
            b = n.to_bytes((n.bit_length() + 7) // 8, "big")
            print(b)