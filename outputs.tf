output "namespace" {
  description = "The name of the Kubernetes namespace"
  value       = kubernetes_namespace.todo.metadata[0].name
}

output "postgres_service_name" {
  description = "PostgreSQL service name"
  value       = kubernetes_service.postgres.metadata[0].name
}

output "postgres_service_host" {
  description = "PostgreSQL service host (FQDN)"
  value       = "${kubernetes_service.postgres.metadata[0].name}.${kubernetes_namespace.todo.metadata[0].name}.svc.cluster.local"
}

output "postgres_service_port" {
  description = "PostgreSQL service port"
  value       = kubernetes_service.postgres.spec[0].port[0].port
}

output "backend_service_name" {
  description = "Backend service name"
  value       = kubernetes_service.backend.metadata[0].name
}

output "backend_service_host" {
  description = "Backend service host (FQDN)"
  value       = "${kubernetes_service.backend.metadata[0].name}.${kubernetes_namespace.todo.metadata[0].name}.svc.cluster.local"
}

output "backend_service_port" {
  description = "Backend service port"
  value       = kubernetes_service.backend.spec[0].port[0].port
}

output "frontend_service_name" {
  description = "Frontend service name"
  value       = kubernetes_service.frontend.metadata[0].name
}

output "frontend_service_port" {
  description = "Frontend service port"
  value       = kubernetes_service.frontend.spec[0].port[0].port
}

output "frontend_node_port" {
  value = kubernetes_service.frontend.spec[0].port[0].node_port
}

output "postgres_pvc_name" {
  description = "PostgreSQL persistent volume claim name"
  value       = kubernetes_persistent_volume_claim.postgres.metadata[0].name
}

output "postgres_storage_size" {
  description = "PostgreSQL storage size"
  value       = kubernetes_persistent_volume_claim.postgres.spec[0].resources[0].requests.storage
}
