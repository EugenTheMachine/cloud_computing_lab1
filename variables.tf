variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  sensitive   = true
}

variable "replicas" {
  description = "Number of replicas for deployments"
  type        = number
  default     = 1
}

variable "backend_replicas" {
  description = "Number of replicas for backend deployment"
  type        = number
  default     = 1
}
