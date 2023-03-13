#  depends_on = [
#    google_project_service.quiz_project_services,
#    google_project_iam_member.quiz_tf_sa_roles
#  ]
#

# Create a Cloud Storage bucket for the PHP code
resource "google_storage_bucket" "quiz_storage_app" {
  project         = var.project_id
  name          = "quiz-engine-storage-app-${var.bucket_suffix}"
  storage_class = "REGIONAL"
  location      = var.location

#  depends_on = [
#    google_project_service.quiz_project_services
#  ]
}

resource "google_storage_bucket" "quiz_storage_images" {
  project         = var.project_id
  name            = "quiz-engine-storage-images-${var.bucket_suffix}"
  storage_class   = "REGIONAL"
  location        = var.location

#  depends_on = [
#    google_project_service.quiz_project_services
#  ]
}
