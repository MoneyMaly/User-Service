from datetime import date, datetime
from enum import Enum
from bson import ObjectId

class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid objectid')
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')


    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        
def to_jsonable_dict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = to_jsonable_dict(v, classkey)
        return data
    if isinstance(obj, Enum):
        return str(obj).split('.')[-1]
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    elif hasattr(obj, '_ast'):
        return to_jsonable_dict(obj._ast())
    elif hasattr(obj, '__iter__') and not isinstance(obj, str):
        return [to_jsonable_dict(v, classkey) for v in obj]
    elif hasattr(obj, '__dict__'):
        data = dict([(key, to_jsonable_dict(value, classkey))
                     for key, value in obj.__dict__.items()
                     if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, '__class__'):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj