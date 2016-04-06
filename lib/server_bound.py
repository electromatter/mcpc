import mcp_base as _mcp

class use_item(_mcp.Base):
	def __init__(_self, hand):
		_self.hand = hand
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(29)
		_raw += _mcp.encode_varint(_self.hand)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 29:
			raise _mcp.NoMatchError()
		hand, _off = _mcp.decode_varint(_raw, _off)
		return use_item(hand)

class place_block(_mcp.Base):
	def __init__(_self, pos, face, hand, x, y, z):
		_self.pos = pos
		_self.face = face
		_self.hand = hand
		_self.x = x
		_self.y = y
		_self.z = z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(28)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_varint(_self.face)
		_raw += _mcp.encode_varint(_self.hand)
		_raw += _mcp.encode_byte(_self.x)
		_raw += _mcp.encode_byte(_self.y)
		_raw += _mcp.encode_byte(_self.z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 28:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		face, _off = _mcp.decode_varint(_raw, _off)
		hand, _off = _mcp.decode_varint(_raw, _off)
		x, _off = _mcp.decode_byte(_raw, _off)
		y, _off = _mcp.decode_byte(_raw, _off)
		z, _off = _mcp.decode_byte(_raw, _off)
		return place_block(pos, face, hand, x, y, z)

class spectate(_mcp.Base):
	def __init__(_self, target):
		_self.target = target
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(27)
		_raw += _mcp.encode_uuid(_self.target)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 27:
			raise _mcp.NoMatchError()
		target, _off = _mcp.decode_uuid(_raw, _off)
		return spectate(target)

class animation(_mcp.Base):
	def __init__(_self, hand):
		_self.hand = hand
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(26)
		_raw += _mcp.encode_varint(_self.hand)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 26:
			raise _mcp.NoMatchError()
		hand, _off = _mcp.decode_varint(_raw, _off)
		return animation(hand)

class update_sign(_mcp.Base):
	def __init__(_self, pos, lines):
		_self.pos = pos
		_self.lines = lines
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(25)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_array(_self.lines, 4, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 25:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		lines, _off = _mcp.decode_array(_raw, _off, 4, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return update_sign(pos, lines)

class creative_inventory(_mcp.Base):
	def __init__(_self, slot, item):
		_self.slot = slot
		_self.item = item
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(24)
		_raw += _mcp.encode_short(_self.slot)
		_raw += _mcp.encode_slot(_self.item)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 24:
			raise _mcp.NoMatchError()
		slot, _off = _mcp.decode_short(_raw, _off)
		item, _off = _mcp.decode_slot(_raw, _off)
		return creative_inventory(slot, item)

class held_item(_mcp.Base):
	def __init__(_self, slot):
		_self.slot = slot
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(23)
		_raw += _mcp.encode_short(_self.slot)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 23:
			raise _mcp.NoMatchError()
		slot, _off = _mcp.decode_short(_raw, _off)
		return held_item(slot)

class pack_status(_mcp.Base):
	def __init__(_self, hash, result):
		_self.hash = hash
		_self.result = result
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(22)
		_raw += _mcp.encode_string(_self.hash, _mcp.encode_varint)
		_raw += _mcp.encode_varint(_self.result)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 22:
			raise _mcp.NoMatchError()
		hash, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		result, _off = _mcp.decode_varint(_raw, _off)
		return pack_status(hash, result)

class steer(_mcp.Base):
	def __init__(_self, sideways, forward, flags):
		_self.sideways = sideways
		_self.forward = forward
		_self.flags = flags
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(21)
		_raw += _mcp.encode_float(_self.sideways)
		_raw += _mcp.encode_float(_self.forward)
		_raw += _mcp.encode_byte(_self.flags)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 21:
			raise _mcp.NoMatchError()
		sideways, _off = _mcp.decode_float(_raw, _off)
		forward, _off = _mcp.decode_float(_raw, _off)
		flags, _off = _mcp.decode_byte(_raw, _off)
		return steer(sideways, forward, flags)

class entity_action(_mcp.Base):
	def __init__(_self, target, action, boost):
		_self.target = target
		_self.action = action
		_self.boost = boost
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(20)
		_raw += _mcp.encode_varint(_self.target)
		_raw += _mcp.encode_varint(_self.action)
		_raw += _mcp.encode_varint(_self.boost)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 20:
			raise _mcp.NoMatchError()
		target, _off = _mcp.decode_varint(_raw, _off)
		action, _off = _mcp.decode_varint(_raw, _off)
		boost, _off = _mcp.decode_varint(_raw, _off)
		return entity_action(target, action, boost)

class digging(_mcp.Base):
	def __init__(_self, status, pos, face):
		_self.status = status
		_self.pos = pos
		_self.face = face
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(19)
		_raw += _mcp.encode_varint(_self.status)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_byte(_self.face)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 19:
			raise _mcp.NoMatchError()
		status, _off = _mcp.decode_varint(_raw, _off)
		pos, _off = _mcp.decode_position(_raw, _off)
		face, _off = _mcp.decode_byte(_raw, _off)
		return digging(status, pos, face)

class player_abilities(_mcp.Base):
	def __init__(_self, flags, fly_speed, walk_speed):
		_self.flags = flags
		_self.fly_speed = fly_speed
		_self.walk_speed = walk_speed
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(18)
		_raw += _mcp.encode_byte(_self.flags)
		_raw += _mcp.encode_float(_self.fly_speed)
		_raw += _mcp.encode_float(_self.walk_speed)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 18:
			raise _mcp.NoMatchError()
		flags, _off = _mcp.decode_byte(_raw, _off)
		fly_speed, _off = _mcp.decode_float(_raw, _off)
		walk_speed, _off = _mcp.decode_float(_raw, _off)
		return player_abilities(flags, fly_speed, walk_speed)

class steer_boat(_mcp.Base):
	def __init__(_self, f1, f2):
		_self.f1 = f1
		_self.f2 = f2
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(17)
		_raw += _mcp.encode_bool(_self.f1)
		_raw += _mcp.encode_bool(_self.f2)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 17:
			raise _mcp.NoMatchError()
		f1, _off = _mcp.decode_bool(_raw, _off)
		f2, _off = _mcp.decode_bool(_raw, _off)
		return steer_boat(f1, f2)

class vehicle_move(_mcp.Base):
	def __init__(_self, x, y, z, yaw, pitch):
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(16)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_float(_self.yaw)
		_raw += _mcp.encode_float(_self.pitch)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 16:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_float(_raw, _off)
		return vehicle_move(x, y, z, yaw, pitch)

class player(_mcp.Base):
	def __init__(_self, on_ground):
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(15)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 15:
			raise _mcp.NoMatchError()
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return player(on_ground)

class player_look(_mcp.Base):
	def __init__(_self, yaw, pitch, on_ground):
		_self.yaw = yaw
		_self.pitch = pitch
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(14)
		_raw += _mcp.encode_float(_self.yaw)
		_raw += _mcp.encode_float(_self.pitch)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 14:
			raise _mcp.NoMatchError()
		yaw, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_float(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return player_look(yaw, pitch, on_ground)

class player_position_and_look(_mcp.Base):
	def __init__(_self, x, y, z, yaw, pitch, on_ground):
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(13)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_float(_self.yaw)
		_raw += _mcp.encode_float(_self.pitch)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 13:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_float(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return player_position_and_look(x, y, z, yaw, pitch, on_ground)

class player_position(_mcp.Base):
	def __init__(_self, x, y, z, on_ground):
		_self.x = x
		_self.y = y
		_self.z = z
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 12:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return player_position(x, y, z, on_ground)

class keepalive(_mcp.Base):
	def __init__(_self, timestamp):
		_self.timestamp = timestamp
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(11)
		_raw += _mcp.encode_varint(_self.timestamp)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 11:
			raise _mcp.NoMatchError()
		timestamp, _off = _mcp.decode_varint(_raw, _off)
		return keepalive(timestamp)

class interact_at_entity(_mcp.Base):
	def __init__(_self, target, x, y, z, hand):
		_self.target = target
		_self.x = x
		_self.y = y
		_self.z = z
		_self.hand = hand
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(10)
		_raw += _mcp.encode_varint(_self.target)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_float(_self.x)
		_raw += _mcp.encode_float(_self.y)
		_raw += _mcp.encode_float(_self.z)
		_raw += _mcp.encode_varint(_self.hand)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 10:
			raise _mcp.NoMatchError()
		target, _off = _mcp.decode_varint(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 2:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_float(_raw, _off)
		y, _off = _mcp.decode_float(_raw, _off)
		z, _off = _mcp.decode_float(_raw, _off)
		hand, _off = _mcp.decode_varint(_raw, _off)
		return interact_at_entity(target, x, y, z, hand)

class attack_entity(_mcp.Base):
	def __init__(_self, target):
		_self.target = target
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(10)
		_raw += _mcp.encode_varint(_self.target)
		_raw += _mcp.encode_varint(1)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 10:
			raise _mcp.NoMatchError()
		target, _off = _mcp.decode_varint(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 1:
			raise _mcp.NoMatchError()
		return attack_entity(target)

class interact_entity(_mcp.Base):
	def __init__(_self, target, hand):
		_self.target = target
		_self.hand = hand
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(10)
		_raw += _mcp.encode_varint(_self.target)
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_varint(_self.hand)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 10:
			raise _mcp.NoMatchError()
		target, _off = _mcp.decode_varint(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 0:
			raise _mcp.NoMatchError()
		hand, _off = _mcp.decode_varint(_raw, _off)
		return interact_entity(target, hand)

class plugin_message(_mcp.Base):
	def __init__(_self, channel, data):
		_self.channel = channel
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(9)
		_raw += _mcp.encode_string(_self.channel, _mcp.encode_varint)
		_raw += _mcp.encode_bytes_eof(_self.data)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 9:
			raise _mcp.NoMatchError()
		channel, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		data, _off = _mcp.decode_bytes_eof(_raw, _off)
		return plugin_message(channel, data)

class close_window(_mcp.Base):
	def __init__(_self, window):
		_self.window = window
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(8)
		_raw += _mcp.encode_byte(_self.window)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 8:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		return close_window(window)

class click_window(_mcp.Base):
	def __init__(_self, window, slot, button, action, mode, clicked_item):
		_self.window = window
		_self.slot = slot
		_self.button = button
		_self.action = action
		_self.mode = mode
		_self.clicked_item = clicked_item
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(7)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_short(_self.slot)
		_raw += _mcp.encode_byte(_self.button)
		_raw += _mcp.encode_short(_self.action)
		_raw += _mcp.encode_varint(_self.mode)
		_raw += _mcp.encode_slot(_self.clicked_item)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 7:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		slot, _off = _mcp.decode_short(_raw, _off)
		button, _off = _mcp.decode_byte(_raw, _off)
		action, _off = _mcp.decode_short(_raw, _off)
		mode, _off = _mcp.decode_varint(_raw, _off)
		clicked_item, _off = _mcp.decode_slot(_raw, _off)
		return click_window(window, slot, button, action, mode, clicked_item)

class enchant(_mcp.Base):
	def __init__(_self, window, enchantment):
		_self.window = window
		_self.enchantment = enchantment
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(6)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_byte(_self.enchantment)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 6:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		enchantment, _off = _mcp.decode_byte(_raw, _off)
		return enchant(window, enchantment)

class confirm_transaction(_mcp.Base):
	def __init__(_self, window, action, accepted):
		_self.window = window
		_self.action = action
		_self.accepted = accepted
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(5)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_short(_self.action)
		_raw += _mcp.encode_bool(_self.accepted)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 5:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		action, _off = _mcp.decode_short(_raw, _off)
		accepted, _off = _mcp.decode_bool(_raw, _off)
		return confirm_transaction(window, action, accepted)

class settings(_mcp.Base):
	def __init__(_self, locale, view, chat_mode, chat_colors, skin_parts, main_hand):
		_self.locale = locale
		_self.view = view
		_self.chat_mode = chat_mode
		_self.chat_colors = chat_colors
		_self.skin_parts = skin_parts
		_self.main_hand = main_hand
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(4)
		_raw += _mcp.encode_string(_self.locale, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.view)
		_raw += _mcp.encode_varint(_self.chat_mode)
		_raw += _mcp.encode_bool(_self.chat_colors)
		_raw += _mcp.encode_byte(_self.skin_parts)
		_raw += _mcp.encode_varint(_self.main_hand)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 4:
			raise _mcp.NoMatchError()
		locale, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		view, _off = _mcp.decode_byte(_raw, _off)
		chat_mode, _off = _mcp.decode_varint(_raw, _off)
		chat_colors, _off = _mcp.decode_bool(_raw, _off)
		skin_parts, _off = _mcp.decode_byte(_raw, _off)
		main_hand, _off = _mcp.decode_varint(_raw, _off)
		return settings(locale, view, chat_mode, chat_colors, skin_parts, main_hand)

class client_status(_mcp.Base):
	def __init__(_self, action):
		_self.action = action
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(3)
		_raw += _mcp.encode_varint(_self.action)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 3:
			raise _mcp.NoMatchError()
		action, _off = _mcp.decode_varint(_raw, _off)
		return client_status(action)

class message(_mcp.Base):
	def __init__(_self, text):
		_self.text = text
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_string(_self.text, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 2:
			raise _mcp.NoMatchError()
		text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return message(text)

class look_tab_complete(_mcp.Base):
	def __init__(_self, text, is_command, look):
		_self.text = text
		_self.is_command = is_command
		_self.look = look
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_string(_self.text, _mcp.encode_varint)
		_raw += _mcp.encode_bool(_self.is_command)
		_raw += _mcp.encode_bool(1)
		_raw += _mcp.encode_position(_self.look)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 1:
			raise _mcp.NoMatchError()
		text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		is_command, _off = _mcp.decode_bool(_raw, _off)
		_match5, _off = _mcp.decode_bool(_raw, _off)
		if _match5 != 1:
			raise _mcp.NoMatchError()
		look, _off = _mcp.decode_position(_raw, _off)
		return look_tab_complete(text, is_command, look)

class tab_complete(_mcp.Base):
	def __init__(_self, text, is_command):
		_self.text = text
		_self.is_command = is_command
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_string(_self.text, _mcp.encode_varint)
		_raw += _mcp.encode_bool(_self.is_command)
		_raw += _mcp.encode_bool(0)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 1:
			raise _mcp.NoMatchError()
		text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		is_command, _off = _mcp.decode_bool(_raw, _off)
		_match5, _off = _mcp.decode_bool(_raw, _off)
		if _match5 != 0:
			raise _mcp.NoMatchError()
		return tab_complete(text, is_command)

class teleport_confirm(_mcp.Base):
	def __init__(_self, teleportid):
		_self.teleportid = teleportid
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_varint(_self.teleportid)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if _match4 != 0:
			raise _mcp.NoMatchError()
		teleportid, _off = _mcp.decode_varint(_raw, _off)
		return teleport_confirm(teleportid)

class play107(_mcp.Base):
	@staticmethod
	def decode(_raw, _off=0):
		_match4, _off = _mcp.decode_varint(_raw, _off)
		if false:
			pass
		elif _match4 == 0:
			teleportid, _off = _mcp.decode_varint(_raw, _off)
			return teleport_confirm(teleportid)
		elif _match4 == 1:
			text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			is_command, _off = _mcp.decode_bool(_raw, _off)
			_match5, _off = _mcp.decode_bool(_raw, _off)
			if false:
				pass
			elif _match5 == 0:
				return tab_complete()
			elif _match5 == 1:
				look, _off = _mcp.decode_position(_raw, _off)
				return look_tab_complete(look)
			else:
				raise _mcp.NoMatchError()
		elif _match4 == 2:
			text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return message(text)
		elif _match4 == 3:
			action, _off = _mcp.decode_varint(_raw, _off)
			return client_status(action)
		elif _match4 == 4:
			locale, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			view, _off = _mcp.decode_byte(_raw, _off)
			chat_mode, _off = _mcp.decode_varint(_raw, _off)
			chat_colors, _off = _mcp.decode_bool(_raw, _off)
			skin_parts, _off = _mcp.decode_byte(_raw, _off)
			main_hand, _off = _mcp.decode_varint(_raw, _off)
			return settings(locale, view, chat_mode, chat_colors, skin_parts, main_hand)
		elif _match4 == 5:
			window, _off = _mcp.decode_byte(_raw, _off)
			action, _off = _mcp.decode_short(_raw, _off)
			accepted, _off = _mcp.decode_bool(_raw, _off)
			return confirm_transaction(window, action, accepted)
		elif _match4 == 6:
			window, _off = _mcp.decode_byte(_raw, _off)
			enchantment, _off = _mcp.decode_byte(_raw, _off)
			return enchant(window, enchantment)
		elif _match4 == 7:
			window, _off = _mcp.decode_byte(_raw, _off)
			slot, _off = _mcp.decode_short(_raw, _off)
			button, _off = _mcp.decode_byte(_raw, _off)
			action, _off = _mcp.decode_short(_raw, _off)
			mode, _off = _mcp.decode_varint(_raw, _off)
			clicked_item, _off = _mcp.decode_slot(_raw, _off)
			return click_window(window, slot, button, action, mode, clicked_item)
		elif _match4 == 8:
			window, _off = _mcp.decode_byte(_raw, _off)
			return close_window(window)
		elif _match4 == 9:
			channel, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			data, _off = _mcp.decode_bytes_eof(_raw, _off)
			return plugin_message(channel, data)
		elif _match4 == 10:
			target, _off = _mcp.decode_varint(_raw, _off)
			_match6, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match6 == 0:
				hand, _off = _mcp.decode_varint(_raw, _off)
				return interact_entity(hand)
			elif _match6 == 1:
				return attack_entity()
			elif _match6 == 2:
				x, _off = _mcp.decode_float(_raw, _off)
				y, _off = _mcp.decode_float(_raw, _off)
				z, _off = _mcp.decode_float(_raw, _off)
				hand, _off = _mcp.decode_varint(_raw, _off)
				return interact_at_entity(x, y, z, hand)
			else:
				raise _mcp.NoMatchError()
		elif _match4 == 11:
			timestamp, _off = _mcp.decode_varint(_raw, _off)
			return keepalive(timestamp)
		elif _match4 == 12:
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return player_position(x, y, z, on_ground)
		elif _match4 == 13:
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_float(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return player_position_and_look(x, y, z, yaw, pitch, on_ground)
		elif _match4 == 14:
			yaw, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_float(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return player_look(yaw, pitch, on_ground)
		elif _match4 == 15:
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return player(on_ground)
		elif _match4 == 16:
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_float(_raw, _off)
			return vehicle_move(x, y, z, yaw, pitch)
		elif _match4 == 17:
			f1, _off = _mcp.decode_bool(_raw, _off)
			f2, _off = _mcp.decode_bool(_raw, _off)
			return steer_boat(f1, f2)
		elif _match4 == 18:
			flags, _off = _mcp.decode_byte(_raw, _off)
			fly_speed, _off = _mcp.decode_float(_raw, _off)
			walk_speed, _off = _mcp.decode_float(_raw, _off)
			return player_abilities(flags, fly_speed, walk_speed)
		elif _match4 == 19:
			status, _off = _mcp.decode_varint(_raw, _off)
			pos, _off = _mcp.decode_position(_raw, _off)
			face, _off = _mcp.decode_byte(_raw, _off)
			return digging(status, pos, face)
		elif _match4 == 20:
			target, _off = _mcp.decode_varint(_raw, _off)
			action, _off = _mcp.decode_varint(_raw, _off)
			boost, _off = _mcp.decode_varint(_raw, _off)
			return entity_action(target, action, boost)
		elif _match4 == 21:
			sideways, _off = _mcp.decode_float(_raw, _off)
			forward, _off = _mcp.decode_float(_raw, _off)
			flags, _off = _mcp.decode_byte(_raw, _off)
			return steer(sideways, forward, flags)
		elif _match4 == 22:
			hash, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			result, _off = _mcp.decode_varint(_raw, _off)
			return pack_status(hash, result)
		elif _match4 == 23:
			slot, _off = _mcp.decode_short(_raw, _off)
			return held_item(slot)
		elif _match4 == 24:
			slot, _off = _mcp.decode_short(_raw, _off)
			item, _off = _mcp.decode_slot(_raw, _off)
			return creative_inventory(slot, item)
		elif _match4 == 25:
			pos, _off = _mcp.decode_position(_raw, _off)
			lines, _off = _mcp.decode_array(_raw, _off, 4, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
			return update_sign(pos, lines)
		elif _match4 == 26:
			hand, _off = _mcp.decode_varint(_raw, _off)
			return animation(hand)
		elif _match4 == 27:
			target, _off = _mcp.decode_uuid(_raw, _off)
			return spectate(target)
		elif _match4 == 28:
			pos, _off = _mcp.decode_position(_raw, _off)
			face, _off = _mcp.decode_varint(_raw, _off)
			hand, _off = _mcp.decode_varint(_raw, _off)
			x, _off = _mcp.decode_byte(_raw, _off)
			y, _off = _mcp.decode_byte(_raw, _off)
			z, _off = _mcp.decode_byte(_raw, _off)
			return place_block(pos, face, hand, x, y, z)
		elif _match4 == 29:
			hand, _off = _mcp.decode_varint(_raw, _off)
			return use_item(hand)
		else:
			raise _mcp.NoMatchError()

