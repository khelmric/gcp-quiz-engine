#resource "google_firestore_database" "quiz-db" {
#  provider                    = google-beta
#  project                     = var.project_id
#  name                        = "quiz-db"
#  location_id                 = "${var.location}"
#  type                        = "FIRESTORE_NATIVE"
#  concurrency_mode            = "OPTIMISTIC"
#  app_engine_integration_mode = "ENABLED"
#
#  depends_on = [
#    google_project_service.quiz_project_services,
#    google_project_iam_member.quiz_tf_sa_roles
#  ]
#}
