#######
# ECM #
#######
ecm (Elastic Cluster Maker) is a simple program that help you to configure and instantiate your elastic cluster.
You only have to follow some simple step:

1. Use your EC2 credential
$ source ec2rc.sh
where ec2rc is the ec2rc file of the project where you want to instantiate your cluster.
[WARNING]
The ecm program asks how you want to instantiate your master node.
If you want to use the nova cli you have to source also the <project_name>-openrc.sh file.
$ source <project_name>-openrc.sh

2. Edit the cluster.conf file

3. Launch the ecm program and follow the instructions
$ python ecm.py 



More details in http://www.pd.infn.it/cloud/Users_Guide/html-desktop/#ClusterConfiguration.
