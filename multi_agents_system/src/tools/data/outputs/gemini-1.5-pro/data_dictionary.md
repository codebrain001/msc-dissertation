# EDR System Data Dictionary

This document outlines the data attributes for the Emotion Detection and Recognition (EDR) system, structured using the Pydantic model. Each attribute is defined with its metadata, data type and format, validation rules, relationships to other data elements, and compliance considerations.

## Table of Contents

- [I. Core Emotion Data](#i-core-emotion-data)
- [II. Patient Session Data](#ii-patient-session-data)
- [III. Data Source Information](#iii-data-source-information)
- [IV. System and User Data](#iv-system-and-user-data)
- [V. Anonymization and Privacy](#v-anonymization-and-privacy)

## I. Core Emotion Data

| Attribute Name | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|---|---|---|---|---|---|---|
| `emotion_timestamp` | Records the precise time at which an emotion is detected. | Datetime | ISO 8601 (e.g., "2023-12-19T12:45:55.123456") | - Must be a valid datetime value. - Should be within a reasonable timeframe relative to the system clock. | - Linked to the specific `session_id`. - Potentially linked to external events (e.g., therapist interventions) if time-stamped data is available. | - Data should be anonymized or de-identified when used for secondary purposes (e.g., research) to comply with HIPAA. |
| `detected_emotion` | Represents the emotion recognized by the system at a given timestamp. | String (Enum) |  | - Must match one of the predefined emotion categories supported by the system (e.g., "Joy," "Sadness," "Anger," "Fear," "Surprise," "Neutral," "Ambiguous"). - Consider allowing for multiple emotions with associated confidence scores to represent blended emotional states. | - Directly linked to `emotion_timestamp` and `confidence_score`. | - The emotion categories used should be carefully chosen to avoid biased or discriminatory interpretations. |
| `confidence_score` | Indicates the system's confidence level in the accuracy of the detected emotion. | Float |  | - Must be a numerical value between 0.0 and 1.0 (representing 0% to 100% confidence). | - Directly associated with the `detected_emotion` at a specific `emotion_timestamp`. | - Transparency about the confidence score is essential, especially when used in clinical decision-making. |

## II. Patient Session Data

| Attribute Name | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|---|---|---|---|---|---|---|
| `session_id` | A unique identifier for each patient session. | UUID |  | - Must be a valid UUID format. | - One-to-many relationship with Core Emotion Data—one session can have multiple emotion data points. | - The `session_id` should not be derived from any personally identifiable information (PII). |
| `patient_id` | A unique identifier for each patient. | String or Integer | Depends on EHR system | - Must match the format used by the integrated EHR system. - Should be validated against the EHR system to ensure the patient ID exists. | - Foreign key referencing the Patient table in the EHR system. | - This attribute is considered PII and requires the highest level of protection. - Access to `patient_id` should be strictly controlled and limited to authorized personnel. |
| `session_start_time` | Records the start time of the patient session. | Datetime | ISO 8601 | - Must be a valid datetime value. | - Linked to `session_end_time` to determine session duration. | - Data should be handled according to the minimum necessary principle, only retaining the information needed for the intended purpose. |
| `session_end_time` | Records the end time of the patient session. | Datetime | ISO 8601 | - Must be a valid datetime value. - Should be chronologically after the `session_start_time`. | - Linked to `session_start_time` to determine session duration. |  |

## III. Data Source Information

| Attribute Name | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|---|---|---|---|---|---|---|
| `data_source` | Identifies the source of the emotional data. | String (Enum) |  | - Must match one of the predefined data sources (e.g., "Facial Expression Analysis," "Speech Analysis," "Heart Rate Variability," "Skin Conductance"). | - Can be linked to specific Emotion Data points to indicate the source of each emotion detection. | - If data from multiple sources is combined, the origin of each data point should be clearly documented. |

## IV. System and User Data

| Attribute Name | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|---|---|---|---|---|---|---|
| `user_id` | Identifies the healthcare professional using the EDR system. | String or Integer | Depends on system authentication | - Should be validated against the system's user database. | - Foreign key referencing the User table in the EDR system's database. | - Access to the system should be logged and monitored to ensure accountability and prevent unauthorized access. |
| `alert_thresholds` | User-defined thresholds for specific emotions or emotional intensity levels that, when exceeded, trigger alerts for the healthcare professional. | JSON |  | - Ensure the JSON structure is valid. - Validate that emotion keys match the system's predefined categories. - Threshold values should fall within acceptable ranges. | - Associated with the `user_id`, allowing for personalized alert settings. | - Default alert thresholds should be set conservatively to minimize potential harm. - Users should be informed about the implications of adjusting alert thresholds. |

## V. Anonymization and Privacy

| Attribute Name | Description | Data Type | Format | Validation Rules | Relationships | Compliance Attributes |
|---|---|---|---|---|---|---|
| `anonymization_status` | Indicates whether the data has been anonymized and is suitable for secondary use (e.g., research). | Boolean |  | - Should be set to True only after all necessary anonymization procedures have been applied. | - Can be a global flag for the entire dataset or applied at the individual data point level. | - All data used for secondary purposes must be appropriately anonymized or de-identified to comply with HIPAA and other relevant regulations. |
| `anonymization_method` | Records the specific anonymization techniques applied to the data. | String (Enum or free text allowing for multiple methods) |  | - If using an Enum, ensure values match predefined anonymization methods (e.g., "Pseudonymization," "Aggregation," "Differential Privacy"). | - Linked to the `anonymization_status`, providing details about the applied methods. | - The chosen anonymization methods should be robust and aligned with best practices for protecting sensitive health information. |

## Pydantic Model Considerations

- **Data Validation:** Utilize Pydantic's validation features (type annotations, custom validators, regex patterns) to enforce data integrity and consistency.
- **Data Serialization:** Define how data is serialized (e.g., to JSON) for storage, retrieval, and API communication.
- **Documentation:** Provide clear and concise documentation for each attribute within the Pydantic model using docstrings. This documentation is crucial for developers and data scientists working with the EDR system's data.

This data dictionary, structured with the Pydantic model, ensures data integrity, facilitates analysis, and upholds patient privacy within the EDR system.