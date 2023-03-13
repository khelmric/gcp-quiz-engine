terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.56"
    }
    google-beta = {
      source  = "hashicorp/google-beta"
      version = "~> 4.56"
    }
    null = {
      version = "~> 3.2.1"
    }
    time = {
      source  = "hashicorp/time"
      version = "0.9.1"
    }
  }
}

