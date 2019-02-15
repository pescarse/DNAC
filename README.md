# **Cisco DNA Center interface reporting**

## **Description**

This code is intended to collect filtered port information from Cisco DNA Center and report on status. Report can then be delivered to email for used to create a Server NOW incident. 


## **Resources**

- Cisco DNA Center Platform API -- https://developer.cisco.com/docs/dna-center/
- Service Now integration API


## **Installation**

Update env_lab.txt to env_lab.py and input appropriate authentication details per platform

requirements.txt included needed python packages
- pip install -r requirements.py

## **Usage**

Run from standard command prompt or as a scheduled cron job

package includes arg parsers for options with help context

