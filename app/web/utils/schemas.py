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
    "email": {"type": "string", "format": "email"},
    "password": {"type": "string", "minLength": 8, "maxLength": 32}
  },
  "required": ["email", "password"]
}

change_pass = {
  "type": "object",
  "properties": {
    "email": {"type": "string", "format": "email"},
  },
  "required": ["email"]
}
