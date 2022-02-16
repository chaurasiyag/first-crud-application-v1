from pydantic import BaseModel, Field
class Todo(BaseModel):
	title:str =Field()
	description:str=Field()
