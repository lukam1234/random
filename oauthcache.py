import time
import json

class TokenStorage:
    def __init__(self, access_token, refresh_token, expires_in, token_type = 'Bearer'):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires = expires_in + time.time()
        self.token_type = token_type

    def check_expired(self) -> bool:
        #check if token is expired
        return time.time() > self.expires

    def to_dict(self) -> dict:
        return {"access_token": self.access_token,
            "token_type": self.token_type,
            "refresh_token": self.refresh_token,
            "expires_in": int(self.expires - time.time()),  # Remaining time
            "expiry_time": self.expires
                }

    def from_dict(self, data: dict):
        self.access_token = data["access_token"]
        self.token_type = data.get("token_type", "Bearer")
        self.refresh_token = data.get("refresh_token")
        self.expires_in = time.time() + data["expires_in"]

    def save_file(self, filename = "token.json"):
        with open(filename, "w") as file:
            json.dump(self.to_dict(), file)

    @classmethod
    def load_from_file(cls, filename="token.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                return cls(
                    access_token=data["access_token"],
                    expires_in=int(data["expiry_time"] - time.time()),
                    refresh_token=data.get("refresh_token"),
                    token_type=data.get("token_type", "Bearer")
                )
        except (FileNotFoundError, KeyError):
            return None

token = OAuth2Token(access_token="aaa524", expires_in=3600, refresh_token="refresh_155")
print("token expired: ", token.is_expired())
token.save_file()
loaded_token = OAuth2Token.load_from_file()
if loaded_token:
    print("loaded token:", loaded_token.to_dict())
