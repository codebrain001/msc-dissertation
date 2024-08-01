# EDR Mobile Application Data Dictionary

| Attribute Name | Description | Data Type | Maximum Length | Minimum Length | Allowed Values | Nullable | Default Value | Constraints | Related To |
|----------------|-------------|-----------|----------------|----------------|----------------|----------|---------------|-------------|------------|
| User ID | Unique identifier for each user | UUID | 36 | 36 | N/A | No | N/A | Primary Key | Username, Email Address |
| Username | User's chosen display name | String | 50 | 3 | Alphanumeric characters, underscores, hyphens | No | N/A | Unique | User ID |
| Email Address | User's email address for account management | String | 255 | 5 | Valid email format | No | N/A | Unique | User ID |
| Password Hash | Securely stored hash of user's password | String | 128 | 128 | N/A | No | N/A | N/A | User ID |
| Date of Birth | User's date of birth for age verification | Date | N/A | N/A | Valid date | Yes | NULL | Must be at least 13 years ago | User ID |
| Last Login Timestamp | Date and time of user's last login | DateTime | N/A | N/A | Valid timestamp | Yes | NULL | Cannot be in the future | User ID |
| Device ID | Unique identifier for user's device | String | 64 | 16 | Alphanumeric | No | N/A | N/A | User ID |
| Location Data | User's current or last known location | JSON | N/A | N/A | Valid GeoJSON | Yes | NULL | N/A | User ID |
| Consent Flag | Indicates user's consent for data processing | Boolean | N/A | N/A | True/False | No | False | N/A | User ID |
| Data Retention Period | Number of days to retain user data | Integer | N/A | N/A | 1-3650 | No | 365 | N/A | User ID |
| Encryption Key ID | Identifier for the encryption key used | String | 32 | 32 | Alphanumeric | No | N/A | N/A | User ID |
| User Preferences | JSON object storing user preferences | JSON | 4096 | 2 | Valid JSON | Yes | {} | N/A | User ID |
| Account Status | Current status of the user account | Enum | N/A | N/A | Active, Suspended, Deactivated | No | Active | N/A | User ID |
| Last Updated Timestamp | Date and time of last profile update | DateTime | N/A | N/A | Valid timestamp | No | Current timestamp | Cannot be in the future | User ID |
| Emotion Data | Detected emotion from user input | JSON | 1024 | 2 | Valid JSON | Yes | NULL | N/A | User ID, Device ID |
| Input Type | Type of input used for emotion detection | Enum | N/A | N/A | Voice, Text, Facial | No | N/A | N/A | Emotion Data |
| Confidence Score | Confidence level of emotion detection | Float | N/A | N/A | 0.0 - 1.0 | No | 0.0 | N/A | Emotion Data |
| Session ID | Unique identifier for each user session | UUID | 36 | 36 | N/A | No | N/A | N/A | User ID, Device ID |
| App Version | Version of the EDR mobile app | String | 10 | 1 | Semantic versioning format | No | 1.0.0 | N/A | Device ID |
| Language Preference | User's preferred language for the app | String | 5 | 2 | ISO 639-1 codes | No | en | N/A | User Preferences |