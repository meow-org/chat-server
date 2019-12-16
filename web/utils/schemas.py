register = {
  "type": "object",
  "properties": {
    "username": {"type": "string", "minLength": 2, "maxLength": 100},
    "email": {"type": "string", "format": "email"},
    "password": {"type": "string", "minLength": 8, "maxLength": 32}
  },
  "required": ["username", "email", "password"]
}

login = {
  "type": "object",
  "properties": {
    "username": {"type": "string", "minLength": 2, "maxLength": 100},
    "password": {"type": "string", "minLength": 8, "maxLength": 32}
  },
  "required": ["username", "password"]
}
