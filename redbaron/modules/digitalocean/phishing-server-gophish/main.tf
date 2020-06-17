terraform {
  required_version = ">= 0.11.0"
}

resource "random_id" "server" {
  count       = var.counter
  byte_length = 4
}

resource "tls_private_key" "ssh" {
  count     = var.counter
  algorithm = "RSA"
  rsa_bits  = 4096
}

resource "digitalocean_ssh_key" "ssh_key" {
  count      = var.counter
  name       = "phishing-server-key-${random_id.server[count.index].hex}"
  public_key = tls_private_key.ssh[count.index].public_key_openssh
}

resource "digitalocean_droplet" "phishing-server" {
  count    = var.counter
  image    = "debian-9-x64"
  name     = "phishing-server-${random_id.server[count.index].hex}"
  region   = var.available_regions[element(var.regions, count.index)]
  ssh_keys = [digitalocean_ssh_key.ssh_key[count.index].id]
  size     = var.size

  provisioner "remote-exec" {
    inline = [
      "apt-get update",
      "apt-get install -y tmux",
    ]

    connection {
      host        = self.ipv4_address
      type        = "ssh"
      user        = "root"
      private_key = tls_private_key.ssh[count.index].private_key_pem
    }
  }

  provisioner "remote-exec" {
    scripts = concat(["../../redbaron/data/scripts/core_deps.sh"], var.install)

    connection {
      host        = self.ipv4_address
      type        = "ssh"
      user        = "root"
      private_key = tls_private_key.ssh[count.index].private_key_pem
    }
  }

  provisioner "file" {
    source      = "../../redbaron/data/scripts/gophish/gophish.service"
    destination = "/lib/systemd/system/gophish.service"
    connection {
      host        = self.ipv4_address
      type        = "ssh"
      user        = "root"
      private_key = tls_private_key.ssh[count.index].private_key_pem
    }
  }

  provisioner "file" {
    source      = "../../redbaron/data/scripts/gophish/gophish_service.sh"
    destination = "/tmp/gophish.sh"
    connection {
      host        = self.ipv4_address
      type        = "ssh"
      user        = "root"
      private_key = tls_private_key.ssh[count.index].private_key_pem
    }
  }

  provisioner "remote-exec" {
    scripts = concat(["../../redbaron/data/scripts/gophish.sh"], var.install)

    connection {
      host        = self.ipv4_address
      type        = "ssh"
      user        = "root"
      private_key = tls_private_key.ssh[count.index].private_key_pem
    }
  }

  provisioner "local-exec" {
    command = "echo \"${tls_private_key.ssh[count.index].private_key_pem}\" > ../../redbaron/data/ssh_keys/${self.ipv4_address} && echo \"${tls_private_key.ssh[count.index].public_key_openssh}\" > ../../redbaron/data/ssh_keys/${self.ipv4_address}.pub && chmod 600 ../../redbaron/data/ssh_keys/*"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "rm ../../redbaron/data/ssh_keys/${self.ipv4_address}*"
  }
}

data "template_file" "ssh_config" {
  count = var.counter

  template = file("../../redbaron/data/templates/ssh_config.tpl")

  depends_on = [digitalocean_droplet.phishing-server]

  vars = {
    name         = "phishing_server_${digitalocean_droplet.phishing-server[count.index].ipv4_address}"
    hostname     = digitalocean_droplet.phishing-server[count.index].ipv4_address
    user         = "root"
    identityfile = "${path.root}/data/ssh_keys/${digitalocean_droplet.phishing-server[count.index].ipv4_address}"
  }
}

resource "null_resource" "gen_ssh_config" {
  count = var.counter

  triggers = {
    template_rendered = data.template_file.ssh_config[count.index].rendered
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.ssh_config[count.index].rendered}' > ../../redbaron/data/ssh_configs/config_${random_id.server[count.index].hex}"
  }

  provisioner "local-exec" {
    when    = destroy
    command = "rm ../../redbaron/data/ssh_configs/config_${random_id.server[count.index].hex}"
  }
}

