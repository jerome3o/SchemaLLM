from pydantic import BaseModel, Field, parse_obj_as
from typing import Optional, Any, Dict, Union, List
from enum import Enum


class SchemaType(str, Enum):
    OBJECT = "object"
    ARRAY = "array"
    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NULL = "null"


class BaseJsonSchema(BaseModel):
    title: Optional[str]
    description: Optional[str]
    default: Optional[Any]
    enum: Optional[List[Any]]
    definitions: Optional[Dict[str, "JsonSchema"]]

    class Config:
        arbitrary_types_allowed = True


class JsonSchemaRef(BaseModel):
    ref: str = Field(..., alias="$ref")


class StringJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.STRING, const=True)
    minLength: Optional[int]
    maxLength: Optional[int]
    pattern: Optional[str]


class ObjectJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.OBJECT, const=True)
    properties: Optional[Dict[str, "JsonSchema"]]
    required: Optional[List[str]]
    additionalProperties: Optional[Union[bool, "JsonSchema"]]


class ArrayJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.ARRAY, const=True)
    items: Optional[Union["JsonSchema", List["JsonSchema"]]]
    minItems: Optional[int]
    maxItems: Optional[int]
    uniqueItems: Optional[bool]


class NumberJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.NUMBER, const=True)
    minimum: Optional[float]
    maximum: Optional[float]
    exclusiveMinimum: Optional[bool]
    exclusiveMaximum: Optional[bool]
    multipleOf: Optional[float]


class IntegerJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.INTEGER, const=True)
    minimum: Optional[int]
    maximum: Optional[int]
    exclusiveMinimum: Optional[bool]
    exclusiveMaximum: Optional[bool]
    multipleOf: Optional[int]


class BooleanJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.BOOLEAN, const=True)


class NullJsonSchema(BaseJsonSchema):
    type: SchemaType = Field(SchemaType.NULL, const=True)


JsonSchema = Union[
    JsonSchemaRef,
    StringJsonSchema,
    ObjectJsonSchema,
    ArrayJsonSchema,
    NumberJsonSchema,
    IntegerJsonSchema,
    BooleanJsonSchema,
    NullJsonSchema,
]
StringJsonSchema.update_forward_refs()
ObjectJsonSchema.update_forward_refs()
ArrayJsonSchema.update_forward_refs()
NumberJsonSchema.update_forward_refs()
IntegerJsonSchema.update_forward_refs()
BooleanJsonSchema.update_forward_refs()
NullJsonSchema.update_forward_refs()
JsonSchemaRef.update_forward_refs()


def parse_json_schema(schema: Dict[str, Any]) -> JsonSchema:
    return parse_obj_as(JsonSchema, schema)


def main():
    class Details(BaseModel):
        season: str
        temperature_celsius: float

    schema = parse_obj_as(JsonSchema, Details.schema())
    print(schema)


if __name__ == "__main__":
    import logging

    logging.basicConfig(level=logging.INFO)
    main()
