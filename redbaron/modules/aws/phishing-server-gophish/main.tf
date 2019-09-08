terraform {
  required_version = ">= 0.11.0"
}

data "aws_region" "current" {}

resource "random_id" "server" {
  count = "${var.count}"
  byte_length = 4
}

resource "tls_private_key" "ssh" {
  count = "${var.count}"
  algorithm = "RSA"
  rsa_bits = 4096
}

resource "aws_key_pair" "gophish-server" {
  count = "${var.count}"
  key_name = "gophish-server-key-${random_id.server.*.hex[count.index]}"
  public_key = "${tls_private_key.ssh.*.public_key_openssh[count.index]}"
}

resource "aws_instance" "gophish-server" {
  // Currently, variables in provider fields are not supported :(
  // This severely limits our ability to spin up instances in diffrent regions
  // https://github.com/hashicorp/terraform/issues/11578

  //provider = "aws.${element(var.regions, count.index)}"

  count = "${var.count}"

  tags = {
    Name = "gophish-server-${random_id.server.*.hex[count.index]}"
  }

  ami = "${var.amis[data.aws_region.current.name]}"
  instance_type = "${var.instance_type}"
  key_name = "${aws_key_pair.gophish-server.*.key_name[count.index]}"
  vpc_security_group_ids = ["${aws_security_group.gophish-server.id}"]
  subnet_id = "${var.subnet_id}"
  associate_public_ip_address = true

  provisioner "local-exec" {
    command = "echo \"${tls_private_key.ssh.*.private_key_pem[count.index]}\" > ../../redbaron/data/ssh_keys/${self.public_ip} && echo \"${tls_private_key.ssh.*.public_key_openssh[count.index]}\" > ../../redbaron/data/ssh_keys/${self.public_ip}.pub && chmod 600 ../../redbaron/data/ssh_keys/*"
  }

  provisioner "local-exec" {
    when = "destroy"
    command = "rm ../../redbaron/data/ssh_keys/${self.public_ip}*"
  }

  provisioner "remote-exec" {
    inline = [
      "sudo apt-get update",
      "sudo apt-get install -y tmux apache2 certbot mosh",
    ]

    connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }


  provisioner "remote-exec" {
    scripts = "${concat(list("../../redbaron/data/scripts/core_deps.sh"), var.install)}"

    connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }

  provisioner "file" {
    source      = "../../redbaron/data/scripts/gophish/gophish.service"
    destination = "/tmp/gophish.service"
        connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo mv /tmp/gophish.service /lib/systemd/system/gophish.service"
    ]

    connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }

  provisioner "file" {
    source      = "../../redbaron/data/scripts/gophish.sh"
    destination = "/tmp/gophish.sh"
        connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }

  provisioner "remote-exec" {
    inline = [
      "sudo chmod 777 /tmp/gophish.sh",
      "sudo /tmp/gophish.sh",
    ]

  # "sudo /opt/goapps/src/github.com/gophish/gophish/gophish &"
    connection {
        type = "ssh"
        user = "admin"
        private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
    }
  }


  # provisioner "remote-exec" {
  #   scripts = "${concat(list("../../redbaron/data/scripts/gophish.sh"), var.install)}"
  #
  #   connection {
  #       type = "ssh"
  #       user = "admin"
  #       private_key = "${tls_private_key.ssh.*.private_key_pem[count.index]}"
  #   }
  # }

}

resource "null_resource" "ansible_provisioner" {
  count = "${signum(length(var.ansible_playbook)) == 1 ? var.count : 0}"

  depends_on = ["aws_instance.gophish-server"]

  triggers {
    droplet_creation = "${join("," , aws_instance.gophish-server.*.id)}"
    policy_sha1 = "${sha1(file(var.ansible_playbook))}"
  }

  provisioner "local-exec" {
    command = "ansible-playbook ${join(" ", compact(var.ansible_arguments))} --user=admin --private-key=../../redbaron/data/ssh_keys/${aws_instance.gophish-server.*.public_ip[count.index]} -e host=${aws_instance.gophish-server.*.public_ip[count.index]} ${var.ansible_playbook}"

    environment {
      ANSIBLE_HOST_KEY_CHECKING = "False"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

data "template_file" "ssh_config" {

  count    = "${var.count}"

  template = "${file("../../redbaron/data/templates/ssh_config.tpl")}"

  depends_on = ["aws_instance.gophish-server"]

  vars {
    name = "dns_rdir_${aws_instance.gophish-server.*.public_ip[count.index]}"
    hostname = "${aws_instance.gophish-server.*.public_ip[count.index]}"
    user = "admin"
    identityfile = "${path.root}/data/ssh_keys/${aws_instance.gophish-server.*.public_ip[count.index]}"
  }

}

resource "null_resource" "gen_ssh_config" {

  count = "${var.count}"

  triggers {
    template_rendered = "${data.template_file.ssh_config.*.rendered[count.index]}"
  }

  provisioner "local-exec" {
    command = "echo '${data.template_file.ssh_config.*.rendered[count.index]}' > ../../redbaron/data/ssh_configs/config_${random_id.server.*.hex[count.index]}"
  }

  provisioner "local-exec" {
    when = "destroy"
    command = "rm ../../redbaron/data/ssh_configs/config_${random_id.server.*.hex[count.index]}"
  }

}
