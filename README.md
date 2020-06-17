# Overlord – Red Teaming Automation
<p align="center">
  <img src="logo.png" width=30%>
</p>

Overlord provides a python-based console CLI which is used to build Red Teaming infrastructure in an automated way. The user has to provide inputs by using the tool’s modules (e.g. C2, Email Server, HTTP web delivery server, Phishing server etc.) and the full infra / modules and scripts will be generated automatically on a cloud provider of choice. Currently supports AWS and Digital Ocean. The tool is still under development and it was inspired and uses the [Red-Baron](https://github.com/byt3bl33d3r/Red-Baron) Terraform implementation found on Github. 

A demo infrastructure was set up in our blog post https://blog.qsecure.com.cy/posts/overlord/.

For the full documentation of the tool visit the Wiki tab at https://github.com/qsecure-labs/overlord/wiki.

# Installation

```bash
git clone https://github.com/qsecure-labs/overlord.git
cd overlord/config
chmod +x install.sh
sudo ./install.sh
```

## Acknowledgments
 
This project could not be created without the awsome work for Marcello Salvati [@byt3bl33d3r](https://twitter.com/byt3bl33d3r) with the [RedBaron](https://github.com/byt3bl33d3r/Red-Baron) Project.
That is the reason why we are referencing the name of RedBaron on our  project as well.
 
As Marcello stated on his acknowledgments, further thanks to:
 
1. [@_RastaMouse's](https://twitter.com/_RastaMouse) two serie's blogpost on 'Automated Red Team Infrastructure Deployment with Terraform' Part [1](https://rastamouse.me/2017/08/automated-red-team-infrastructure-deployment-with-terraform---part-1/) and [2](https://rastamouse.me/2017/09/automated-red-team-infrastructure-deployment-with-terraform---part-2/)
2. [@bluscreenofjeff's](https://twitter.com/bluscreenofjeff) with his amazing Wiki on [Read Team Infrastucture](https://github.com/bluscreenofjeff/Red-Team-Infrastructure-Wiki)
3. [@spotheplanet's](https://ired.team/offensive-security/red-team-infrastructure) blog post on Red team infrastructure

## Disclaimer
Overlord comes without warranty and is meant to be used by penetration testers during approved red teaming assessments and/or social enigneering assessments. Overlord's developers and QSecure decline all responsibility in case the tool is used for malicious purposes or in any illegal context.
