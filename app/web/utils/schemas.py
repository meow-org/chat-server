# Validate params to response
email = {
  "type": "string",
  "pattern": "^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$",
  "errors": {
    "pattern": "Wrong email address"
  }
}
password = {
  "type": "string",
  "minLength": 3,
  "maxLength": 32,
  "errors": {
      "minLength": "Your password too short",
      "maxLength": "Your password too long"
  }
}
username = {"type": "string", "minLength": 2, "maxLength": 80}


def build_validators(**kwargs):
    return {
        "type": "object",
        "properties": kwargs,
        "required": list(kwargs.keys())
    }


register = build_validators(email=email, password=password, username=username)
login = build_validators(email=email, password=password)
change_pass = build_validators(email=email)
validate_new_pass = build_validators(password=password, passwordConfirmation=password, email=email)
