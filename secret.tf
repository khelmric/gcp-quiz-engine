# Create a secret for quiz engine admin-password
resource "google_secret_manager_secret" "admin-password" {
  project         = var.project_id
  secret_id = "admin-password"
  replication {
    user_managed {
      replicas {
        location = var.location
      }
    }
  }
  labels = {
    label = "quiz-engine"
  }
  depends_on = [
    google_project_service.quiz_project_services
  ]
}

# Add the secret data for quiz engine admin-password secret
resource "google_secret_manager_secret_version" "admin-password" {
  secret = google_secret_manager_secret.admin-password.id
  secret_data = var.admin_password
}
