data "google_client_openid_userinfo" "my-user" {
}

resource "google_project" "quiz_project" {
  name            = var.project_name
  project_id      = var.project_id
  billing_account = var.billing_account
  org_id          = var.org_id
}

resource "google_project_service" "quiz_project_services" {
  project = var.project_id
  for_each = toset([
    "cloudresourcemanager.googleapis.com",
    "serviceusage.googleapis.com",
    "firestore.googleapis.com",
    "firebase.googleapis.com",
    "firebasestorage.googleapis.com",
    "identitytoolkit.googleapis.com",
    "compute.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com"
  ])
  service = each.key

  timeouts {
    create = "30m"
    update = "40m"
  }
}

# Create Terraform service account
#resource "google_service_account" "quiz_tf_sa" {
#  project         = var.project_id
#  account_id      = "sa-tf-quiz-engine"
#  display_name    = "Quiz Engine Terraform Service Account"
#}

# Grant roles to Terraform service account
#resource "google_project_iam_member" "quiz_tf_sa_roles" {
#  for_each = toset([
##    "roles/firebase.admin",
#    "roles/serviceusage.serviceUsageAdmin",
#    "roles/appengine.appAdmin",
#    "roles/appengine.appCreator",
#    "roles/editor",
#    "roles/storage.admin"
#  ])
#  role = each.key
#  member = "serviceAccount:${google_service_account.quiz_tf_sa.email}"
#  project = var.project_id
#}

# Allow my-user to create a access token
#resource "google_service_account_iam_member" "grant-token-iam" {
#  service_account_id = google_service_account.quiz_tf_sa.id
#  role               = "roles/iam.serviceAccountTokenCreator"
#  member             = "user:${data.google_client_openid_userinfo.my-user.email}"
#}

# Create access token
#data "google_service_account_access_token" "default" {
#  target_service_account = google_service_account.quiz_tf_sa.email
#  scopes                 = ["userinfo-email", "cloud-platform"]
#  lifetime               = "300s"
#  depends_on = [
#    google_project_iam_member.quiz_tf_sa_roles
#  ]
#}


# Create sa-key with service account
#resource "google_service_account_key" "mykey" {
#  provider           = google-beta.gcloud-user
#  service_account_id = google_service_account.service_account.id
#  # Wait for the account being added to roles
#  depends_on = [
#    google_project_iam_member.firebase-admin-iam,
#    google_project_iam_member.service-usage-admin-iam,
#  ]
#}


