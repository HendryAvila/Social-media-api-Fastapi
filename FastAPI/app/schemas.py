from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Literal


#---------------------------------------------------------------------------------
  
class ResponseUser(BaseModel):
    email: str
    created_at: datetime
    id: int
    class Config:
        from_attributes = True    
class UserCreated_and_Updated(BaseModel):
    email: EmailStr
    password: str
    
    
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: Optional[str] = None      
class PostBase(BaseModel):
    '''SCHEMA:
In the context of an API, a schema refers to a formal definition of the structure
and data types of the input and output data that the API expects or returns.
It helps ensure that the data being sent or received is valid and adheres to a specific format.

Pydantic is a Python library that provides runtime validation and parsing of data structures,
commonly used for data validation and serialization/deserialization in API development.
BaseModel is a class provided by Pydantic that allows you to define a schema for your data by specifying
the fields and their types. It also provides additional features like data validation, default values, and more.'''
    title: str
    content: str
    published: bool = True
    
class PostCreate(PostBase):
    pass    

class ResponsePost(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner : ResponseUser
    class Config:
        from_attributes = True
        

class Vote(BaseModel):
    posts_id: int
    dir: Literal[0, 1]    