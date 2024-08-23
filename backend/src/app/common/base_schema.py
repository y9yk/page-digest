from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class BaseResponse(BaseModel):
    code: int = 200
    message: str = "success"
    results: Optional[Union[str, List, Dict]] = None
