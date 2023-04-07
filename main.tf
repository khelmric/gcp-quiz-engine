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
    "compute.googleapis.com",
    "containerregistry.googleapis.com",
    "run.googleapis.com",
    "cloudbuild.googleapis.com",
    "artifactregistry.googleapis.com",
    "appengine.googleapis.com",
    "orgpolicy.googleapis.com",
    "secretmanager.googleapis.com"
  ])
  service = each.key

  timeouts {
    create = "30m"
    update = "40m"
  }
}

resource "google_project_organization_policy" "org_policy_resource_location" {
  project   = var.project_id
  constraint = "gcp.resourceLocations"

  list_policy {
    allow {
      all = true
    }
  }

}

