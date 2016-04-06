import mcp_base as _mcp

class explosion_record(_mcp.Base):
	def __init__(_self, x, y, z):
		_self.x = x
		_self.y = y
		_self.z = z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_byte(_self.x)
		_raw += _mcp.encode_byte(_self.y)
		_raw += _mcp.encode_byte(_self.z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		x, _off = _mcp.decode_byte(_raw, _off)
		y, _off = _mcp.decode_byte(_raw, _off)
		z, _off = _mcp.decode_byte(_raw, _off)
		return explosion_record(x, y, z)

class entity_property_modifier(_mcp.Base):
	def __init__(_self, uuid, ammount, operation):
		_self.uuid = uuid
		_self.ammount = ammount
		_self.operation = operation
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_double(_self.ammount)
		_raw += _mcp.encode_byte(_self.operation)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		ammount, _off = _mcp.decode_double(_raw, _off)
		operation, _off = _mcp.decode_byte(_raw, _off)
		return entity_property_modifier(uuid, ammount, operation)

class entity_property(_mcp.Base):
	def __init__(_self, key, value, modifiers):
		_self.key = key
		_self.value = value
		_self.modifiers = modifiers
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_string(_self.key, _mcp.encode_varint)
		_raw += _mcp.encode_double(_self.value)
		_raw += _mcp.encode_array(_self.modifiers, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_double(_raw, _off)
		modifiers, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, entity_property_modifier.decode)
		return entity_property(key, value, modifiers)

class block_change_record(_mcp.Base):
	def __init__(_self, xz, y, block_data):
		_self.xz = xz
		_self.y = y
		_self.block_data = block_data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_byte(_self.xz)
		_raw += _mcp.encode_byte(_self.y)
		_raw += _mcp.encode_varint(_self.block_data)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		xz, _off = _mcp.decode_byte(_raw, _off)
		y, _off = _mcp.decode_byte(_raw, _off)
		block_data, _off = _mcp.decode_varint(_raw, _off)
		return block_change_record(xz, y, block_data)

class statistic(_mcp.Base):
	def __init__(_self, name, value):
		_self.name = name
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_varint(_self.value)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_varint(_raw, _off)
		return statistic(name, value)

class signed_player_property(_mcp.Base):
	def __init__(_self, key, value, signature):
		_self.key = key
		_self.value = value
		_self.signature = signature
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_string(_self.key, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.value, _mcp.encode_varint)
		_raw += _mcp.encode_bool(1)
		_raw += _mcp.encode_string(_self.signature, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match3, _off = _mcp.decode_bool(_raw, _off)
		if _match3 != 1:
			raise _mcp.NoMatchError()
		signature, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return signed_player_property(key, value, signature)

class unsigned_player_property(_mcp.Base):
	def __init__(_self, key, value):
		_self.key = key
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_string(_self.key, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.value, _mcp.encode_varint)
		_raw += _mcp.encode_bool(0)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match3, _off = _mcp.decode_bool(_raw, _off)
		if _match3 != 0:
			raise _mcp.NoMatchError()
		return unsigned_player_property(key, value)

class player_property(_mcp.Base):
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match3, _off = _mcp.decode_bool(_raw, _off)
		if false:
			pass
		elif _match3 == 0:
			return unsigned_player_property()
		elif _match3 == 1:
			signature, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return signed_player_property(signature)
		else:
			raise _mcp.NoMatchError()

class displayname(_mcp.Base):
	def __init__(_self, key, display):
		_self.key = key
		_self.display = display
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_uuid(_self.key)
		_raw += _mcp.encode_bool(1)
		_raw += _mcp.encode_string(_self.display, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_uuid(_raw, _off)
		_match4, _off = _mcp.decode_bool(_raw, _off)
		if _match4 != 1:
			raise _mcp.NoMatchError()
		display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return displayname(key, display)

class no_displayname(_mcp.Base):
	def __init__(_self, key):
		_self.key = key
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_uuid(_self.key)
		_raw += _mcp.encode_bool(0)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_uuid(_raw, _off)
		_match4, _off = _mcp.decode_bool(_raw, _off)
		if _match4 != 0:
			raise _mcp.NoMatchError()
		return no_displayname(key)

class player_displayname(_mcp.Base):
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_uuid(_raw, _off)
		_match4, _off = _mcp.decode_bool(_raw, _off)
		if false:
			pass
		elif _match4 == 0:
			return no_displayname()
		elif _match4 == 1:
			display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return displayname(display)
		else:
			raise _mcp.NoMatchError()

class player_info(_mcp.Base):
	def __init__(_self, key, name, properties, gamemode, ping, displayname):
		_self.key = key
		_self.name = name
		_self.properties = properties
		_self.gamemode = gamemode
		_self.ping = ping
		_self.displayname = displayname
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_uuid(_self.key)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_array(_self.properties, _mcp.encode_varint, (lambda _val: _val.encode()))
		_raw += _mcp.encode_varint(_self.gamemode)
		_raw += _mcp.encode_varint(_self.ping)
		_raw += _self.displayname.encode()
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_uuid(_raw, _off)
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		properties, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, player_property.decode)
		gamemode, _off = _mcp.decode_varint(_raw, _off)
		ping, _off = _mcp.decode_varint(_raw, _off)
		displayname, _off = player_displayname.decode(_raw, _off)
		return player_info(key, name, properties, gamemode, ping, displayname)

class uuid_varint(_mcp.Base):
	def __init__(_self, key, value):
		_self.key = key
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_uuid(_self.key)
		_raw += _mcp.encode_varint(_self.value)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		key, _off = _mcp.decode_uuid(_raw, _off)
		value, _off = _mcp.decode_varint(_raw, _off)
		return uuid_varint(key, value)

class map_icon(_mcp.Base):
	def __init__(_self, dirtype, x, z):
		_self.dirtype = dirtype
		_self.x = x
		_self.z = z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_byte(_self.dirtype)
		_raw += _mcp.encode_byte(_self.x)
		_raw += _mcp.encode_byte(_self.z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		dirtype, _off = _mcp.decode_byte(_raw, _off)
		x, _off = _mcp.decode_byte(_raw, _off)
		z, _off = _mcp.decode_byte(_raw, _off)
		return map_icon(dirtype, x, z)

class entity_effect(_mcp.Base):
	def __init__(_self, entity, effect, amplifier, duration, particles):
		_self.entity = entity
		_self.effect = effect
		_self.amplifier = amplifier
		_self.duration = duration
		_self.particles = particles
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(76)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_byte(_self.effect)
		_raw += _mcp.encode_byte(_self.amplifier)
		_raw += _mcp.encode_varint(_self.duration)
		_raw += _mcp.encode_byte(_self.particles)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 76:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		effect, _off = _mcp.decode_byte(_raw, _off)
		amplifier, _off = _mcp.decode_byte(_raw, _off)
		duration, _off = _mcp.decode_varint(_raw, _off)
		particles, _off = _mcp.decode_byte(_raw, _off)
		return entity_effect(entity, effect, amplifier, duration, particles)

class entity_properties(_mcp.Base):
	def __init__(_self, entity, properties):
		_self.entity = entity
		_self.properties = properties
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(75)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_array(_self.properties, _mcp.encode_int, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 75:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		properties, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, entity_property.decode)
		return entity_properties(entity, properties)

class teleport_entity(_mcp.Base):
	def __init__(_self, entity, x, y, z, yaw, pitch, on_ground):
		_self.entity = entity
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(74)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 74:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return teleport_entity(entity, x, y, z, yaw, pitch, on_ground)

class collect_item(_mcp.Base):
	def __init__(_self, collected, collector):
		_self.collected = collected
		_self.collector = collector
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(73)
		_raw += _mcp.encode_varint(_self.collected)
		_raw += _mcp.encode_varint(_self.collector)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 73:
			raise _mcp.NoMatchError()
		collected, _off = _mcp.decode_varint(_raw, _off)
		collector, _off = _mcp.decode_varint(_raw, _off)
		return collect_item(collected, collector)

class player_list_footer(_mcp.Base):
	def __init__(_self, header, footer):
		_self.header = header
		_self.footer = footer
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(72)
		_raw += _mcp.encode_string(_self.header, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.footer, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 72:
			raise _mcp.NoMatchError()
		header, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		footer, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return player_list_footer(header, footer)

class sound(_mcp.Base):
	def __init__(_self, sound, category, x, y, z, volume, pitch):
		_self.sound = sound
		_self.category = category
		_self.x = x
		_self.y = y
		_self.z = z
		_self.volume = volume
		_self.pitch = pitch
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(71)
		_raw += _mcp.encode_varint(_self.sound)
		_raw += _mcp.encode_varint(_self.category)
		_raw += _mcp.encode_int(_self.x)
		_raw += _mcp.encode_int(_self.y)
		_raw += _mcp.encode_int(_self.z)
		_raw += _mcp.encode_float(_self.volume)
		_raw += _mcp.encode_byte(_self.pitch)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 71:
			raise _mcp.NoMatchError()
		sound, _off = _mcp.decode_varint(_raw, _off)
		category, _off = _mcp.decode_varint(_raw, _off)
		x, _off = _mcp.decode_int(_raw, _off)
		y, _off = _mcp.decode_int(_raw, _off)
		z, _off = _mcp.decode_int(_raw, _off)
		volume, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_byte(_raw, _off)
		return sound(sound, category, x, y, z, volume, pitch)

class update_sign(_mcp.Base):
	def __init__(_self, pos, lines):
		_self.pos = pos
		_self.lines = lines
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(70)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_array(_self.lines, 4, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 70:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		lines, _off = _mcp.decode_array(_raw, _off, 4, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return update_sign(pos, lines)

class reset_title(_mcp.Base):
	def __init__(_self):
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(69)
		_raw += _mcp.encode_varint(4)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 69:
			raise _mcp.NoMatchError()
		_match13, _off = _mcp.decode_varint(_raw, _off)
		if _match13 != 4:
			raise _mcp.NoMatchError()
		return reset_title()

class hide_title(_mcp.Base):
	def __init__(_self):
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(69)
		_raw += _mcp.encode_varint(3)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 69:
			raise _mcp.NoMatchError()
		_match13, _off = _mcp.decode_varint(_raw, _off)
		if _match13 != 3:
			raise _mcp.NoMatchError()
		return hide_title()

class set_title_times(_mcp.Base):
	def __init__(_self, fade_in, stay, fade_out):
		_self.fade_in = fade_in
		_self.stay = stay
		_self.fade_out = fade_out
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(69)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_int(_self.fade_in)
		_raw += _mcp.encode_int(_self.stay)
		_raw += _mcp.encode_int(_self.fade_out)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 69:
			raise _mcp.NoMatchError()
		_match13, _off = _mcp.decode_varint(_raw, _off)
		if _match13 != 2:
			raise _mcp.NoMatchError()
		fade_in, _off = _mcp.decode_int(_raw, _off)
		stay, _off = _mcp.decode_int(_raw, _off)
		fade_out, _off = _mcp.decode_int(_raw, _off)
		return set_title_times(fade_in, stay, fade_out)

class set_subtitle(_mcp.Base):
	def __init__(_self, text):
		_self.text = text
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(69)
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_string(_self.text, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 69:
			raise _mcp.NoMatchError()
		_match13, _off = _mcp.decode_varint(_raw, _off)
		if _match13 != 1:
			raise _mcp.NoMatchError()
		text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return set_subtitle(text)

class set_title(_mcp.Base):
	def __init__(_self, text):
		_self.text = text
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(69)
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_string(_self.text, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 69:
			raise _mcp.NoMatchError()
		_match13, _off = _mcp.decode_varint(_raw, _off)
		if _match13 != 0:
			raise _mcp.NoMatchError()
		text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return set_title(text)

class update_time(_mcp.Base):
	def __init__(_self, age, time):
		_self.age = age
		_self.time = time
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(68)
		_raw += _mcp.encode_long(_self.age)
		_raw += _mcp.encode_long(_self.time)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 68:
			raise _mcp.NoMatchError()
		age, _off = _mcp.decode_long(_raw, _off)
		time, _off = _mcp.decode_long(_raw, _off)
		return update_time(age, time)

class compass_center(_mcp.Base):
	def __init__(_self, pos):
		_self.pos = pos
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(67)
		_raw += _mcp.encode_position(_self.pos)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 67:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		return compass_center(pos)

class remove_score(_mcp.Base):
	def __init__(_self, name, objective):
		_self.name = name
		_self.objective = objective
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(66)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_bool(1)
		_raw += _mcp.encode_string(_self.objective, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 66:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match12, _off = _mcp.decode_bool(_raw, _off)
		if _match12 != 1:
			raise _mcp.NoMatchError()
		objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return remove_score(name, objective)

class update_score(_mcp.Base):
	def __init__(_self, name, objective, value):
		_self.name = name
		_self.objective = objective
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(66)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_bool(0)
		_raw += _mcp.encode_string(_self.objective, _mcp.encode_varint)
		_raw += _mcp.encode_varint(_self.value)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 66:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match12, _off = _mcp.decode_bool(_raw, _off)
		if _match12 != 0:
			raise _mcp.NoMatchError()
		objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		value, _off = _mcp.decode_varint(_raw, _off)
		return update_score(name, objective, value)

class team_remove_players(_mcp.Base):
	def __init__(_self, name, players):
		_self.name = name
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(65)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_byte(4)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 65:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match11, _off = _mcp.decode_byte(_raw, _off)
		if _match11 != 4:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return team_remove_players(name, players)

class team_add_players(_mcp.Base):
	def __init__(_self, name, players):
		_self.name = name
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(65)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_byte(3)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 65:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match11, _off = _mcp.decode_byte(_raw, _off)
		if _match11 != 3:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return team_add_players(name, players)

class update_team_info(_mcp.Base):
	def __init__(_self, name, display, prefix, suffix, friendly_fire, name_tag, collision_rule, color):
		_self.name = name
		_self.display = display
		_self.prefix = prefix
		_self.suffix = suffix
		_self.friendly_fire = friendly_fire
		_self.name_tag = name_tag
		_self.collision_rule = collision_rule
		_self.color = color
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(65)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_byte(2)
		_raw += _mcp.encode_string(_self.display, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.prefix, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.suffix, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.friendly_fire)
		_raw += _mcp.encode_string(_self.name_tag, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.collision_rule, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.color)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 65:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match11, _off = _mcp.decode_byte(_raw, _off)
		if _match11 != 2:
			raise _mcp.NoMatchError()
		display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		prefix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		suffix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		friendly_fire, _off = _mcp.decode_byte(_raw, _off)
		name_tag, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		collision_rule, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		color, _off = _mcp.decode_byte(_raw, _off)
		return update_team_info(name, display, prefix, suffix, friendly_fire, name_tag, collision_rule, color)

class remove_team(_mcp.Base):
	def __init__(_self, name):
		_self.name = name
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(65)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_byte(1)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 65:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match11, _off = _mcp.decode_byte(_raw, _off)
		if _match11 != 1:
			raise _mcp.NoMatchError()
		return remove_team(name)

class create_team(_mcp.Base):
	def __init__(_self, name, display, prefix, suffix, friendly_fire, name_tag, collision_rule, color, players):
		_self.name = name
		_self.display = display
		_self.prefix = prefix
		_self.suffix = suffix
		_self.friendly_fire = friendly_fire
		_self.name_tag = name_tag
		_self.collision_rule = collision_rule
		_self.color = color
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(65)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_byte(0)
		_raw += _mcp.encode_string(_self.display, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.prefix, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.suffix, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.friendly_fire)
		_raw += _mcp.encode_string(_self.name_tag, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.collision_rule, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.color)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 65:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match11, _off = _mcp.decode_byte(_raw, _off)
		if _match11 != 0:
			raise _mcp.NoMatchError()
		display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		prefix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		suffix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		friendly_fire, _off = _mcp.decode_byte(_raw, _off)
		name_tag, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		collision_rule, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		color, _off = _mcp.decode_byte(_raw, _off)
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return create_team(name, display, prefix, suffix, friendly_fire, name_tag, collision_rule, color, players)

class set_passengers(_mcp.Base):
	def __init__(_self, entity, passengers):
		_self.entity = entity
		_self.passengers = passengers
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(64)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_array(_self.passengers, _mcp.encode_varint, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 64:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		passengers, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_varint)
		return set_passengers(entity, passengers)

class update_objective(_mcp.Base):
	def __init__(_self, objective, value, type):
		_self.objective = objective
		_self.value = value
		_self.type = type
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(63)
		_raw += _mcp.encode_string(_self.objective, _mcp.encode_varint)
		_raw += _mcp.encode_byte(2)
		_raw += _mcp.encode_string(_self.value, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.type, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 63:
			raise _mcp.NoMatchError()
		objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match10, _off = _mcp.decode_byte(_raw, _off)
		if _match10 != 2:
			raise _mcp.NoMatchError()
		value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return update_objective(objective, value, type)

class remove_objective(_mcp.Base):
	def __init__(_self, objective):
		_self.objective = objective
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(63)
		_raw += _mcp.encode_string(_self.objective, _mcp.encode_varint)
		_raw += _mcp.encode_byte(1)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 63:
			raise _mcp.NoMatchError()
		objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match10, _off = _mcp.decode_byte(_raw, _off)
		if _match10 != 1:
			raise _mcp.NoMatchError()
		return remove_objective(objective)

class create_objective(_mcp.Base):
	def __init__(_self, objective, value, type):
		_self.objective = objective
		_self.value = value
		_self.type = type
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(63)
		_raw += _mcp.encode_string(_self.objective, _mcp.encode_varint)
		_raw += _mcp.encode_byte(0)
		_raw += _mcp.encode_string(_self.value, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.type, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 63:
			raise _mcp.NoMatchError()
		objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		_match10, _off = _mcp.decode_byte(_raw, _off)
		if _match10 != 0:
			raise _mcp.NoMatchError()
		value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return create_objective(objective, value, type)

class update_health(_mcp.Base):
	def __init__(_self, update_health, food, sat):
		_self.update_health = update_health
		_self.food = food
		_self.sat = sat
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(62)
		_raw += _mcp.encode_float(_self.update_health)
		_raw += _mcp.encode_varint(_self.food)
		_raw += _mcp.encode_float(_self.sat)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 62:
			raise _mcp.NoMatchError()
		update_health, _off = _mcp.decode_float(_raw, _off)
		food, _off = _mcp.decode_varint(_raw, _off)
		sat, _off = _mcp.decode_float(_raw, _off)
		return update_health(update_health, food, sat)

class set_xp(_mcp.Base):
	def __init__(_self, xp_bar, level, total_xp):
		_self.xp_bar = xp_bar
		_self.level = level
		_self.total_xp = total_xp
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(61)
		_raw += _mcp.encode_float(_self.xp_bar)
		_raw += _mcp.encode_varint(_self.level)
		_raw += _mcp.encode_varint(_self.total_xp)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 61:
			raise _mcp.NoMatchError()
		xp_bar, _off = _mcp.decode_float(_raw, _off)
		level, _off = _mcp.decode_varint(_raw, _off)
		total_xp, _off = _mcp.decode_varint(_raw, _off)
		return set_xp(xp_bar, level, total_xp)

class entity_equipment(_mcp.Base):
	def __init__(_self, entity, slot, item):
		_self.entity = entity
		_self.slot = slot
		_self.item = item
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(60)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_varint(_self.slot)
		_raw += _mcp.encode_slot(_self.item)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 60:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		slot, _off = _mcp.decode_varint(_raw, _off)
		item, _off = _mcp.decode_slot(_raw, _off)
		return entity_equipment(entity, slot, item)

class entity_velocity(_mcp.Base):
	def __init__(_self, entity, vx, vy, vz):
		_self.entity = entity
		_self.vx = vx
		_self.vy = vy
		_self.vz = vz
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(59)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_short(_self.vx)
		_raw += _mcp.encode_short(_self.vy)
		_raw += _mcp.encode_short(_self.vz)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 59:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		vx, _off = _mcp.decode_short(_raw, _off)
		vy, _off = _mcp.decode_short(_raw, _off)
		vz, _off = _mcp.decode_short(_raw, _off)
		return entity_velocity(entity, vx, vy, vz)

class attach_entity(_mcp.Base):
	def __init__(_self, attached, holding):
		_self.attached = attached
		_self.holding = holding
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(58)
		_raw += _mcp.encode_int(_self.attached)
		_raw += _mcp.encode_int(_self.holding)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 58:
			raise _mcp.NoMatchError()
		attached, _off = _mcp.decode_int(_raw, _off)
		holding, _off = _mcp.decode_int(_raw, _off)
		return attach_entity(attached, holding)

class entity_metadata(_mcp.Base):
	def __init__(_self, entity, metadata):
		_self.entity = entity
		_self.metadata = metadata
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(57)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_bytes_eof(_self.metadata)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 57:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
		return entity_metadata(entity, metadata)

class display_scoreboard(_mcp.Base):
	def __init__(_self, position, score_name):
		_self.position = position
		_self.score_name = score_name
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(56)
		_raw += _mcp.encode_byte(_self.position)
		_raw += _mcp.encode_string(_self.score_name, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 56:
			raise _mcp.NoMatchError()
		position, _off = _mcp.decode_byte(_raw, _off)
		score_name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return display_scoreboard(position, score_name)

class held_item_change(_mcp.Base):
	def __init__(_self, slot):
		_self.slot = slot
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(55)
		_raw += _mcp.encode_byte(_self.slot)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 55:
			raise _mcp.NoMatchError()
		slot, _off = _mcp.decode_byte(_raw, _off)
		return held_item_change(slot)

class camera(_mcp.Base):
	def __init__(_self, entity):
		_self.entity = entity
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(54)
		_raw += _mcp.encode_varint(_self.entity)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 54:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		return camera(entity)

class world_border_warn_size(_mcp.Base):
	def __init__(_self, warn_size):
		_self.warn_size = warn_size
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(5)
		_raw += _mcp.encode_varint(_self.warn_size)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 5:
			raise _mcp.NoMatchError()
		warn_size, _off = _mcp.decode_varint(_raw, _off)
		return world_border_warn_size(warn_size)

class world_border_warn_time(_mcp.Base):
	def __init__(_self, warn_time):
		_self.warn_time = warn_time
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(4)
		_raw += _mcp.encode_varint(_self.warn_time)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 4:
			raise _mcp.NoMatchError()
		warn_time, _off = _mcp.decode_varint(_raw, _off)
		return world_border_warn_time(warn_time)

class init_world_border(_mcp.Base):
	def __init__(_self, x, z, old_d, new_d, speed, portal_boundary, warn_time, warn_blocks):
		_self.x = x
		_self.z = z
		_self.old_d = old_d
		_self.new_d = new_d
		_self.speed = speed
		_self.portal_boundary = portal_boundary
		_self.warn_time = warn_time
		_self.warn_blocks = warn_blocks
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(3)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_double(_self.old_d)
		_raw += _mcp.encode_double(_self.new_d)
		_raw += _mcp.encode_varlong(_self.speed)
		_raw += _mcp.encode_varint(_self.portal_boundary)
		_raw += _mcp.encode_varint(_self.warn_time)
		_raw += _mcp.encode_varint(_self.warn_blocks)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 3:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		old_d, _off = _mcp.decode_double(_raw, _off)
		new_d, _off = _mcp.decode_double(_raw, _off)
		speed, _off = _mcp.decode_varlong(_raw, _off)
		portal_boundary, _off = _mcp.decode_varint(_raw, _off)
		warn_time, _off = _mcp.decode_varint(_raw, _off)
		warn_blocks, _off = _mcp.decode_varint(_raw, _off)
		return init_world_border(x, z, old_d, new_d, speed, portal_boundary, warn_time, warn_blocks)

class world_border_center(_mcp.Base):
	def __init__(_self, x, z):
		_self.x = x
		_self.z = z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 2:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		return world_border_center(x, z)

class world_border_lerp(_mcp.Base):
	def __init__(_self, old_d, new_d, speed):
		_self.old_d = old_d
		_self.new_d = new_d
		_self.speed = speed
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_double(_self.old_d)
		_raw += _mcp.encode_double(_self.new_d)
		_raw += _mcp.encode_varlong(_self.speed)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 1:
			raise _mcp.NoMatchError()
		old_d, _off = _mcp.decode_double(_raw, _off)
		new_d, _off = _mcp.decode_double(_raw, _off)
		speed, _off = _mcp.decode_varlong(_raw, _off)
		return world_border_lerp(old_d, new_d, speed)

class world_border_size(_mcp.Base):
	def __init__(_self, d):
		_self.d = d
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(53)
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_double(_self.d)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 53:
			raise _mcp.NoMatchError()
		_match9, _off = _mcp.decode_varint(_raw, _off)
		if _match9 != 0:
			raise _mcp.NoMatchError()
		d, _off = _mcp.decode_double(_raw, _off)
		return world_border_size(d)

class entity_head_look(_mcp.Base):
	def __init__(_self, entity, head_yaw):
		_self.entity = entity
		_self.head_yaw = head_yaw
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(52)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_angle(_self.head_yaw)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 52:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		head_yaw, _off = _mcp.decode_angle(_raw, _off)
		return entity_head_look(entity, head_yaw)

class respawn(_mcp.Base):
	def __init__(_self, dimension, difficulty, gamemode, level_type):
		_self.dimension = dimension
		_self.difficulty = difficulty
		_self.gamemode = gamemode
		_self.level_type = level_type
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(51)
		_raw += _mcp.encode_int(_self.dimension)
		_raw += _mcp.encode_byte(_self.difficulty)
		_raw += _mcp.encode_byte(_self.gamemode)
		_raw += _mcp.encode_string(_self.level_type, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 51:
			raise _mcp.NoMatchError()
		dimension, _off = _mcp.decode_int(_raw, _off)
		difficulty, _off = _mcp.decode_byte(_raw, _off)
		gamemode, _off = _mcp.decode_byte(_raw, _off)
		level_type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return respawn(dimension, difficulty, gamemode, level_type)

class resource_pack(_mcp.Base):
	def __init__(_self, url, hash):
		_self.url = url
		_self.hash = hash
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(50)
		_raw += _mcp.encode_string(_self.url, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.hash, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 50:
			raise _mcp.NoMatchError()
		url, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		hash, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return resource_pack(url, hash)

class remove_effect(_mcp.Base):
	def __init__(_self, entity, effect):
		_self.entity = entity
		_self.effect = effect
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(49)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_byte(_self.effect)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 49:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		effect, _off = _mcp.decode_byte(_raw, _off)
		return remove_effect(entity, effect)

class destroy_entities(_mcp.Base):
	def __init__(_self, entites):
		_self.entites = entites
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(48)
		_raw += _mcp.encode_array(_self.entites, _mcp.encode_varint, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 48:
			raise _mcp.NoMatchError()
		entites, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_varint)
		return destroy_entities(entites)

class use_bed(_mcp.Base):
	def __init__(_self, entity, pos):
		_self.entity = entity
		_self.pos = pos
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(47)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_position(_self.pos)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 47:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		pos, _off = _mcp.decode_position(_raw, _off)
		return use_bed(entity, pos)

class player_position_and_look(_mcp.Base):
	def __init__(_self, x, y, z, yaw, pitch, flags, teleport):
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		_self.flags = flags
		_self.teleport = teleport
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(46)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_float(_self.yaw)
		_raw += _mcp.encode_float(_self.pitch)
		_raw += _mcp.encode_byte(_self.flags)
		_raw += _mcp.encode_varint(_self.teleport)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 46:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_float(_raw, _off)
		flags, _off = _mcp.decode_byte(_raw, _off)
		teleport, _off = _mcp.decode_varint(_raw, _off)
		return player_position_and_look(x, y, z, yaw, pitch, flags, teleport)

class player_list_remove(_mcp.Base):
	def __init__(_self, players):
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(45)
		_raw += _mcp.encode_varint(4)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, _mcp.encode_uuid)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 45:
			raise _mcp.NoMatchError()
		_match8, _off = _mcp.decode_varint(_raw, _off)
		if _match8 != 4:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_uuid)
		return player_list_remove(players)

class player_list_display_name(_mcp.Base):
	def __init__(_self, players):
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(45)
		_raw += _mcp.encode_varint(3)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 45:
			raise _mcp.NoMatchError()
		_match8, _off = _mcp.decode_varint(_raw, _off)
		if _match8 != 3:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, player_displayname.decode)
		return player_list_display_name(players)

class player_list_latency(_mcp.Base):
	def __init__(_self, players):
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(45)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 45:
			raise _mcp.NoMatchError()
		_match8, _off = _mcp.decode_varint(_raw, _off)
		if _match8 != 2:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, uuid_varint.decode)
		return player_list_latency(players)

class player_list_gamemode(_mcp.Base):
	def __init__(_self, players):
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(45)
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 45:
			raise _mcp.NoMatchError()
		_match8, _off = _mcp.decode_varint(_raw, _off)
		if _match8 != 1:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, uuid_varint.decode)
		return player_list_gamemode(players)

class player_list_add(_mcp.Base):
	def __init__(_self, players):
		_self.players = players
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(45)
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_array(_self.players, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 45:
			raise _mcp.NoMatchError()
		_match8, _off = _mcp.decode_varint(_raw, _off)
		if _match8 != 0:
			raise _mcp.NoMatchError()
		players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, player_info.decode)
		return player_list_add(players)

class combat_entity_dead(_mcp.Base):
	def __init__(_self, player, entity, message):
		_self.player = player
		_self.entity = entity
		_self.message = message
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(44)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_varint(_self.player)
		_raw += _mcp.encode_int(_self.entity)
		_raw += _mcp.encode_string(_self.message, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 44:
			raise _mcp.NoMatchError()
		_match7, _off = _mcp.decode_varint(_raw, _off)
		if _match7 != 2:
			raise _mcp.NoMatchError()
		player, _off = _mcp.decode_varint(_raw, _off)
		entity, _off = _mcp.decode_int(_raw, _off)
		message, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return combat_entity_dead(player, entity, message)

class combat_leave(_mcp.Base):
	def __init__(_self, duration, entity):
		_self.duration = duration
		_self.entity = entity
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(44)
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_varint(_self.duration)
		_raw += _mcp.encode_int(_self.entity)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 44:
			raise _mcp.NoMatchError()
		_match7, _off = _mcp.decode_varint(_raw, _off)
		if _match7 != 1:
			raise _mcp.NoMatchError()
		duration, _off = _mcp.decode_varint(_raw, _off)
		entity, _off = _mcp.decode_int(_raw, _off)
		return combat_leave(duration, entity)

class combat_enter(_mcp.Base):
	def __init__(_self):
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(44)
		_raw += _mcp.encode_varint(0)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 44:
			raise _mcp.NoMatchError()
		_match7, _off = _mcp.decode_varint(_raw, _off)
		if _match7 != 0:
			raise _mcp.NoMatchError()
		return combat_enter()

class player_abilities(_mcp.Base):
	def __init__(_self, flags, fly_speed, fov):
		_self.flags = flags
		_self.fly_speed = fly_speed
		_self.fov = fov
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(43)
		_raw += _mcp.encode_byte(_self.flags)
		_raw += _mcp.encode_float(_self.fly_speed)
		_raw += _mcp.encode_float(_self.fov)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 43:
			raise _mcp.NoMatchError()
		flags, _off = _mcp.decode_byte(_raw, _off)
		fly_speed, _off = _mcp.decode_float(_raw, _off)
		fov, _off = _mcp.decode_float(_raw, _off)
		return player_abilities(flags, fly_speed, fov)

class open_sign(_mcp.Base):
	def __init__(_self, pos):
		_self.pos = pos
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(42)
		_raw += _mcp.encode_position(_self.pos)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 42:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		return open_sign(pos)

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
		_raw += _mcp.encode_varint(41)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_float(_self.yaw)
		_raw += _mcp.encode_float(_self.pitch)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 41:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_float(_raw, _off)
		return vehicle_move(x, y, z, yaw, pitch)

class entity(_mcp.Base):
	def __init__(_self, entity):
		_self.entity = entity
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(40)
		_raw += _mcp.encode_varint(_self.entity)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 40:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		return entity(entity)

class entity_look(_mcp.Base):
	def __init__(_self, entity, yaw, pitch, on_ground):
		_self.entity = entity
		_self.yaw = yaw
		_self.pitch = pitch
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(39)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 39:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return entity_look(entity, yaw, pitch, on_ground)

class entity_look_move(_mcp.Base):
	def __init__(_self, entity, dx, dy, dz, yaw, pitch, on_ground):
		_self.entity = entity
		_self.dx = dx
		_self.dy = dy
		_self.dz = dz
		_self.yaw = yaw
		_self.pitch = pitch
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(38)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_short(_self.dx)
		_raw += _mcp.encode_short(_self.dy)
		_raw += _mcp.encode_short(_self.dz)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 38:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		dx, _off = _mcp.decode_short(_raw, _off)
		dy, _off = _mcp.decode_short(_raw, _off)
		dz, _off = _mcp.decode_short(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return entity_look_move(entity, dx, dy, dz, yaw, pitch, on_ground)

class entity_move(_mcp.Base):
	def __init__(_self, entity, dx, dy, dz, on_ground):
		_self.entity = entity
		_self.dx = dx
		_self.dy = dy
		_self.dz = dz
		_self.on_ground = on_ground
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(37)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_short(_self.dx)
		_raw += _mcp.encode_short(_self.dy)
		_raw += _mcp.encode_short(_self.dz)
		_raw += _mcp.encode_bool(_self.on_ground)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 37:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		dx, _off = _mcp.decode_short(_raw, _off)
		dy, _off = _mcp.decode_short(_raw, _off)
		dz, _off = _mcp.decode_short(_raw, _off)
		on_ground, _off = _mcp.decode_bool(_raw, _off)
		return entity_move(entity, dx, dy, dz, on_ground)

class map_data(_mcp.Base):
	def __init__(_self, damage, scale, tracking, icons, columns, rows, x, z, data):
		_self.damage = damage
		_self.scale = scale
		_self.tracking = tracking
		_self.icons = icons
		_self.columns = columns
		_self.rows = rows
		_self.x = x
		_self.z = z
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(36)
		_raw += _mcp.encode_varint(_self.damage)
		_raw += _mcp.encode_byte(_self.scale)
		_raw += _mcp.encode_bool(_self.tracking)
		_raw += _mcp.encode_array(_self.icons, _mcp.encode_varint, (lambda _val: _val.encode()))
		if columns in [0]:
			raise _mcp.NoMatchError()
		_raw += _mcp.encode_byte(_self.columns)
		_raw += _mcp.encode_byte(_self.rows)
		_raw += _mcp.encode_byte(_self.x)
		_raw += _mcp.encode_byte(_self.z)
		_raw += _mcp.encode_array(_self.data, _mcp.encode_varint, _mcp.encode_byte)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 36:
			raise _mcp.NoMatchError()
		damage, _off = _mcp.decode_varint(_raw, _off)
		scale, _off = _mcp.decode_byte(_raw, _off)
		tracking, _off = _mcp.decode_bool(_raw, _off)
		icons, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, map_icon.decode)
		columns, _off = _mcp.decode_byte(_raw, _off)
		if columns in [0]:
			raise _mcp.NoMatchError()
		rows, _off = _mcp.decode_byte(_raw, _off)
		x, _off = _mcp.decode_byte(_raw, _off)
		z, _off = _mcp.decode_byte(_raw, _off)
		data, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_byte)
		return map_data(damage, scale, tracking, icons, columns, rows, x, z, data)

class map(_mcp.Base):
	def __init__(_self, damage, scale, tracking, icons):
		_self.damage = damage
		_self.scale = scale
		_self.tracking = tracking
		_self.icons = icons
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(36)
		_raw += _mcp.encode_varint(_self.damage)
		_raw += _mcp.encode_byte(_self.scale)
		_raw += _mcp.encode_bool(_self.tracking)
		_raw += _mcp.encode_array(_self.icons, _mcp.encode_varint, (lambda _val: _val.encode()))
		_raw += _mcp.encode_byte(0)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 36:
			raise _mcp.NoMatchError()
		damage, _off = _mcp.decode_varint(_raw, _off)
		scale, _off = _mcp.decode_byte(_raw, _off)
		tracking, _off = _mcp.decode_bool(_raw, _off)
		icons, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, map_icon.decode)
		columns, _off = _mcp.decode_byte(_raw, _off)
		if columns != 0:
			raise _mcp.NoMatchError()
		return map(damage, scale, tracking, icons)

class join_game(_mcp.Base):
	def __init__(_self, entity, gamemode, dimension, difficulty, max_players, level_type, reduced_debug):
		_self.entity = entity
		_self.gamemode = gamemode
		_self.dimension = dimension
		_self.difficulty = difficulty
		_self.max_players = max_players
		_self.level_type = level_type
		_self.reduced_debug = reduced_debug
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(35)
		_raw += _mcp.encode_int(_self.entity)
		_raw += _mcp.encode_byte(_self.gamemode)
		_raw += _mcp.encode_byte(_self.dimension)
		_raw += _mcp.encode_byte(_self.difficulty)
		_raw += _mcp.encode_byte(_self.max_players)
		_raw += _mcp.encode_string(_self.level_type, _mcp.encode_varint)
		_raw += _mcp.encode_bool(_self.reduced_debug)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 35:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_int(_raw, _off)
		gamemode, _off = _mcp.decode_byte(_raw, _off)
		dimension, _off = _mcp.decode_byte(_raw, _off)
		difficulty, _off = _mcp.decode_byte(_raw, _off)
		max_players, _off = _mcp.decode_byte(_raw, _off)
		level_type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		reduced_debug, _off = _mcp.decode_bool(_raw, _off)
		return join_game(entity, gamemode, dimension, difficulty, max_players, level_type, reduced_debug)

class particle(_mcp.Base):
	def __init__(_self, particle, far, x, y, z, ox, oy, oz, particle_data, data):
		_self.particle = particle
		_self.far = far
		_self.x = x
		_self.y = y
		_self.z = z
		_self.ox = ox
		_self.oy = oy
		_self.oz = oz
		_self.particle_data = particle_data
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(34)
		_raw += _mcp.encode_int(_self.particle)
		_raw += _mcp.encode_bool(_self.far)
		_raw += _mcp.encode_float(_self.x)
		_raw += _mcp.encode_float(_self.y)
		_raw += _mcp.encode_float(_self.z)
		_raw += _mcp.encode_float(_self.ox)
		_raw += _mcp.encode_float(_self.oy)
		_raw += _mcp.encode_float(_self.oz)
		_raw += _mcp.encode_float(_self.particle_data)
		_raw += _mcp.encode_array(_self.data, _mcp.encode_int, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 34:
			raise _mcp.NoMatchError()
		particle, _off = _mcp.decode_int(_raw, _off)
		far, _off = _mcp.decode_bool(_raw, _off)
		x, _off = _mcp.decode_float(_raw, _off)
		y, _off = _mcp.decode_float(_raw, _off)
		z, _off = _mcp.decode_float(_raw, _off)
		ox, _off = _mcp.decode_float(_raw, _off)
		oy, _off = _mcp.decode_float(_raw, _off)
		oz, _off = _mcp.decode_float(_raw, _off)
		particle_data, _off = _mcp.decode_float(_raw, _off)
		data, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, _mcp.decode_varint)
		return particle(particle, far, x, y, z, ox, oy, oz, particle_data, data)

class effect(_mcp.Base):
	def __init__(_self, effect, pos, data, volume):
		_self.effect = effect
		_self.pos = pos
		_self.data = data
		_self.volume = volume
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(33)
		_raw += _mcp.encode_int(_self.effect)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_int(_self.data)
		_raw += _mcp.encode_bool(_self.volume)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 33:
			raise _mcp.NoMatchError()
		effect, _off = _mcp.decode_int(_raw, _off)
		pos, _off = _mcp.decode_position(_raw, _off)
		data, _off = _mcp.decode_int(_raw, _off)
		volume, _off = _mcp.decode_bool(_raw, _off)
		return effect(effect, pos, data, volume)

class chunk_data(_mcp.Base):
	def __init__(_self, ch_x, ch_z, biomes, bitmask, data):
		_self.ch_x = ch_x
		_self.ch_z = ch_z
		_self.biomes = biomes
		_self.bitmask = bitmask
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(32)
		_raw += _mcp.encode_int(_self.ch_x)
		_raw += _mcp.encode_int(_self.ch_z)
		_raw += _mcp.encode_bool(_self.biomes)
		_raw += _mcp.encode_varint(_self.bitmask)
		_raw += _mcp.encode_bytes(_self.data, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 32:
			raise _mcp.NoMatchError()
		ch_x, _off = _mcp.decode_int(_raw, _off)
		ch_z, _off = _mcp.decode_int(_raw, _off)
		biomes, _off = _mcp.decode_bool(_raw, _off)
		bitmask, _off = _mcp.decode_varint(_raw, _off)
		data, _off = _mcp.decode_bytes(_raw, _off, _mcp.decode_varint)
		return chunk_data(ch_x, ch_z, biomes, bitmask, data)

class keepalive(_mcp.Base):
	def __init__(_self, timestamp):
		_self.timestamp = timestamp
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(31)
		_raw += _mcp.encode_varint(_self.timestamp)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 31:
			raise _mcp.NoMatchError()
		timestamp, _off = _mcp.decode_varint(_raw, _off)
		return keepalive(timestamp)

class change_game_state(_mcp.Base):
	def __init__(_self, reason, value):
		_self.reason = reason
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(30)
		_raw += _mcp.encode_byte(_self.reason)
		_raw += _mcp.encode_float(_self.value)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 30:
			raise _mcp.NoMatchError()
		reason, _off = _mcp.decode_byte(_raw, _off)
		value, _off = _mcp.decode_float(_raw, _off)
		return change_game_state(reason, value)

class unload_chunk(_mcp.Base):
	def __init__(_self, ch_x, ch_z):
		_self.ch_x = ch_x
		_self.ch_z = ch_z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(29)
		_raw += _mcp.encode_int(_self.ch_x)
		_raw += _mcp.encode_int(_self.ch_z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 29:
			raise _mcp.NoMatchError()
		ch_x, _off = _mcp.decode_int(_raw, _off)
		ch_z, _off = _mcp.decode_int(_raw, _off)
		return unload_chunk(ch_x, ch_z)

class explosion(_mcp.Base):
	def __init__(_self, x, y, z, r, records, pv_x, pv_y, pv_z):
		_self.x = x
		_self.y = y
		_self.z = z
		_self.r = r
		_self.records = records
		_self.pv_x = pv_x
		_self.pv_y = pv_y
		_self.pv_z = pv_z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(28)
		_raw += _mcp.encode_float(_self.x)
		_raw += _mcp.encode_float(_self.y)
		_raw += _mcp.encode_float(_self.z)
		_raw += _mcp.encode_float(_self.r)
		_raw += _mcp.encode_array(_self.records, _mcp.encode_int, (lambda _val: _val.encode()))
		_raw += _mcp.encode_float(_self.pv_x)
		_raw += _mcp.encode_float(_self.pv_y)
		_raw += _mcp.encode_float(_self.pv_z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 28:
			raise _mcp.NoMatchError()
		x, _off = _mcp.decode_float(_raw, _off)
		y, _off = _mcp.decode_float(_raw, _off)
		z, _off = _mcp.decode_float(_raw, _off)
		r, _off = _mcp.decode_float(_raw, _off)
		records, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, explosion_record.decode)
		pv_x, _off = _mcp.decode_float(_raw, _off)
		pv_y, _off = _mcp.decode_float(_raw, _off)
		pv_z, _off = _mcp.decode_float(_raw, _off)
		return explosion(x, y, z, r, records, pv_x, pv_y, pv_z)

class entity_status(_mcp.Base):
	def __init__(_self, entity, status):
		_self.entity = entity
		_self.status = status
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(27)
		_raw += _mcp.encode_int(_self.entity)
		_raw += _mcp.encode_byte(_self.status)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 27:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_int(_raw, _off)
		status, _off = _mcp.decode_byte(_raw, _off)
		return entity_status(entity, status)

class disconnect(_mcp.Base):
	def __init__(_self, reason):
		_self.reason = reason
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(26)
		_raw += _mcp.encode_string(_self.reason, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 26:
			raise _mcp.NoMatchError()
		reason, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return disconnect(reason)

class named_sound(_mcp.Base):
	def __init__(_self, name, category, x, y, z, volume, pitch):
		_self.name = name
		_self.category = category
		_self.x = x
		_self.y = y
		_self.z = z
		_self.volume = volume
		_self.pitch = pitch
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(25)
		_raw += _mcp.encode_string(_self.name, _mcp.encode_varint)
		_raw += _mcp.encode_varint(_self.category)
		_raw += _mcp.encode_int(_self.x)
		_raw += _mcp.encode_int(_self.y)
		_raw += _mcp.encode_int(_self.z)
		_raw += _mcp.encode_float(_self.volume)
		_raw += _mcp.encode_byte(_self.pitch)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 25:
			raise _mcp.NoMatchError()
		name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		category, _off = _mcp.decode_varint(_raw, _off)
		x, _off = _mcp.decode_int(_raw, _off)
		y, _off = _mcp.decode_int(_raw, _off)
		z, _off = _mcp.decode_int(_raw, _off)
		volume, _off = _mcp.decode_float(_raw, _off)
		pitch, _off = _mcp.decode_byte(_raw, _off)
		return named_sound(name, category, x, y, z, volume, pitch)

class plugin_message(_mcp.Base):
	def __init__(_self, channel, data):
		_self.channel = channel
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(24)
		_raw += _mcp.encode_string(_self.channel, _mcp.encode_varint)
		_raw += _mcp.encode_bytes_eof(_self.data)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 24:
			raise _mcp.NoMatchError()
		channel, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		data, _off = _mcp.decode_bytes_eof(_raw, _off)
		return plugin_message(channel, data)

class set_cooldown(_mcp.Base):
	def __init__(_self, item, cooldown_ticks):
		_self.item = item
		_self.cooldown_ticks = cooldown_ticks
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(23)
		_raw += _mcp.encode_varint(_self.item)
		_raw += _mcp.encode_varint(_self.cooldown_ticks)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 23:
			raise _mcp.NoMatchError()
		item, _off = _mcp.decode_varint(_raw, _off)
		cooldown_ticks, _off = _mcp.decode_varint(_raw, _off)
		return set_cooldown(item, cooldown_ticks)

class set_slot(_mcp.Base):
	def __init__(_self, window, slot, item):
		_self.window = window
		_self.slot = slot
		_self.item = item
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(22)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_short(_self.slot)
		_raw += _mcp.encode_slot(_self.item)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 22:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		slot, _off = _mcp.decode_short(_raw, _off)
		item, _off = _mcp.decode_slot(_raw, _off)
		return set_slot(window, slot, item)

class window_property(_mcp.Base):
	def __init__(_self, window, property, value):
		_self.window = window
		_self.property = property
		_self.value = value
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(21)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_short(_self.property)
		_raw += _mcp.encode_short(_self.value)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 21:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		property, _off = _mcp.decode_short(_raw, _off)
		value, _off = _mcp.decode_short(_raw, _off)
		return window_property(window, property, value)

class window_items(_mcp.Base):
	def __init__(_self, window, items):
		_self.window = window
		_self.items = items
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(20)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_array(_self.items, _mcp.encode_short, _mcp.encode_slot)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 20:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		items, _off = _mcp.decode_array(_raw, _off, _mcp.decode_short, _mcp.decode_slot)
		return window_items(window, items)

class open_window(_mcp.Base):
	def __init__(_self, window, type, title, num_slots):
		_self.window = window
		_self.type = type
		_self.title = title
		_self.num_slots = num_slots
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(19)
		_raw += _mcp.encode_byte(_self.window)
		if _self.type in ["EntityHorse"]:
			raise _mcp.NoMatchError()
		_raw += _mcp.encode_string(_self.type, _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.title, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.num_slots)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 19:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		if type in ["EntityHorse"]:
			raise _mcp.NoMatchError()
		title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		num_slots, _off = _mcp.decode_byte(_raw, _off)
		return open_window(window, type, title, num_slots)

class open_horse_window(_mcp.Base):
	def __init__(_self, window, title, num_slots, entity):
		_self.window = window
		_self.title = title
		_self.num_slots = num_slots
		_self.entity = entity
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(19)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_string("EntityHorse", _mcp.encode_varint)
		_raw += _mcp.encode_string(_self.title, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.num_slots)
		_raw += _mcp.encode_int(_self.entity)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 19:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		if type != "EntityHorse":
			raise _mcp.NoMatchError()
		title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		num_slots, _off = _mcp.decode_byte(_raw, _off)
		entity, _off = _mcp.decode_int(_raw, _off)
		return open_horse_window(window, title, num_slots, entity)

class close_window(_mcp.Base):
	def __init__(_self, window):
		_self.window = window
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(18)
		_raw += _mcp.encode_byte(_self.window)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 18:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		return close_window(window)

class confirm_transaction(_mcp.Base):
	def __init__(_self, window, action, accepted):
		_self.window = window
		_self.action = action
		_self.accepted = accepted
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(17)
		_raw += _mcp.encode_byte(_self.window)
		_raw += _mcp.encode_short(_self.action)
		_raw += _mcp.encode_bool(_self.accepted)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 17:
			raise _mcp.NoMatchError()
		window, _off = _mcp.decode_byte(_raw, _off)
		action, _off = _mcp.decode_short(_raw, _off)
		accepted, _off = _mcp.decode_bool(_raw, _off)
		return confirm_transaction(window, action, accepted)

class multi_block_change(_mcp.Base):
	def __init__(_self, chunk_x, chunk_y, records):
		_self.chunk_x = chunk_x
		_self.chunk_y = chunk_y
		_self.records = records
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(16)
		_raw += _mcp.encode_int(_self.chunk_x)
		_raw += _mcp.encode_int(_self.chunk_y)
		_raw += _mcp.encode_array(_self.records, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 16:
			raise _mcp.NoMatchError()
		chunk_x, _off = _mcp.decode_int(_raw, _off)
		chunk_y, _off = _mcp.decode_int(_raw, _off)
		records, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, block_change_record.decode)
		return multi_block_change(chunk_x, chunk_y, records)

class chat_message(_mcp.Base):
	def __init__(_self, message, position):
		_self.message = message
		_self.position = position
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(15)
		_raw += _mcp.encode_string(_self.message, _mcp.encode_varint)
		_raw += _mcp.encode_byte(_self.position)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 15:
			raise _mcp.NoMatchError()
		message, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		position, _off = _mcp.decode_byte(_raw, _off)
		return chat_message(message, position)

class tab_complete(_mcp.Base):
	def __init__(_self, matches):
		_self.matches = matches
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(14)
		_raw += _mcp.encode_array(_self.matches, _mcp.encode_varint, (lambda _val: _mcp.encode_string(_val, _mcp.encode_varint)))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 14:
			raise _mcp.NoMatchError()
		matches, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
		return tab_complete(matches)

class server_difficulty(_mcp.Base):
	def __init__(_self, difficulty):
		_self.difficulty = difficulty
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(13)
		_raw += _mcp.encode_byte(_self.difficulty)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 13:
			raise _mcp.NoMatchError()
		difficulty, _off = _mcp.decode_byte(_raw, _off)
		return server_difficulty(difficulty)

class boss_bar_flags(_mcp.Base):
	def __init__(_self, uuid, flags):
		_self.uuid = uuid
		_self.flags = flags
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(5)
		_raw += _mcp.encode_byte(_self.flags)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 5:
			raise _mcp.NoMatchError()
		flags, _off = _mcp.decode_byte(_raw, _off)
		return boss_bar_flags(uuid, flags)

class boss_bar_style(_mcp.Base):
	def __init__(_self, uuid, color, dividers):
		_self.uuid = uuid
		_self.color = color
		_self.dividers = dividers
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(4)
		_raw += _mcp.encode_varint(_self.color)
		_raw += _mcp.encode_varint(_self.dividers)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 4:
			raise _mcp.NoMatchError()
		color, _off = _mcp.decode_varint(_raw, _off)
		dividers, _off = _mcp.decode_varint(_raw, _off)
		return boss_bar_style(uuid, color, dividers)

class boss_bar_title(_mcp.Base):
	def __init__(_self, uuid, title):
		_self.uuid = uuid
		_self.title = title
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(3)
		_raw += _mcp.encode_string(_self.title, _mcp.encode_varint)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 3:
			raise _mcp.NoMatchError()
		title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		return boss_bar_title(uuid, title)

class boss_bar_health(_mcp.Base):
	def __init__(_self, uuid, health):
		_self.uuid = uuid
		_self.health = health
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_float(_self.health)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 2:
			raise _mcp.NoMatchError()
		health, _off = _mcp.decode_float(_raw, _off)
		return boss_bar_health(uuid, health)

class remove_boss_bar(_mcp.Base):
	def __init__(_self, uuid):
		_self.uuid = uuid
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(1)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 1:
			raise _mcp.NoMatchError()
		return remove_boss_bar(uuid)

class new_boss_bar(_mcp.Base):
	def __init__(_self, uuid, title, health, color, division, flags):
		_self.uuid = uuid
		_self.title = title
		_self.health = health
		_self.color = color
		_self.division = division
		_self.flags = flags
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(12)
		_raw += _mcp.encode_uuid(_self.uuid)
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_string(_self.title, _mcp.encode_varint)
		_raw += _mcp.encode_float(_self.health)
		_raw += _mcp.encode_varint(_self.color)
		_raw += _mcp.encode_varint(_self.division)
		_raw += _mcp.encode_byte(_self.flags)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 12:
			raise _mcp.NoMatchError()
		uuid, _off = _mcp.decode_uuid(_raw, _off)
		_match6, _off = _mcp.decode_varint(_raw, _off)
		if _match6 != 0:
			raise _mcp.NoMatchError()
		title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		health, _off = _mcp.decode_float(_raw, _off)
		color, _off = _mcp.decode_varint(_raw, _off)
		division, _off = _mcp.decode_varint(_raw, _off)
		flags, _off = _mcp.decode_byte(_raw, _off)
		return new_boss_bar(uuid, title, health, color, division, flags)

class block_change(_mcp.Base):
	def __init__(_self, pos, block_data):
		_self.pos = pos
		_self.block_data = block_data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(11)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_varint(_self.block_data)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 11:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		block_data, _off = _mcp.decode_varint(_raw, _off)
		return block_change(pos, block_data)

class block_action(_mcp.Base):
	def __init__(_self, pos, byte1, byte2, block_type):
		_self.pos = pos
		_self.byte1 = byte1
		_self.byte2 = byte2
		_self.block_type = block_type
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(10)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_byte(_self.byte1)
		_raw += _mcp.encode_byte(_self.byte2)
		_raw += _mcp.encode_varint(_self.block_type)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 10:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		byte1, _off = _mcp.decode_byte(_raw, _off)
		byte2, _off = _mcp.decode_byte(_raw, _off)
		block_type, _off = _mcp.decode_varint(_raw, _off)
		return block_action(pos, byte1, byte2, block_type)

class update_block_entity(_mcp.Base):
	def __init__(_self, pos, action, data):
		_self.pos = pos
		_self.action = action
		_self.data = data
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(9)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_byte(_self.action)
		_raw += _mcp.encode_nbt(_self.data)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 9:
			raise _mcp.NoMatchError()
		pos, _off = _mcp.decode_position(_raw, _off)
		action, _off = _mcp.decode_byte(_raw, _off)
		data, _off = _mcp.decode_nbt(_raw, _off)
		return update_block_entity(pos, action, data)

class block_break_animation(_mcp.Base):
	def __init__(_self, entity, pos, stage):
		_self.entity = entity
		_self.pos = pos
		_self.stage = stage
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(8)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_position(_self.pos)
		_raw += _mcp.encode_byte(_self.stage)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 8:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		pos, _off = _mcp.decode_position(_raw, _off)
		stage, _off = _mcp.decode_byte(_raw, _off)
		return block_break_animation(entity, pos, stage)

class statistics(_mcp.Base):
	def __init__(_self, statistics):
		_self.statistics = statistics
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(7)
		_raw += _mcp.encode_array(_self.statistics, _mcp.encode_varint, (lambda _val: _val.encode()))
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 7:
			raise _mcp.NoMatchError()
		statistics, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, statistic.decode)
		return statistics(statistics)

class animation(_mcp.Base):
	def __init__(_self, entity, animation):
		_self.entity = entity
		_self.animation = animation
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(6)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_byte(_self.animation)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 6:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		animation, _off = _mcp.decode_byte(_raw, _off)
		return animation(entity, animation)

class spawn_player(_mcp.Base):
	def __init__(_self, entity, player_uuid, x, y, z, yaw, pitch, metadata):
		_self.entity = entity
		_self.player_uuid = player_uuid
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		_self.metadata = metadata
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(5)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_uuid(_self.player_uuid)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_bytes_eof(_self.metadata)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 5:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		player_uuid, _off = _mcp.decode_uuid(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
		return spawn_player(entity, player_uuid, x, y, z, yaw, pitch, metadata)

class spawn_painting(_mcp.Base):
	def __init__(_self, entity, entity_uuid, title, location, direction):
		_self.entity = entity
		_self.entity_uuid = entity_uuid
		_self.title = title
		_self.location = location
		_self.direction = direction
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(4)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_uuid(_self.entity_uuid)
		_raw += _mcp.encode_string(_self.title, _mcp.encode_varint)
		_raw += _mcp.encode_position(_self.location)
		_raw += _mcp.encode_byte(_self.direction)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 4:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		entity_uuid, _off = _mcp.decode_uuid(_raw, _off)
		title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
		location, _off = _mcp.decode_position(_raw, _off)
		direction, _off = _mcp.decode_byte(_raw, _off)
		return spawn_painting(entity, entity_uuid, title, location, direction)

class spawn_mob(_mcp.Base):
	def __init__(_self, entity, entity_uuid, type, x, y, z, yaw, pitch, head_pitch, v_x, v_y, v_z, metadata):
		_self.entity = entity
		_self.entity_uuid = entity_uuid
		_self.type = type
		_self.x = x
		_self.y = y
		_self.z = z
		_self.yaw = yaw
		_self.pitch = pitch
		_self.head_pitch = head_pitch
		_self.v_x = v_x
		_self.v_y = v_y
		_self.v_z = v_z
		_self.metadata = metadata
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(3)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_uuid(_self.entity_uuid)
		_raw += _mcp.encode_byte(_self.type)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_angle(_self.head_pitch)
		_raw += _mcp.encode_short(_self.v_x)
		_raw += _mcp.encode_short(_self.v_y)
		_raw += _mcp.encode_short(_self.v_z)
		_raw += _mcp.encode_bytes_eof(_self.metadata)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 3:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		entity_uuid, _off = _mcp.decode_uuid(_raw, _off)
		type, _off = _mcp.decode_byte(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		head_pitch, _off = _mcp.decode_angle(_raw, _off)
		v_x, _off = _mcp.decode_short(_raw, _off)
		v_y, _off = _mcp.decode_short(_raw, _off)
		v_z, _off = _mcp.decode_short(_raw, _off)
		metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
		return spawn_mob(entity, entity_uuid, type, x, y, z, yaw, pitch, head_pitch, v_x, v_y, v_z, metadata)

class spawn_global_entity(_mcp.Base):
	def __init__(_self, entity, type, x, y, z):
		_self.entity = entity
		_self.type = type
		_self.x = x
		_self.y = y
		_self.z = z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(2)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_byte(_self.type)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 2:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		type, _off = _mcp.decode_byte(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		return spawn_global_entity(entity, type, x, y, z)

class spawn_xp_orb(_mcp.Base):
	def __init__(_self, entity, x, y, z, count):
		_self.entity = entity
		_self.x = x
		_self.y = y
		_self.z = z
		_self.count = count
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(1)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_short(_self.count)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 1:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		count, _off = _mcp.decode_short(_raw, _off)
		return spawn_xp_orb(entity, x, y, z, count)

class spawn_object(_mcp.Base):
	def __init__(_self, entity, object_uuid, type, x, y, z, pitch, yaw, data, v_x, v_y, v_z):
		_self.entity = entity
		_self.object_uuid = object_uuid
		_self.type = type
		_self.x = x
		_self.y = y
		_self.z = z
		_self.pitch = pitch
		_self.yaw = yaw
		_self.data = data
		_self.v_x = v_x
		_self.v_y = v_y
		_self.v_z = v_z
		return
	def encode(_self):
		_raw = bytes()
		_raw += _mcp.encode_varint(0)
		_raw += _mcp.encode_varint(_self.entity)
		_raw += _mcp.encode_uuid(_self.object_uuid)
		_raw += _mcp.encode_byte(_self.type)
		_raw += _mcp.encode_double(_self.x)
		_raw += _mcp.encode_double(_self.y)
		_raw += _mcp.encode_double(_self.z)
		_raw += _mcp.encode_angle(_self.pitch)
		_raw += _mcp.encode_angle(_self.yaw)
		_raw += _mcp.encode_int(_self.data)
		_raw += _mcp.encode_short(_self.v_x)
		_raw += _mcp.encode_short(_self.v_y)
		_raw += _mcp.encode_short(_self.v_z)
		return _raw
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if _match5 != 0:
			raise _mcp.NoMatchError()
		entity, _off = _mcp.decode_varint(_raw, _off)
		object_uuid, _off = _mcp.decode_uuid(_raw, _off)
		type, _off = _mcp.decode_byte(_raw, _off)
		x, _off = _mcp.decode_double(_raw, _off)
		y, _off = _mcp.decode_double(_raw, _off)
		z, _off = _mcp.decode_double(_raw, _off)
		pitch, _off = _mcp.decode_angle(_raw, _off)
		yaw, _off = _mcp.decode_angle(_raw, _off)
		data, _off = _mcp.decode_int(_raw, _off)
		v_x, _off = _mcp.decode_short(_raw, _off)
		v_y, _off = _mcp.decode_short(_raw, _off)
		v_z, _off = _mcp.decode_short(_raw, _off)
		return spawn_object(entity, object_uuid, type, x, y, z, pitch, yaw, data, v_x, v_y, v_z)

class play107(_mcp.Base):
	@staticmethod
	def decode(_raw, _off=0):
		_match5, _off = _mcp.decode_varint(_raw, _off)
		if false:
			pass
		elif _match5 == 0:
			entity, _off = _mcp.decode_varint(_raw, _off)
			object_uuid, _off = _mcp.decode_uuid(_raw, _off)
			type, _off = _mcp.decode_byte(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			data, _off = _mcp.decode_int(_raw, _off)
			v_x, _off = _mcp.decode_short(_raw, _off)
			v_y, _off = _mcp.decode_short(_raw, _off)
			v_z, _off = _mcp.decode_short(_raw, _off)
			return spawn_object(entity, object_uuid, type, x, y, z, pitch, yaw, data, v_x, v_y, v_z)
		elif _match5 == 1:
			entity, _off = _mcp.decode_varint(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			count, _off = _mcp.decode_short(_raw, _off)
			return spawn_xp_orb(entity, x, y, z, count)
		elif _match5 == 2:
			entity, _off = _mcp.decode_varint(_raw, _off)
			type, _off = _mcp.decode_byte(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			return spawn_global_entity(entity, type, x, y, z)
		elif _match5 == 3:
			entity, _off = _mcp.decode_varint(_raw, _off)
			entity_uuid, _off = _mcp.decode_uuid(_raw, _off)
			type, _off = _mcp.decode_byte(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			head_pitch, _off = _mcp.decode_angle(_raw, _off)
			v_x, _off = _mcp.decode_short(_raw, _off)
			v_y, _off = _mcp.decode_short(_raw, _off)
			v_z, _off = _mcp.decode_short(_raw, _off)
			metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
			return spawn_mob(entity, entity_uuid, type, x, y, z, yaw, pitch, head_pitch, v_x, v_y, v_z, metadata)
		elif _match5 == 4:
			entity, _off = _mcp.decode_varint(_raw, _off)
			entity_uuid, _off = _mcp.decode_uuid(_raw, _off)
			title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			location, _off = _mcp.decode_position(_raw, _off)
			direction, _off = _mcp.decode_byte(_raw, _off)
			return spawn_painting(entity, entity_uuid, title, location, direction)
		elif _match5 == 5:
			entity, _off = _mcp.decode_varint(_raw, _off)
			player_uuid, _off = _mcp.decode_uuid(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
			return spawn_player(entity, player_uuid, x, y, z, yaw, pitch, metadata)
		elif _match5 == 6:
			entity, _off = _mcp.decode_varint(_raw, _off)
			animation, _off = _mcp.decode_byte(_raw, _off)
			return animation(entity, animation)
		elif _match5 == 7:
			statistics, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, statistic.decode)
			return statistics(statistics)
		elif _match5 == 8:
			entity, _off = _mcp.decode_varint(_raw, _off)
			pos, _off = _mcp.decode_position(_raw, _off)
			stage, _off = _mcp.decode_byte(_raw, _off)
			return block_break_animation(entity, pos, stage)
		elif _match5 == 9:
			pos, _off = _mcp.decode_position(_raw, _off)
			action, _off = _mcp.decode_byte(_raw, _off)
			data, _off = _mcp.decode_nbt(_raw, _off)
			return update_block_entity(pos, action, data)
		elif _match5 == 10:
			pos, _off = _mcp.decode_position(_raw, _off)
			byte1, _off = _mcp.decode_byte(_raw, _off)
			byte2, _off = _mcp.decode_byte(_raw, _off)
			block_type, _off = _mcp.decode_varint(_raw, _off)
			return block_action(pos, byte1, byte2, block_type)
		elif _match5 == 11:
			pos, _off = _mcp.decode_position(_raw, _off)
			block_data, _off = _mcp.decode_varint(_raw, _off)
			return block_change(pos, block_data)
		elif _match5 == 12:
			uuid, _off = _mcp.decode_uuid(_raw, _off)
			_match6, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match6 == 0:
				title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				health, _off = _mcp.decode_float(_raw, _off)
				color, _off = _mcp.decode_varint(_raw, _off)
				division, _off = _mcp.decode_varint(_raw, _off)
				flags, _off = _mcp.decode_byte(_raw, _off)
				return new_boss_bar(title, health, color, division, flags)
			elif _match6 == 1:
				return remove_boss_bar()
			elif _match6 == 2:
				health, _off = _mcp.decode_float(_raw, _off)
				return boss_bar_health(health)
			elif _match6 == 3:
				title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return boss_bar_title(title)
			elif _match6 == 4:
				color, _off = _mcp.decode_varint(_raw, _off)
				dividers, _off = _mcp.decode_varint(_raw, _off)
				return boss_bar_style(color, dividers)
			elif _match6 == 5:
				flags, _off = _mcp.decode_byte(_raw, _off)
				return boss_bar_flags(flags)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 13:
			difficulty, _off = _mcp.decode_byte(_raw, _off)
			return server_difficulty(difficulty)
		elif _match5 == 14:
			matches, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
			return tab_complete(matches)
		elif _match5 == 15:
			message, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			position, _off = _mcp.decode_byte(_raw, _off)
			return chat_message(message, position)
		elif _match5 == 16:
			chunk_x, _off = _mcp.decode_int(_raw, _off)
			chunk_y, _off = _mcp.decode_int(_raw, _off)
			records, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, block_change_record.decode)
			return multi_block_change(chunk_x, chunk_y, records)
		elif _match5 == 17:
			window, _off = _mcp.decode_byte(_raw, _off)
			action, _off = _mcp.decode_short(_raw, _off)
			accepted, _off = _mcp.decode_bool(_raw, _off)
			return confirm_transaction(window, action, accepted)
		elif _match5 == 18:
			window, _off = _mcp.decode_byte(_raw, _off)
			return close_window(window)
		elif _match5 == 19:
			window, _off = _mcp.decode_byte(_raw, _off)
			type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			title, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			num_slots, _off = _mcp.decode_byte(_raw, _off)
			if false:
				pass
			elif type == "EntityHorse":
				entity, _off = _mcp.decode_int(_raw, _off)
				return open_horse_window(entity)
			else:
				return open_window()
		elif _match5 == 20:
			window, _off = _mcp.decode_byte(_raw, _off)
			items, _off = _mcp.decode_array(_raw, _off, _mcp.decode_short, _mcp.decode_slot)
			return window_items(window, items)
		elif _match5 == 21:
			window, _off = _mcp.decode_byte(_raw, _off)
			property, _off = _mcp.decode_short(_raw, _off)
			value, _off = _mcp.decode_short(_raw, _off)
			return window_property(window, property, value)
		elif _match5 == 22:
			window, _off = _mcp.decode_byte(_raw, _off)
			slot, _off = _mcp.decode_short(_raw, _off)
			item, _off = _mcp.decode_slot(_raw, _off)
			return set_slot(window, slot, item)
		elif _match5 == 23:
			item, _off = _mcp.decode_varint(_raw, _off)
			cooldown_ticks, _off = _mcp.decode_varint(_raw, _off)
			return set_cooldown(item, cooldown_ticks)
		elif _match5 == 24:
			channel, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			data, _off = _mcp.decode_bytes_eof(_raw, _off)
			return plugin_message(channel, data)
		elif _match5 == 25:
			name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			category, _off = _mcp.decode_varint(_raw, _off)
			x, _off = _mcp.decode_int(_raw, _off)
			y, _off = _mcp.decode_int(_raw, _off)
			z, _off = _mcp.decode_int(_raw, _off)
			volume, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_byte(_raw, _off)
			return named_sound(name, category, x, y, z, volume, pitch)
		elif _match5 == 26:
			reason, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return disconnect(reason)
		elif _match5 == 27:
			entity, _off = _mcp.decode_int(_raw, _off)
			status, _off = _mcp.decode_byte(_raw, _off)
			return entity_status(entity, status)
		elif _match5 == 28:
			x, _off = _mcp.decode_float(_raw, _off)
			y, _off = _mcp.decode_float(_raw, _off)
			z, _off = _mcp.decode_float(_raw, _off)
			r, _off = _mcp.decode_float(_raw, _off)
			records, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, explosion_record.decode)
			pv_x, _off = _mcp.decode_float(_raw, _off)
			pv_y, _off = _mcp.decode_float(_raw, _off)
			pv_z, _off = _mcp.decode_float(_raw, _off)
			return explosion(x, y, z, r, records, pv_x, pv_y, pv_z)
		elif _match5 == 29:
			ch_x, _off = _mcp.decode_int(_raw, _off)
			ch_z, _off = _mcp.decode_int(_raw, _off)
			return unload_chunk(ch_x, ch_z)
		elif _match5 == 30:
			reason, _off = _mcp.decode_byte(_raw, _off)
			value, _off = _mcp.decode_float(_raw, _off)
			return change_game_state(reason, value)
		elif _match5 == 31:
			timestamp, _off = _mcp.decode_varint(_raw, _off)
			return keepalive(timestamp)
		elif _match5 == 32:
			ch_x, _off = _mcp.decode_int(_raw, _off)
			ch_z, _off = _mcp.decode_int(_raw, _off)
			biomes, _off = _mcp.decode_bool(_raw, _off)
			bitmask, _off = _mcp.decode_varint(_raw, _off)
			data, _off = _mcp.decode_bytes(_raw, _off, _mcp.decode_varint)
			return chunk_data(ch_x, ch_z, biomes, bitmask, data)
		elif _match5 == 33:
			effect, _off = _mcp.decode_int(_raw, _off)
			pos, _off = _mcp.decode_position(_raw, _off)
			data, _off = _mcp.decode_int(_raw, _off)
			volume, _off = _mcp.decode_bool(_raw, _off)
			return effect(effect, pos, data, volume)
		elif _match5 == 34:
			particle, _off = _mcp.decode_int(_raw, _off)
			far, _off = _mcp.decode_bool(_raw, _off)
			x, _off = _mcp.decode_float(_raw, _off)
			y, _off = _mcp.decode_float(_raw, _off)
			z, _off = _mcp.decode_float(_raw, _off)
			ox, _off = _mcp.decode_float(_raw, _off)
			oy, _off = _mcp.decode_float(_raw, _off)
			oz, _off = _mcp.decode_float(_raw, _off)
			particle_data, _off = _mcp.decode_float(_raw, _off)
			data, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, _mcp.decode_varint)
			return particle(particle, far, x, y, z, ox, oy, oz, particle_data, data)
		elif _match5 == 35:
			entity, _off = _mcp.decode_int(_raw, _off)
			gamemode, _off = _mcp.decode_byte(_raw, _off)
			dimension, _off = _mcp.decode_byte(_raw, _off)
			difficulty, _off = _mcp.decode_byte(_raw, _off)
			max_players, _off = _mcp.decode_byte(_raw, _off)
			level_type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			reduced_debug, _off = _mcp.decode_bool(_raw, _off)
			return join_game(entity, gamemode, dimension, difficulty, max_players, level_type, reduced_debug)
		elif _match5 == 36:
			damage, _off = _mcp.decode_varint(_raw, _off)
			scale, _off = _mcp.decode_byte(_raw, _off)
			tracking, _off = _mcp.decode_bool(_raw, _off)
			icons, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, map_icon.decode)
			columns, _off = _mcp.decode_byte(_raw, _off)
			if false:
				pass
			elif columns == 0:
				return map()
			else:
				rows, _off = _mcp.decode_byte(_raw, _off)
				x, _off = _mcp.decode_byte(_raw, _off)
				z, _off = _mcp.decode_byte(_raw, _off)
				data, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_byte)
				return map_data(rows, x, z, data)
		elif _match5 == 37:
			entity, _off = _mcp.decode_varint(_raw, _off)
			dx, _off = _mcp.decode_short(_raw, _off)
			dy, _off = _mcp.decode_short(_raw, _off)
			dz, _off = _mcp.decode_short(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return entity_move(entity, dx, dy, dz, on_ground)
		elif _match5 == 38:
			entity, _off = _mcp.decode_varint(_raw, _off)
			dx, _off = _mcp.decode_short(_raw, _off)
			dy, _off = _mcp.decode_short(_raw, _off)
			dz, _off = _mcp.decode_short(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return entity_look_move(entity, dx, dy, dz, yaw, pitch, on_ground)
		elif _match5 == 39:
			entity, _off = _mcp.decode_varint(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return entity_look(entity, yaw, pitch, on_ground)
		elif _match5 == 40:
			entity, _off = _mcp.decode_varint(_raw, _off)
			return entity(entity)
		elif _match5 == 41:
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_float(_raw, _off)
			return vehicle_move(x, y, z, yaw, pitch)
		elif _match5 == 42:
			pos, _off = _mcp.decode_position(_raw, _off)
			return open_sign(pos)
		elif _match5 == 43:
			flags, _off = _mcp.decode_byte(_raw, _off)
			fly_speed, _off = _mcp.decode_float(_raw, _off)
			fov, _off = _mcp.decode_float(_raw, _off)
			return player_abilities(flags, fly_speed, fov)
		elif _match5 == 44:
			_match7, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match7 == 0:
				return combat_enter()
			elif _match7 == 1:
				duration, _off = _mcp.decode_varint(_raw, _off)
				entity, _off = _mcp.decode_int(_raw, _off)
				return combat_leave(duration, entity)
			elif _match7 == 2:
				player, _off = _mcp.decode_varint(_raw, _off)
				entity, _off = _mcp.decode_int(_raw, _off)
				message, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return combat_entity_dead(player, entity, message)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 45:
			_match8, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match8 == 0:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, player_info.decode)
				return player_list_add(players)
			elif _match8 == 1:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, uuid_varint.decode)
				return player_list_gamemode(players)
			elif _match8 == 2:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, uuid_varint.decode)
				return player_list_latency(players)
			elif _match8 == 3:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, player_displayname.decode)
				return player_list_display_name(players)
			elif _match8 == 4:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_uuid)
				return player_list_remove(players)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 46:
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_float(_raw, _off)
			flags, _off = _mcp.decode_byte(_raw, _off)
			teleport, _off = _mcp.decode_varint(_raw, _off)
			return player_position_and_look(x, y, z, yaw, pitch, flags, teleport)
		elif _match5 == 47:
			entity, _off = _mcp.decode_varint(_raw, _off)
			pos, _off = _mcp.decode_position(_raw, _off)
			return use_bed(entity, pos)
		elif _match5 == 48:
			entites, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_varint)
			return destroy_entities(entites)
		elif _match5 == 49:
			entity, _off = _mcp.decode_varint(_raw, _off)
			effect, _off = _mcp.decode_byte(_raw, _off)
			return remove_effect(entity, effect)
		elif _match5 == 50:
			url, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			hash, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return resource_pack(url, hash)
		elif _match5 == 51:
			dimension, _off = _mcp.decode_int(_raw, _off)
			difficulty, _off = _mcp.decode_byte(_raw, _off)
			gamemode, _off = _mcp.decode_byte(_raw, _off)
			level_type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return respawn(dimension, difficulty, gamemode, level_type)
		elif _match5 == 52:
			entity, _off = _mcp.decode_varint(_raw, _off)
			head_yaw, _off = _mcp.decode_angle(_raw, _off)
			return entity_head_look(entity, head_yaw)
		elif _match5 == 53:
			_match9, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match9 == 0:
				d, _off = _mcp.decode_double(_raw, _off)
				return world_border_size(d)
			elif _match9 == 1:
				old_d, _off = _mcp.decode_double(_raw, _off)
				new_d, _off = _mcp.decode_double(_raw, _off)
				speed, _off = _mcp.decode_varlong(_raw, _off)
				return world_border_lerp(old_d, new_d, speed)
			elif _match9 == 2:
				x, _off = _mcp.decode_double(_raw, _off)
				z, _off = _mcp.decode_double(_raw, _off)
				return world_border_center(x, z)
			elif _match9 == 3:
				x, _off = _mcp.decode_double(_raw, _off)
				z, _off = _mcp.decode_double(_raw, _off)
				old_d, _off = _mcp.decode_double(_raw, _off)
				new_d, _off = _mcp.decode_double(_raw, _off)
				speed, _off = _mcp.decode_varlong(_raw, _off)
				portal_boundary, _off = _mcp.decode_varint(_raw, _off)
				warn_time, _off = _mcp.decode_varint(_raw, _off)
				warn_blocks, _off = _mcp.decode_varint(_raw, _off)
				return init_world_border(x, z, old_d, new_d, speed, portal_boundary, warn_time, warn_blocks)
			elif _match9 == 4:
				warn_time, _off = _mcp.decode_varint(_raw, _off)
				return world_border_warn_time(warn_time)
			elif _match9 == 5:
				warn_size, _off = _mcp.decode_varint(_raw, _off)
				return world_border_warn_size(warn_size)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 54:
			entity, _off = _mcp.decode_varint(_raw, _off)
			return camera(entity)
		elif _match5 == 55:
			slot, _off = _mcp.decode_byte(_raw, _off)
			return held_item_change(slot)
		elif _match5 == 56:
			position, _off = _mcp.decode_byte(_raw, _off)
			score_name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return display_scoreboard(position, score_name)
		elif _match5 == 57:
			entity, _off = _mcp.decode_varint(_raw, _off)
			metadata, _off = _mcp.decode_bytes_eof(_raw, _off)
			return entity_metadata(entity, metadata)
		elif _match5 == 58:
			attached, _off = _mcp.decode_int(_raw, _off)
			holding, _off = _mcp.decode_int(_raw, _off)
			return attach_entity(attached, holding)
		elif _match5 == 59:
			entity, _off = _mcp.decode_varint(_raw, _off)
			vx, _off = _mcp.decode_short(_raw, _off)
			vy, _off = _mcp.decode_short(_raw, _off)
			vz, _off = _mcp.decode_short(_raw, _off)
			return entity_velocity(entity, vx, vy, vz)
		elif _match5 == 60:
			entity, _off = _mcp.decode_varint(_raw, _off)
			slot, _off = _mcp.decode_varint(_raw, _off)
			item, _off = _mcp.decode_slot(_raw, _off)
			return entity_equipment(entity, slot, item)
		elif _match5 == 61:
			xp_bar, _off = _mcp.decode_float(_raw, _off)
			level, _off = _mcp.decode_varint(_raw, _off)
			total_xp, _off = _mcp.decode_varint(_raw, _off)
			return set_xp(xp_bar, level, total_xp)
		elif _match5 == 62:
			update_health, _off = _mcp.decode_float(_raw, _off)
			food, _off = _mcp.decode_varint(_raw, _off)
			sat, _off = _mcp.decode_float(_raw, _off)
			return update_health(update_health, food, sat)
		elif _match5 == 63:
			objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			_match10, _off = _mcp.decode_byte(_raw, _off)
			if false:
				pass
			elif _match10 == 0:
				value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return create_objective(value, type)
			elif _match10 == 1:
				return remove_objective()
			elif _match10 == 2:
				value, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				type, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return update_objective(value, type)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 64:
			entity, _off = _mcp.decode_varint(_raw, _off)
			passengers, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, _mcp.decode_varint)
			return set_passengers(entity, passengers)
		elif _match5 == 65:
			name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			_match11, _off = _mcp.decode_byte(_raw, _off)
			if false:
				pass
			elif _match11 == 0:
				display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				prefix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				suffix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				friendly_fire, _off = _mcp.decode_byte(_raw, _off)
				name_tag, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				collision_rule, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				color, _off = _mcp.decode_byte(_raw, _off)
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
				return create_team(display, prefix, suffix, friendly_fire, name_tag, collision_rule, color, players)
			elif _match11 == 1:
				return remove_team()
			elif _match11 == 2:
				display, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				prefix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				suffix, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				friendly_fire, _off = _mcp.decode_byte(_raw, _off)
				name_tag, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				collision_rule, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				color, _off = _mcp.decode_byte(_raw, _off)
				return update_team_info(display, prefix, suffix, friendly_fire, name_tag, collision_rule, color)
			elif _match11 == 3:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
				return team_add_players(players)
			elif _match11 == 4:
				players, _off = _mcp.decode_array(_raw, _off, _mcp.decode_varint, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
				return team_remove_players(players)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 66:
			name, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			_match12, _off = _mcp.decode_bool(_raw, _off)
			if false:
				pass
			elif _match12 == 0:
				objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				value, _off = _mcp.decode_varint(_raw, _off)
				return update_score(objective, value)
			elif _match12 == 1:
				objective, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return remove_score(objective)
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 67:
			pos, _off = _mcp.decode_position(_raw, _off)
			return compass_center(pos)
		elif _match5 == 68:
			age, _off = _mcp.decode_long(_raw, _off)
			time, _off = _mcp.decode_long(_raw, _off)
			return update_time(age, time)
		elif _match5 == 69:
			_match13, _off = _mcp.decode_varint(_raw, _off)
			if false:
				pass
			elif _match13 == 0:
				text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return set_title(text)
			elif _match13 == 1:
				text, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
				return set_subtitle(text)
			elif _match13 == 2:
				fade_in, _off = _mcp.decode_int(_raw, _off)
				stay, _off = _mcp.decode_int(_raw, _off)
				fade_out, _off = _mcp.decode_int(_raw, _off)
				return set_title_times(fade_in, stay, fade_out)
			elif _match13 == 3:
				return hide_title()
			elif _match13 == 4:
				return reset_title()
			else:
				raise _mcp.NoMatchError()
		elif _match5 == 70:
			pos, _off = _mcp.decode_position(_raw, _off)
			lines, _off = _mcp.decode_array(_raw, _off, 4, (lambda _raw, _off: _mcp.decode_string(_raw, _off, _mcp.decode_varint)))
			return update_sign(pos, lines)
		elif _match5 == 71:
			sound, _off = _mcp.decode_varint(_raw, _off)
			category, _off = _mcp.decode_varint(_raw, _off)
			x, _off = _mcp.decode_int(_raw, _off)
			y, _off = _mcp.decode_int(_raw, _off)
			z, _off = _mcp.decode_int(_raw, _off)
			volume, _off = _mcp.decode_float(_raw, _off)
			pitch, _off = _mcp.decode_byte(_raw, _off)
			return sound(sound, category, x, y, z, volume, pitch)
		elif _match5 == 72:
			header, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			footer, _off = _mcp.decode_string(_raw, _off, _mcp.decode_varint)
			return player_list_footer(header, footer)
		elif _match5 == 73:
			collected, _off = _mcp.decode_varint(_raw, _off)
			collector, _off = _mcp.decode_varint(_raw, _off)
			return collect_item(collected, collector)
		elif _match5 == 74:
			entity, _off = _mcp.decode_varint(_raw, _off)
			x, _off = _mcp.decode_double(_raw, _off)
			y, _off = _mcp.decode_double(_raw, _off)
			z, _off = _mcp.decode_double(_raw, _off)
			yaw, _off = _mcp.decode_angle(_raw, _off)
			pitch, _off = _mcp.decode_angle(_raw, _off)
			on_ground, _off = _mcp.decode_bool(_raw, _off)
			return teleport_entity(entity, x, y, z, yaw, pitch, on_ground)
		elif _match5 == 75:
			entity, _off = _mcp.decode_varint(_raw, _off)
			properties, _off = _mcp.decode_array(_raw, _off, _mcp.decode_int, entity_property.decode)
			return entity_properties(entity, properties)
		elif _match5 == 76:
			entity, _off = _mcp.decode_varint(_raw, _off)
			effect, _off = _mcp.decode_byte(_raw, _off)
			amplifier, _off = _mcp.decode_byte(_raw, _off)
			duration, _off = _mcp.decode_varint(_raw, _off)
			particles, _off = _mcp.decode_byte(_raw, _off)
			return entity_effect(entity, effect, amplifier, duration, particles)
		else:
			raise _mcp.NoMatchError()

