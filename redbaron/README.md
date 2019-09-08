# Red Baron [QSecure Edition]

<p align="center">
  <img src="https://orig00.deviantart.net/5aae/f/2016/085/0/5/bloody_baron_by_synestesi_art-d9wjp94.jpg" width="400" height="600" alt="baron"/>
</p>


Red Baron is a set of [modules](https://www.terraform.io/docs/modules/index.html) and custom/third-party providers for [Terraform](https://www.terraform.io/) which tries to automate creating resilient, disposable, secure and agile infrastructure for Red Teams.


# Setup

**Red Baron only supports Terraform version 0.11.0 or newer and will only work on Linux x64 systems.** 

Download Terraform from https://www.terraform.io/downloads.html (versions 0.11.14 works fine)
Install Terraform using the instructions on https://learn.hashicorp.com/terraform/getting-started/install.html
The terraform works with:
https://releases.hashicorp.com/terraform/0.11.14/

Install Ansible: ```sudo pip install ansible```
```
#~ git clone git@gitlab.cdma.com.cy:vsikkis/redbaron.git && cd redbaron
```
The only token we need is from Digital Ocean. it was added to the ~/variables.tf ```DIGITALOCEAN_TOKEN="token"```. The file contains and the domains in a list which they will be used in the engagement.

Copy an infrastructure configuration file from the examples folder (preferably ```qsecure-template.tf``` ) to the root directory and modify it to your needs. The directory holds more examples and the ```qsecure-full.tf``` that contains experimental code with all the functionality.
```
#~ cp examples/qsecure/qsecure-template.tf .
#~ cp examples/qsecure/variables.tf .

#~ terraform init
#~ terraform plan
#~ terraform apply
```
# Modules
Each module has its own README.md containing all the necessary information to load and execute.

# Tool & Module Documentation
The official github repo has moved : https://github.com/byt3bl33d3r/Red-Baron
For detailed documentation on the tool and each module please see Red Baron's [wiki](https://github.com/coalfire/pentest-red-baron/wiki).
Most of the documentation assumes you are familiar with [Terraform](https://www.terraform.io/) itself, [Terraform's](https://www.terraform.io/) documentation can be found [here](https://www.terraform.io/docs/index.html).



# License

This fork of the original Red Baron repository is licensed under the GNU General Public License v3.0.
