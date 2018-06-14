# cloud-vms

Scripts for launching large numbers of VMs on CyVerse Atmosphere and XSEDE Jetstream

scripts and code written by [Julian Pistorius](https://github.com/julianpistorius)

# Contents

## launch_ .py

Run this script to launch on the given cloud provider; here we are supporting IU (Indiana) TACC (Texas Advanced Computing Center), Marana (CyVerse).
  
## clouds.yaml

This `.yaml` file has the parameter values for each cloud service - you will need to update your `username`, `project` and `password` information.

Your `username` and `project` are the same; use your CyVerse or Jetstream usernames.

For the `password`, get your API Credentials from your cloud provider.

[Jetstream API Credentials](https://use.jetstream-cloud.org/api/credentials)

[Atmosphere API Credentials](https://atmo.cyverse.org/api/credentials) 

Select the hashed value from the `"value"` field:

```
"key": "secret",
"value": "dxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx2"
 ```
 
