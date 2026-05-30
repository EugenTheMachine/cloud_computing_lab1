resource "kubernetes_deployment" "backend" {
  metadata {
    name      = "backend"
    namespace = kubernetes_namespace.todo.metadata[0].name
  }
  spec {
    replicas = var.backend_replicas
    selector {
      match_labels = {
        app = "backend"
      }
    }
    template {
      metadata {
        labels = {
          app = "backend"
        }
      }
      spec {
        container {
          image             = "todo-backend"
          image_pull_policy = "Never"
          name              = "backend"
          port {
            container_port = 8000
          }
          env {
            name  = "POSTGRES_HOST"
            value = kubernetes_service.postgres.metadata[0].name
          }
          env {
            name  = "POSTGRES_PORT"
            value = "5432"
          }
          env {
            name  = "POSTGRES_DB"
            value = "todo_db"
          }
          env {
            name  = "POSTGRES_USER"
            value = "todo_user"
          }
          env {
            name  = "POSTGRES_PASSWORD"
            value = var.postgres_password
          }
          resources {
            requests = {
              cpu    = "100m"
              memory = "128Mi"
            }
            limits = {
              cpu    = "500m"
              memory = "256Mi"
            }
          }
        }
      }
    }
  }
  depends_on = [kubernetes_service.postgres]
}

resource "kubernetes_service" "backend" {
  metadata {
    name      = "backend"
    namespace = kubernetes_namespace.todo.metadata[0].name
  }
  spec {
    selector = {
      app = "backend"
    }
    port {
      port        = 8000
      target_port = 8000
    }
    type = "ClusterIP"
  }
  depends_on = [kubernetes_deployment.backend]
}
