resource "null_resource" "ansible_provisioner" {
  triggers = {
    policy_sha1 = filesha1(var.playbook)
  }

  provisioner "local-exec" {
    command = "ansible-playbook --private-key=../../redbaron/data/ssh_keys/${var.ip} --user ${var.user} -i ${var.ip}, ${var.playbook} -e ansible_python_interpreter=/usr/bin/python3"

    environment = {
      ANSIBLE_HOST_KEY_CHECKING = "False"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

