from pydantic import BaseModel


class TokenResponse(BaseModel):

    access_token: str

    token_type: str = "bearer" 
"""
"bearer" is the default fallback value assigned if no other value is provided for the token_type 
field. This is a common convention in OAuth2 and JWT-based authentication systems, where the token 
type is typically specified as "bearer" to indicate that the token is a bearer token.

"""