#!/usr/bin/env python3
"""
Models per AetherAPIService - Creato autonomamente il 2025-07-20T05:30:38.484643
"""

from pydantic import BaseModel
from typing import Optional, List
import datetime

class BaseItem(BaseModel):
    name: str
    description: Optional[str] = None
    
class Item(BaseItem):
    id: int
    value: float
    created_at: datetime.datetime
    updated_at: Optional[datetime.datetime] = None
    
class ItemCreate(BaseItem):
    value: float
    
class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    value: Optional[float] = None
    
class ApiResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None
    timestamp: datetime.datetime = datetime.datetime.now()
