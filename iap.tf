resource "google_iap_brand" "quiz_engine_brand" {
  project           = var.project_id
  support_email     = var.support_email
  application_title = "Quiz Engine"
}

resource "google_iap_client" "quiz_engine_client" {
  display_name = "Quiz Engine"
  brand        =  google_iap_brand.quiz_engine_brand.name
}

resource "google_iap_web_type_app_engine_iam_binding" "binding" {
  project = var.project_id
  app_id = google_app_engine_application.quiz_app.app_id
  role = "roles/iap.httpsResourceAccessor"
  members = var.access_list
}
