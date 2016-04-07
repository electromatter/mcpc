# mcp_base.py
#
# Copyright (c) 2016 Eric Chai <electromatter@gmail.com>
# All rights reserved.
#
# This software may be modified and distributed under the terms
# of the ISC license. See the LICENSE file for details.

import struct
import uuid
import nbt
import io

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
	def encode(self):
		if self.itemid < 0:
			return encode_short(-1)
		raw = encode_byte(self.itemid)
		raw += encode_short(self.count)
		raw += encode_short(self.damage)
		return raw + encode_nbt(self.nbt)
	@staticmethod
	def decode(raw, off):
		itemid, off = decode_short(raw, off)
		if itemid < 0:
			return None, off
		count, off = decode_byte(raw, off)
		damage, off = decode_short(raw, off)
		nbt, off = decode_nbt(raw, off)
		return Slot(itemid, count, damage, nbt), off

#Types:
#int - bool byte short int long varint varlong
#simple - float double uuid angle position slot nbt bytes_eof
#string - string string_utf16 bytes
#array - array

def fix_sign(x, bits):
	if x >= (1 << bits):
		raise ValueError('too large: %r' % x)
	if x < 0:
		raise ValueError('negitive: %r' % x)
	if x & (1 << (bits - 1)):
		x -= 1 << bits
	return x

# the interface here is: decode_*type*(raw, off, *args*) -> (val, new_off)
def decode_raw(raw, off, n):
	if n < 0:
		raise ValueError('negitive size: %r' % n)
	if len(raw) < off + n:
		raise NotEnoughData()
	return raw[off:off+n], off+n

def decode_bool(raw, off=0):
	raw, off = decode_raw(raw, off, 1)
	ret = not not raw[0]
	return ret, off

def decode_byte(raw, off=0):
	raw, off = decode_raw(raw, off, 1)
	return struct.unpack('!b', raw)[0], off

def decode_short(raw, off=0):
	raw, off = decode_raw(raw, off, 2)
	return struct.unpack("!h", raw)[0], off

def decode_int(raw, off=0):
	raw, off = decode_raw(raw, off, 4)
	return struct.unpack("!i", raw)[0], off

def decode_long(raw, off=0):
	raw, off = decode_raw(raw, off, 8)
	return struct.unpack("!q", raw)[0], off

def decode_uvarlong(raw, _off=0):
	raw = raw[_off:]
	val = 0
	for off in range(11):
		if off >= len(raw):
			raise NotEnoughData()
		val |= (raw[off] & 0x7f) << (off * 7)
		if (raw[off] & 0x80) == 0:
			return val, off + _off + 1
	raise NoMatchError('varint too long')

def decode_varint(raw, off=0):
	raw, off = decode_uvarlong(raw, off)
	return fix_sign(raw, 32), off

def decode_varlong(raw, off=0):
	raw, off = decode_uvarlong(raw, off)
	return fix_sign(raw, 64), off

def decode_float(raw, off=0):
	raw, off = decode_raw(raw, off, 4)
	return struct.unpack("!f", raw)[0], off

def decode_double(raw, off=0):
	raw, off = decode_raw(raw, off, 8)
	return struct.unpack("!d", raw)[0], off

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
	raw = memoryview(raw)[off:]
	if raw[0] == 0:
		return None, off + 1
	f = io.BytesIO(raw)
	return nbt.nbt.TAG_Compound(buffer=f), off + f.tell()

def decode_slot(raw, off=0):
	return Slot.decode(raw, off)

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

#returns true if the signed value fits in bits
def sign_range_bits(val, bits):
	maxval = (1 << (bits - 1)) - 1
	minval = -(1 << (bits - 1))
	return minval < val and val < maxval

#TODO: softer value checking
# the interface is: encode_type(val, *args*) -> bytes
def encode_byte(val):
	return struct.pack('!b', val)

def encode_bool(val):
	return encode_byte(1 if val else 0)

def encode_short(val):
	return struct.pack('!h', val)

def encode_int(val):
	return struct.pack('!i', val)

def encode_long(val):
	return struct.pack('!q', val)

def encode_uvarlong(val):
	raw = bytearray(11)
	assert val >= 0
	for off in range(len(raw)):
		if val >= 0x7f:
			raw[off] = 0x80 | (val & 0x7f)
		else:
			raw[off] = val
		val >>= 7
		if val == 0:
			return bytes(raw[:off + 1])
	raise ValueError('val too big: %r' % val)

def encode_varint(val):
	if not sign_range_bits(val, 32):
		raise ValueError('val does not fit in a varint %r' % val)
	return encode_uvarlong(val & 0xffffffff)

def encode_varlong(val):
	if not sign_range_bits(val, 64):
		raise ValueError('val does not fit in a varint %r' % val)
	return encode_uvarlong(val & 0xffffffffffffffff)

def encode_float(val):
	return struct.pack('!f', val)

def encode_double(val):
	return struct.pack('!d', val)

def encode_uuid(val):
	if isinstance(val, str):
		val = uuid.UUID(val)
	elif isinstance(val, uuid.UUID):
		pass
	else:
		raise ValueError('val must a uuid')
	return val.bytes

def encode_angle(val):
	return encode_byte(val)

def encode_position(val):
	x, y, z = val
	if not (sign_range_bits(x, 26) and sign_range_bits(y, 12) and sign_range_bits(z, 26)):
		raise ValueError('x, y, z must be 26 bits, 12 bits, 26 bits respectively')
	return encode_long(((x & 0x3ffffff) << 38) | ((y & 0xfff) << 26) | (z & 0x3ffffff))

def encode_nbt(val):
	if val is None:
		b'\x00'
	f = io.BytesIO()
	val.write_file(buffer=f)
	return f.getvalue()

def encode_slot(val):
	if val is None:
		return encode_short(-1)
	return val.encode()

def encode_bytes_eof(val):
	return bytes(val)

def encode_bytes(val, size=encode_varint):
	val = bytes(val)
	return size(len(val)) + val

def encode_string(val, size=encode_varint):
	return encode_bytes(val.encode('utf-8'), size)

def encode_string_utf16(val, size=encode_varint):
	raise NotImplementedError()

def encode_array(val, size=encode_varint, elem=None):
	raw = size(len(val))
	for x in val:
		raw += elem(x)
	return raw

