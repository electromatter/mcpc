import struct

class NoMatchError(Exception):
	pass

class NotEnoughData(Exception):
	pass

class Base:
	@classmethod
	def decode(cls, ptr):
		raise NotImplementedError('tried to decode base type')

	def __init__(self):
		raise NotImplementedError('tried to create non-terminal type')

	def encode(self):
		raise NotImplementedError('tried to encode non-terminal type')

class Slot:
	def __init__(self, itemid, count=1, damage=0, nbt=None):
		self.itemid = itemid
		self.count = count
		self.damage = damage
		self.nbt = nbt

#Types:
#int - bool byte short int long varint varlong
#simple - float double uuid angle position slot nbt bytes_eof
#string - string string_utf16 bytes
#array - array

def fix_sign(x, bits):
	if x >= (1 << bits):
		raise ValueError('Too large')
	if x < 0:
		raise ValueError('negitive?')
	if x & (1 << (bits - 1)):
		x -= 1 << bits
	return x

def decode_raw(raw, off, n):
	if n < 0:
		raise ValueError('n negitive?')
	if len(raw) < off + n:
		raise NotEnoughData()
	return raw[off:off+n], off+n

def decode_bool(raw, off=0):
	raw, off = decode_raw(raw, off, 1)
	ret = not not raw[0]
	return ret, off

def decode_byte(raw, off=0):
	raw, off = decode_raw(raw, off, 1)
	return raw[0], off

def decode_short(raw, off=0):
	raw, off = decode_raw(raw, off, 2)
	return struct.unpack("!h", raw), off

def decode_int(raw, off=0):
	raw, off = decode_raw(raw, off, 4)
	return struct.unpack("!i", raw), off

def decode_long(raw, off=0):
	raw, off = decode_raw(raw, off, 8)
	return struct.unpack("!l", raw), off

def decode_uvarlong(raw, _off=0):
	raw = raw[_off:]
	val = 0
	for off in range(11):
		if off >= len(raw):
			raise NotEnoughData()
		val |= (raw[off] & 0x7f) << (off * 7)
		if (raw[off] & 0x80) == 0:
			return val, off + _off
	raise NoMatchError('varint too long')

def decode_varint(raw, off=0):
	raw, off = decode_uvarlong(raw, off)
	return fix_sign(raw, 32), off

def decode_varlong(raw, off=0):
	raw, off = decode_uvarlong(raw, off)
	return fix_sign(raw, 64), off

def decode_float(raw, off=0):
	raw, off = decode_raw(raw, off, 4)
	return struct.unpack("!f", raw), off

def decode_double(raw, off=0):
	raw, off = decode_raw(raw, off, 8)
	return struct.unpack("!d", raw), off

def decode_uuid(raw, off=0):
	raw, off = decode_raw(raw, off, 16)
	return uuid.UUID(bytes=raw), off

def decode_angle(raw, off=0):
	return decode_byte(raw, off)

def decode_position(raw, off=0):
	raw, off = decode_long(raw, off)
	raw &= 0xffffffffffffffff
	x = fix_sign(raw >> 38, 26)
	y = fix_sign((raw >> 26) & 0xfff, 12)
	z = fix_sign(raw & 0x3ffffff, 26)
	return (x, y, z), off
	
def decode_nbt(raw, off=0):
	raise NotImplementedError()

def decode_slot(raw, off=0):
	itemid, off = decode_short(raw, off)
	if itemid < 0:
		return None, off
	count, off = decode_short(raw, off)
	damage, off = decode_short(raw, off)
	nbt, off = decode_nbt(raw, off)
	return Slot(itemid, count, damage, nbt), off

def decode_bytes_eof(raw, off=0):
	if len(raw) < off:
		raise NotEnoughData()
	return raw[off:], len(raw)

def decode_bytes(raw, off=0, size=decode_varint):
	if not isinstance(size, int):
		size, off = size(raw, off)
	return decode_raw(raw, off, size)

def decode_string(raw, off=0, size=decode_varint):
	raw, off = decode_bytes(raw, off, size)
	return raw.decode('utf-8'), off

def decode_string_utf16(raw, off=0, size=decode_varint):
	raise NotImplementedError()

def decode_array(raw, off=0, size=decode_varint, elem=None):
	val = []
	if not isinstance(size, int):
		size, off = size(raw, off)
	if elem is None:
		raise ValueError('elem must be a decode closure')
	for _ in range(size):
		x, off = elem(raw, off)
		val.append(x)
	return val, off

