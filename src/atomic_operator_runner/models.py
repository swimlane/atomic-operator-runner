"""Models to standardize output from this package."""
from datetime import datetime
from typing import Dict
from typing import List
from typing import Optional

from pydantic import BaseModel
from pydantic import Field


class BaseRecord(BaseModel):
    """Base record model used by Remote communications."""

    type: Optional[str] = Field(alias="record-type")
    message_data: Optional[str] = Field(alias="message")
    source: Optional[str]
    time_generated: Optional[datetime] = Field(alias="time-generated")
    pid: Optional[int] = Field(alias="process-id")
    native_thread_id: Optional[int] = Field(alias="native-thread-id")
    managed_thread_id: Optional[int] = Field(alias="managed-thread-id")
    extra: Optional[Dict]


class TargetEnvironment(BaseModel):
    """Environmental model."""

    platform: Optional[str]
    hostname: Optional[str]
    user: Optional[str]


class RunnerResponse(BaseModel):
    """Model representing common output data."""

    environment: Optional[TargetEnvironment]
    command: Optional[str]
    executor: Optional[str]
    elevation_required: Optional[bool]
    start_timestamp: Optional[datetime]
    end_timestamp: Optional[datetime]
    return_code: Optional[str] or Optional[int] = Field(alias="return-code")
    output: Optional[str]
    errors: Optional[str]
    records: Optional[List[BaseRecord]]
