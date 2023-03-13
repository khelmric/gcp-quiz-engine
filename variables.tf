variable "org_id" {
  description = "Organization ID for the Quiz Engine project."
  type        = string
  default     = null
}

variable "project_id" {
  description = "Project ID for the Quiz Engine project."
  type        = string
  default     = null
}

variable "project_name" {
  description = "Project display name for the Quiz Engine project."
  type        = string
  default     = "Quiz Engine"
}

variable "billing_account" {
  description = "Billing Account for the Quiz Engine project."
  type        = string
  default     = null
}

variable "location" {
  description = "Location ID of the Quiz Engine resources."
  type        = string
  default     = "EU"
}

variable "bucket_suffix" {
  description = "Custom suffix for the storage bucket."
  type        = string
  default     = null
}
