# output the bucket name created for backend resource `default`
output "storage-bucket-name" {
    value = google_storage_bucket.default.name
}

output "flask-vm-external-ip" {
    value = google_compute_instance.webserver.network_interface.0.access_config.0.nat_ip
    sensitive = true
}

output "flask-vm-cpu_platform" {
    value = google_compute_instance.webserver.cpu_platform
}

output "database-vm-external-ip" {
    value = google_compute_instance.dbserver.network_interface.0.access_config.0.nat_ip
}

output "external-reserved-ip" {
    value = google_compute_address.external_with_subnet_and_address.address
}