# Comprehensive Data Dictionary for Emotion Detection Application

| Attribute Name | Description | Data Type | Maximum Length | Minimum Length | Allowed Values | Nullable | Default Value | Constraints | Related To |
|----------------|-------------|-----------|----------------|----------------|----------------|----------|---------------|-------------|------------|
| user_id | Unique identifier for a user | string | 36 | 36 | UUID format | false | null | Must be unique, pseudonymized or encrypted | consent_status, emotional_state |
| consent_status | Indicates if user has given consent for data processing | boolean | n/a | n/a | true, false | false | false | Must be true for data processing | user_id |
| consent_timestamp | Date and time when consent was given | datetime | n/a | n/a | ISO 8601 format | false | null | Must be earlier than or equal to current timestamp | consent_status |
| consent_version | Version of the privacy policy agreed to | string | 10 | 1 | Semantic versioning format | false | null | Must be a valid version number | consent_status |
| consent_withdrawal_status | Indicates if user has withdrawn consent | boolean | n/a | n/a | true, false | false | false | If true, data processing must stop | consent_status |
| consent_withdrawal_timestamp | Date and time when consent was withdrawn | datetime | n/a | n/a | ISO 8601 format | true | null | Must be later than consent_timestamp if present | consent_withdrawal_status |
| voice_data | Audio file containing user's voice input | binary | 10MB | 1KB | WAV, MP3 format | true | null | File size must be within specified range | emotional_state |
| voice_duration | Duration of the voice input | float | n/a | n/a | Positive numbers | false | 0.0 | Must be greater than 0 | voice_data |
| voice_sampling_rate | Sampling rate of the voice input | integer | n/a | n/a | 8000, 16000, 44100, 48000 | false | 16000 | Must be one of the allowed values | voice_data |
| text_data | User's text input for analysis | string | 1000 | 1 | UTF-8 encoded text | true | null | Must not contain personally identifiable information | emotional_state |
| text_language | Language of the text input | string | 2 | 2 | ISO 639-1 language codes | false | "en" | Must be a valid language code | text_data |
| facial_expression_data | Image data of user's facial expression | binary | 5MB | 10KB | JPEG, PNG format | true | null | File size must be within specified range | emotional_state |
| facial_expression_resolution | Resolution of the facial expression image | string | 20 | 7 | Format: WIDTHxHEIGHT (e.g., "1280x720") | false | "640x480" | Must match the format WIDTHxHEIGHT | facial_expression_data |
| emotional_state | Detected emotional state of the user | string | 20 | 3 | happy, sad, angry, neutral, etc. | false | "neutral" | Must be one of the predefined emotional states | user_id, voice_data, text_data, facial_expression_data |
| emotional_state_confidence | Confidence level of the detected emotional state | float | n/a | n/a | 0.0 to 1.0 | false | 0.0 | Must be between 0.0 and 1.0 | emotional_state |
| processing_purpose | Purpose for processing the user's data | string | 100 | 5 | emotion_detection, targeted_advertising, etc. | false | "emotion_detection" | Must be one of the predefined purposes | user_id |
| legal_basis | Legal basis for processing the data | string | 50 | 5 | consent, legitimate_interest, etc. | false | "consent