resource "google_service_account" "quiz-app-sa" {
  project                     = var.project_id
  account_id   = "quiz-app-account"
  display_name = "Quiz App Service Account"
}


resource "google_project_iam_member" "quiz_app_sa_roles" {
  for_each = toset([
    "roles/storage.objectViewer",
    "roles/compute.networkUser",
    "roles/appengine.appAdmin",
    "roles/appengine.appCreator",
    "roles/datastore.owner"
  ])
  role = each.key
  project = google_service_account.quiz-app-sa.project
  member  = "serviceAccount:${google_service_account.quiz-app-sa.email}"
}

data "archive_file" "app-engine-source-zip" {
 type        = "zip"
 source_dir  = "./app"
 output_path = "./app.zip"
}

# Upload the app.zip to the bucket
resource "google_storage_bucket_object" "upload-app" {
  name   = "app.zip"
  bucket = google_storage_bucket.quiz_storage_app.name
  source = "app.zip"
  content_type = "application/zip"

  depends_on = [
    google_storage_bucket.quiz_storage_app,
    data.archive_file.app-engine-source-zip
  ]
}

# Create an App Engine application
resource "google_app_engine_application" "quiz_app" {
  project  = var.project_id
  location_id = var.location
  database_type = "CLOUD_FIRESTORE"
}

# Create a Python App Engine service
resource "google_app_engine_standard_app_version" "quiz_app_v1" {
  project         = var.project_id
  version_id      = "v1"
  service         = "default"
  runtime         = "python39"
  instance_class      = "F4_1G"
  entrypoint {
    shell = "python3 ./main.py"
  }
  deployment {
    zip {
      source_url = "https://storage.googleapis.com/${google_storage_bucket.quiz_storage_app.name}/app.zip"
    }
  }
  env_variables = {
    GOOGLE_CLOUD_PROJECT = "${var.project_id}"
  }
  automatic_scaling {
    standard_scheduler_settings {
      max_instances = 2
    }
  }

  delete_service_on_destroy = true
  service_account = google_service_account.quiz-app-sa.email

  depends_on = [
    google_storage_bucket_object.upload-app
  ]
}



