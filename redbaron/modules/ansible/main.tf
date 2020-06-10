terraform {
  required_version = ">= 0.11.0"
}

resource "null_resource" "ansible_provisioner" {

  triggers {
    policy_sha1 = "${sha1(file(var.playbook))}"
  }

  provisioner "local-exec" {
    command = "ansible-playbook --private-key=../../redbaron/data/ssh_keys/${var.ip} --user ${var.user} -i ${var.ip}, ${var.playbook}"

    environment {
      ANSIBLE_HOST_KEY_CHECKING = "False"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}