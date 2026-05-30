resource "kubernetes_namespace" "todo" {
  metadata {
    name = "todo"
  }
}
