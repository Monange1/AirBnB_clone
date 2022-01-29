from . import base_model
from . import user
from .engine.file_storage import FileStorage

all = [base_model.BaseModel, user.User]

storage = FileStorage()
storage.reload()
