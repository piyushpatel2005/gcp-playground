resource "google_compute_firewall" "hivemetastore_allow_sql_access" {
  name        = "allow-cloudsqlproxy-access"
  network     = "${google_compute_network.network.self_link}"
  priority    = "800"
  direction   = "EGRESS"
  description = "Allow outbound access for cloud sql proxy to the hive metastore instance"

  allow {
    protocol = "tcp"
    ports    = ["3307"]
  }

  destination_ranges = ["${google_sql_database_instance.hive_metastore_instance.ip_address.0.ip_address}/32"]
  target_tags        = ["sql-egress"]
}

resource "google_compute_firewall" "dataproc_firewall" {
  name        = "${google_compute_network.network.name}-allow-internal"
  network     = "${google_compute_network.network.self_link}"
  description = "Firewall rule for dataproc"

  priority = "800"

  allow {
    protocol = "tcp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "udp"
    ports    = ["0-65535"]
  }

  allow {
    protocol = "icmp"
  }

  source_tags = ["${google_compute_network.network.name}-allow-internal"]
  target_tags = ["${google_compute_network.network.name}-allow-internal"]
}

resource "google_compute_firewall" "allow-ingress-from-iap" {
  name        = "${google_compute_network.network.name}-allow-ingress-from-iap"
  network     = "${google_compute_network.network.self_link}"
  description = "Firewall rule for using IAP for TCP forwarding"

  priority = "800"

  direction = "INGRESS"
  
  allow {
    protocol = "tcp"
    ports = ["22", "3389"]
  }

  source_ranges = ["35.235.240.0/20"]
}