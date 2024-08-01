# Comprehensive Data Dictionary for Emotion Detection Application

## Introduction
This document provides a comprehensive data dictionary for the emotion detection application, which aims to detect user emotions through voice, text, and facial expressions, and provide tailored responses and advertisements based on detected emotions. The data dictionary ensures data integrity and consistency, aligning with the project requirements and compliance measures, including GDPR compliance.

## Pydantic Models
Pydantic is a data validation and settings management library for Python, leveraging Python type annotations. It ensures that data conforms to specified types and validation rules, making it ideal for defining and validating data attributes in our application.

## Data Attributes

| Attribute Name       | Data Type   | Format          | Validation Rules                          | Relationships                  | Metadata                                      | Compliance Attributes                        |
|----------------------|-------------|-----------------|-------------------------------------------|--------------------------------|-----------------------------------------------|----------------------------------------------|
| user_id              | UUID        | uuid4           | Must be a valid UUID                      | Primary Key                    | Unique identifier for each user               | Pseudonymized data                           |
| emotion_detected     | Enum        | ['happy', 'sad', 'angry', 'neutral'] | Must be one of the predefined emotions    | Foreign Key to Emotion Table   | Detected emotion from user input              | Special category data, requires explicit consent |
| timestamp            | datetime    | ISO 8601        | Must be a valid datetime                  |                                | Time when the emotion was detected            |                                              |
| voice_data           | bytes       | base64          | Must be base64 encoded                    |                                | Raw voice data                                | Special category data, requires explicit consent |
| text_data            | str         |                 | Must be a non-empty string                |                                | Raw text data                                 | Special category data, requires explicit consent |
| facial_expression    | str         | base64          | Must be base64 encoded image              |                                | Raw facial expression data                    | Special category data, requires explicit consent |
| response_generated   | str         |                 | Must be a non-empty string                |                                | Response generated based on detected emotion  |                                              |
| advertisement_shown  | str         | URL             | Must be a valid URL                       |                                | URL of the advertisement shown                |                                              |
| consent_given        | bool        |                 | Must be True                              |                                | Indicates if user has given consent           | GDPR compliance                              |
| user_preferences     | JSON        |                 | Must be a valid JSON                      |                                | User preferences for tailored responses       |                                              |

## Compliance Requirements Summary
- **Explicit Consent**: Ensure explicit consent is obtained for processing special category data such as emotions, voice, text, and facial expressions.
- **Data Protection**: Implement robust security measures to protect user data.
- **Pseudonymization**: Use pseudonymization techniques for user identifiers to enhance privacy.
- **GDPR Compliance**: Adhere to GDPR guidelines for data processing, storage, and user rights.

## Relationships Between Attributes
- `user_id` serves as the primary key and is linked to all other attributes to uniquely identify user data.
- `emotion_detected` is linked to the Emotion Table, which contains predefined emotions.
- `consent_given` is a critical attribute ensuring that data processing complies with GDPR requirements.

## Final Review
This document has been reviewed to ensure that all data attributes are covered as per the BRD draft. The data dictionary aligns with the project requirements and compliance measures, providing a structured and comprehensive overview of the data attributes.

By following this data dictionary, we can ensure data integrity, consistency, and compliance throughout the project.

---

This comprehensive data dictionary should serve as a valuable resource for the development and management of the emotion detection application, ensuring that all data attributes are well-defined, validated, and compliant with relevant regulations.