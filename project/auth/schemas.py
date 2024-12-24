from pydantic import BaseModel, EmailStr, Field

class SUserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=5)

class SUserRegister(SUserAuth):
    username: str = Field(min_length=3)
    confirm_password: str

    def validate_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords don't match")
