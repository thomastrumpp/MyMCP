variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "mymcp-antigravity-prod"
}

variable "region" {
  description = "The GCP region"
  type        = string
  default     = "europe-west1"
}

variable "repo_name" {
  description = "Artifact Registry repository name"
  type        = string
  default     = "cloud-run-source-deploy"
}

variable "github_repo" {
  description = "The GitHub repository (Owner/Repo)"
  type        = string
  default     = "thomastrumpp/MyMCP"
}
