# Quiz Engine
The main purpose of this application is to provide a solution which is supporting self-development and practice exams. The content can be managed easyly according to any custom needs. The generated Quiz website can be published for a public accessibility or it can be shared within a team and restrict the access by granting permission only for specific Google-Users, -Groups or -Domains.

# Overview
The Quiz Engine was designed for Google Cloud. The solution was developed by using services on a low-cost (or even free) way, but still having the possibility to scale-up if necessary.
![Alt text](images/Diagram-Quiz-Engine.png?raw=true "Quiz Engine")

## Resources

### Terraform
All required components are deployed with Terraform scripts. The customization can be done in the `terraform.tfvars` file.

### App Engine
The Python-based application is deployed to an App Engine instance in a dedicated Google Cloud project.
The main components are:
- Python
- Flask
- HTML/CSS
- Jinja templates

### Cloud Firestore
This noSQL database is used for storing all the documents (categories, groups, questions).

### Cloud Storage
- Storage bucket ***quiz-engine-storage-app***: location for the `app.zip` file, used by the App Engine
- Storage bucket ***quiz-engine-storage-db-exports***: location for the database exports, created by the admin user

### Identity-Aware Proxy
The Identity-Aware Proxy (IAP) allows to restrict the access for specific Google-Accounts, or make the access possible for the public.

### Secret Manager
Sensitive information like the admin password is stored in Secret Manager.

## Key Features
- Quiz mode
  - Select main category
  - Select sub category
  - Select question group
  - Start Quiz (questions and answers are randomized by default)
- Edit mode
  - All Quiz mode functionalities
  - Add/Edit/Delete main category
  - Add/Edit/Delete sub category
  - Add/Edit/Delete question group
  - Add/Edit/Delete questions
  - Database Export/Import

## Database
The database is located in the Collection ***quiz_db*** in Cloud Firestore. The following document types are used inside the database:
- main-category
- sub-category
- group
- question

![Alt text](images/Database-Quiz-Engine.png?raw=true "Quiz Engine")

### Document JSON schemas
#### Main Category
```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "type": {"const": "main-category"}
    },
    "required": [
        "type",
        "name",
        "id"
    ]
}
```

#### Sub Category
```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "main_category_id": {"type": "string"},
        "type": {"const": "sub-category"}
    },
    "required": [
        "type",
        "name",
        "main_category_id",
        "id"
    ]
}
```

#### Question Group
```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string"},
        "sub_category_id": {"type": "string"},
        "type": {"const": "group"}
    },
    "required": [
        "type",
        "name",
        "sub_category_id",
        "id"
    ]
}
```

#### Question
```
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "question": {"type": "string"},
        "documentation": {"type": "string"},
        "solution_comment": {"type": "string"},
        "group_id": {"type": "string"},
        
        "type": {"const": "question"}
    },
    "required": [
        "type",
        "name",
        "sub_category_id",
        "id"
    ]
}
```

# Installation

## Prerequisites

## Customization

## Deployment
```
cd init
gcloud auth application-default login
terraform init
terraform plan
terraform apply
```