# Quiz Engine
The main purpose of this application is to provide a solution which is supporting self-development and practice exams. The content can be managed easyly according to any custom needs. Also it can be shared within a team and restrict the access by granting permission only for specific Google-Users, -Groups or -Domains.

# Overview
The Quiz Engine was designed for Google Cloud. The solution was developed by using services on a low-cost (or even free) way, but still having the possibility to scale-up if necessary.
![Alt text](Diagram-Quiz-Engine.png?raw=true "Quiz Engine")

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

### Identity-Aware Proxy

### Secret Manager

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

### Document schemas

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