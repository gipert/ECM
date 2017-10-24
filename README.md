# ECM 

ecm (Elastic Cluster Maker) is a simple program that help you to configure and instantiate your elastic cluster.

## Create your userdata file

You only have to follow some simple step:

1. Use your EC2 credential
```bash
$ source ec2rc.sh
```
where ec2rc is the ec2rc file of the project where you want to instantiate your cluster.

2. Edit the cluster.conf file

3. Launch the ecm script and follow the instructions
```bash
$ python ecm.py 
```

## Docker universe

Using a CentOS7 based cluster you can submit jobs using the docker universe of HTCondor.

## Customize your cluster

You can customize your cluster edit the master_files and the slave_files before run the script.


## Complite documentation

More details in http://www.pd.infn.it/cloud/Users_Guide/html-desktop/#ClusterConfiguration.
