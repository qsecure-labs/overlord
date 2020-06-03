# Overlord – Red Teaming Automation
<p align="center">
  <img src="logo.png" width=30%>
</p>

Overlord provides a python-based console CLI which is used to build Red Teaming infrastructure in an automated way. The user has to provide inputs by using the tool’s modules (e.g. C2, Email Server, HTTP web delivery server, Phishing server etc.) and the full infra / modules and scripts will be generated automatically on a cloud provider of choice. Currently supports AWS and Digital Ocean. The tool is still under development and it was inspired and uses the [Red-Baron](https://github.com/byt3bl33d3r/Red-Baron) Terraform implementation found on Github. 

A demo infrastructure was set up in our blog post https://blog.qsecure.com.cy/posts/overlord/ .

# Installation

```bash
git clone overlord /opt/overlord
cd /opt/overlord/config
./install.sh
```

## Disclaimer
Overlord comes without warranty and is meant to be used by penetration testers during approved red teaming assessments and/or social enigneering assessments. Overlord's developers and QSecure decline all responsibility in case the tool is used for malicious purposes or in any illegal context.