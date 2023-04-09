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

variable "suffix" {
  description = "Custom suffix for unique IDs."
  type        = string
  default     = null
}

variable "admin_password" {
  description = "Admin password to enable edit functions."
  type        = string
  default     = "quizEngine123!"
  sensitive   = true
}

variable "access_list" {
  description = "List of accounts to get access on the website."
  type        = list(string)
  default     = [ "allUsers" ]
}
