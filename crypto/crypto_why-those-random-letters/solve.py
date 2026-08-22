enc = 'cqsWvloGoWfGsv|LXS4e`YEI4E5EmJuL`ExB2Fuuii`qSV5LoLeUpbnH"W~n'
for i in range(0, len(enc), 2):
    print(chr(ord(enc[i])-1),end='')
print()
