# Emotion Surveillance Mobile Application Data Dictionary

| Attribute | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|-----------|-------------|-----------|--------|------------------|---------------|------------------------|
| User | Represents an individual user of the application | Pydantic BaseModel | ```python
class User(BaseModel):
    user_id: UUID
    username: str
    email: EmailStr
    date_of_birth: date
    registration_date: datetime
    last_login: datetime
``` | - `user_id`: Must be a valid UUID
- `username`: 3-50 characters, alphanumeric and underscores only
- `email`: Must be a valid email format
- `date_of_birth`: Must be a valid date, user must be at least 13 years old
- `registration_date`: Cannot be in the future
- `last_login`: Cannot be earlier than registration_date | One-to-many with EmotionData, PrivacySetting, and ComplianceLog | - Pseudonymization: user_id
- Data minimization: Only essential user information collected |
| EmotionData | Stores emotion recognition data for a user | Pydantic BaseModel | ```python
class EmotionData(BaseModel):
    emotion_id: UUID
    user_id: UUID
    timestamp: datetime
    emotion: str
    confidence: float
    facial_features: Dict[str, float]
``` | - `emotion_id`: Must be a valid UUID
- `user_id`: Must be a valid UUID, existing in User table
- `timestamp`: Cannot be in the future
- `emotion`: Must be one of predefined emotion categories
- `confidence`: Float between 0 and 1
- `facial_features`: Dict of predefined facial landmarks | Many-to-one with User | - Special category data: Biometric data
- Purpose limitation: Only for emotion recognition
- Storage limitation: Subject to DataRetentionPolicy |
| PrivacySetting | Stores user's privacy preferences | Pydantic BaseModel | ```python
class PrivacySetting(BaseModel):
    setting_id: UUID
    user_id: UUID
    data_sharing: bool
    anonymized_analytics: bool
    retention_period: int  # in days
    last_updated: datetime
``` | - `setting_id`: Must be a valid UUID
- `user_id`: Must be a valid UUID, existing in User table
- `data_sharing`: Boolean
- `anonymized_analytics`: Boolean
- `retention_period`: Integer, 1-365 days
- `last_updated`: Cannot be in the future | Many-to-one with User | - User consent: Explicit settings for data processing
- Right to be forgotten: Retention period setting |
| ComplianceLog | Logs compliance-related actions | Pydantic BaseModel | ```python
class ComplianceLog(BaseModel):
    log_id: UUID
    user_id: UUID
    action_type: str
    action_details: str
    timestamp: datetime
    performed_by: str
``` | - `log_id`: Must be a valid UUID
- `user_id`: Must be a valid UUID, existing in User table
- `action_type`: Must be one of predefined compliance actions
- `timestamp`: Cannot be in the future
- `performed_by`: Must be a valid system user or "SYSTEM" | Many-to-one with User | - Accountability: Logging of all compliance-related actions
- Transparency: Provides audit trail for data processing activities |
| EmotionAlert | Represents alerts generated based on emotion data | Pydantic BaseModel | ```python
class EmotionAlert(BaseModel):
    alert_id: UUID
    user_id: UUID
    emotion_id: UUID
    alert_type: str
    alert_message: str
    timestamp: datetime
    is_acknowledged: bool
``` | - `alert_id`: Must be a valid UUID
- `user_