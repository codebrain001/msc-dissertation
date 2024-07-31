# Comprehensive Data Dictionary for Emotion Surveillance Mobile Application

## Summary of Compliance Requirements
The data dictionary must comply with GDPR and CCPA regulations. Key compliance measures include:
- Data minimization: Only collect data necessary for the specified purpose.
- User consent: Obtain explicit consent from users before collecting their data.
- Data access and portability: Allow users to access their data and transfer it to another service.
- Data deletion: Provide users with the option to delete their data upon request.
- Anonymization: Anonymize personal data to protect user privacy.

## Data Attributes

### User
| Attribute Name | Data Type | Format | Validation Rules | Relationships | Compliance Attributes | Metadata |
|----------------|-----------|--------|------------------|---------------|-----------------------|----------|
| user_id        | UUID      | UUIDv4 | Required, Unique | Primary Key   | Anonymized            | Unique identifier for each user |
| email          | String    | Email  | Required, Unique |               | User consent required | User's email address |
| password       | String    |        | Required         |               | Encrypted             | User's password |
| consent        | Boolean   |        | Required         |               |                       | User's consent for data collection |

### Emotion Data
| Attribute Name | Data Type | Format | Validation Rules | Relationships | Compliance Attributes | Metadata |
|----------------|-----------|--------|------------------|---------------|-----------------------|----------|
| emotion_id     | UUID      | UUIDv4 | Required, Unique | Primary Key   | Anonymized            | Unique identifier for each emotion record |
| user_id        | UUID      | UUIDv4 | Required         | Foreign Key   |                       | Links to the user who generated the emotion data |
| timestamp      | DateTime  | ISO8601| Required         |               |                       | Timestamp of the emotion data capture |
| emotion_type   | String    |        | Required         |               |                       | Type of emotion detected (e.g., happy, sad) |
| confidence     | Float     |        | Required         |               |                       | Confidence level of the emotion detection |

### Voice Data
| Attribute Name | Data Type | Format | Validation Rules | Relationships | Compliance Attributes | Metadata |
|----------------|-----------|--------|------------------|---------------|-----------------------|----------|
| voice_id       | UUID      | UUIDv4 | Required, Unique | Primary Key   | Anonymized            | Unique identifier for each voice record |
| user_id        | UUID      | UUIDv4 | Required         | Foreign Key   |                       | Links to the user who generated the voice data |
| timestamp      | DateTime  | ISO8601| Required         |               |                       | Timestamp of the voice data capture |
| audio_file     | String    | URL    | Required         |               | Encrypted             | URL to the stored audio file |
| transcription  | String    |        |                  |               |                       | Transcription of the audio file |

### Text Data
| Attribute Name | Data Type | Format | Validation Rules | Relationships | Compliance Attributes | Metadata |
|----------------|-----------|--------|------------------|---------------|-----------------------|----------|
| text_id        | UUID      | UUIDv4 | Required, Unique | Primary Key   | Anonymized            | Unique identifier for each text record |
| user_id        | UUID      | UUIDv4 | Required         | Foreign Key   |                       | Links to the user who generated the text data |
| timestamp      | DateTime  | ISO8601| Required         |               |                       | Timestamp of the text data capture |
| text_content   | String    |        | Required         |               |                       | Content of the text message |

### Facial Expression Data
| Attribute Name | Data Type | Format | Validation Rules | Relationships | Compliance Attributes | Metadata |
|----------------|-----------|--------|------------------|---------------|-----------------------|----------|
| face_id        | UUID      | UUIDv4 | Required, Unique | Primary Key   | Anonymized            | Unique identifier for each facial expression record |
| user_id        | UUID      | UUIDv4 | Required         | Foreign Key   |                       | Links to the user who generated the facial expression data |
| timestamp      | DateTime  | ISO8601| Required         |               |                       | Timestamp of the facial expression data capture |
| image_file     | String    | URL    | Required         |               | Encrypted             | URL to the stored image file |
| expression     | String    |        | Required         |               |                       | Detected facial expression (e.g., smile, frown) |

## Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field, UUID4
from datetime import datetime
from typing import Optional

class User(BaseModel):
    user_id: UUID4
    email: EmailStr
    password: str
    consent: bool

class EmotionData(BaseModel):
    emotion_id: UUID4
    user_id: UUID4
    timestamp: datetime
    emotion_type: str
    confidence: float

class VoiceData(BaseModel):
    voice_id: UUID4
    user_id: UUID4
    timestamp: datetime
    audio_file: str
    transcription: Optional[str]

class TextData(BaseModel):
    text_id: UUID4
    user_id: UUID4
    timestamp: datetime
    text_content: str

class FacialExpressionData(BaseModel):
    face_id: UUID4
    user_id: UUID4
    timestamp: datetime
    image_file: str
    expression: str
```

This comprehensive data dictionary ensures data integrity and consistency while aligning with the project requirements and compliance measures. Each data attribute is clearly defined with its data type, format, validation rules, relationships, and compliance attributes, supported by detailed metadata.