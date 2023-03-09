# Compute Engines

Compute Engines run Linux and Windows OS images that Google provides or private custome images. Each instance belongs to GCP project and a project can have one or more instances. While creating, we specify region, zone, instance type and OS information. When it is delete, it is removed from the GCP project. By default, Compute Engine instances have small persistent disk only for OS. If needed, we can add additional persistent disk from storage options.

## Tools for Access

1. Console
2. GCloud CLI with `gcloud storage`
3. Client libraries for programmatic access
4. REST API for making requests using REST calls.
5. Terraform for declarative configuration management

## Key features:

- Access can be controlled using SSH keys which can be generated during instance creation or can be applied which already exists. When VM is accessed using Cloud shell or Console SSH button, an SSH key is automatically generated and applied to the account.
- The default timezzone for the VM is UTC.
- We can add our own ssh key to Metadata section in Compute Engines > Settings section. The key has to be in below format.

```shell
ssh-rsa AAAAB3Nza... google-ssh {"userName":"username@hostname","expireOn":"2023-03-09T20:12:00+0000"}
```

- The default VPN has firewall rules to allow for ICMP, SSH, RDP from everywhere around the world and all communication for internal IP ranges.
- We can stop or reset the machine using UI or even with command line.
- Permissions assigned to the VM can be seen under PERMISSIONS tab.
