import datetime
import sys
import base64
from subprocess import call

scripts = [(1, "Scientific Linux 6", "scientific", "master_files/SL6-master", "slave_files/SL6-slave"),
           (2, "Ubuntu", "ubuntu", "master_files/Ubuntu-master", "slave_files/Ubuntu-slave"),
           (3, "uCernVM", "ucernvm", "master_files/uCernVM-master", "slave_files/uCernVM-slave"),
           (4, "CentOS 7", "centos", "master_files/CentOS7-master", "slave_files/CentOS7-slave")]
           
SL_images = [(1, "SL68-x86_64-20161107", "ami-6b1406fc"),
          (2, "SL67-x86_64-20151017", "ami-09877a78"),
          (3, "SL66-x86_64-20150521", "ami-d558813f"),
          (4, "SL66-x86_64-20150309", "ami-55829d60"),
          (5, "SL66-x86_64-20150131", "ami-dc9da54c"),
          (6, "SL65-x86_64-20151029", "ami-d760f202"),
          (7, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
          
ubuntu_images = [(1, "ubuntu-trusty-20141025", "ami-84616f8f"),
          (2, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
          
cern_images = [(1, "uCernVM 3.4.3", "ami-fcfdc38d"),
          (2, "uCernVM 2.3-0", "ami-c84d00a7"),
          (3, "uCernVM 1.18.14", "ami-aebb6e5f"),
          (4, "uCernVM 1.18.13", "ami-7ad4ec84"),
          (5, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]

centos_images = [(1, "CentOS 7", "ami-9f3da3fc"),
                 (2, "CentOS-7-x86_64-GenericCloud-1608", "ami-3f901eed"),
                 (3, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
           
if __name__ == "__main__":

    number_version, info_version=sys.version.split(" (default")
    major_version, minor_version, micro_version = number_version.split(".")

    today = datetime.date.today()
    now_time = "%s" %datetime.datetime.now().time()
    now_long, now_numeber = now_time.split(".")
    now_hour, now_min, now_sec = now_long.split(":")
    now = "%s.%s.%s" %(now_hour, now_min, now_sec)

    file = open('ecm.conf', 'r')

    params = dict()
    for line in file:
        try:
            k, v = line.split("=")
        except:
            line=line
        params[k] = v.strip()
    flavor_vms = params['FLAVOR_VMS']
    max_vms = params['MAX_VMS']
    min_vms = params['MIN_VMS']
    jobs_per_vm = params['JOBS_PER_VM']
    idle_time = params['IDLE_TIME']
    key_name = params['KEY_NAME']

    print("\nChoose the Operating System (OS) type that you want to use for your master and worker nodes:")
    for n, d, so, f, slf in scripts:
        print("%s: %s" % (n, d))
    which = input()
    ctrl=int(which)

    try:
        if ctrl < 1:
            exit("[ERROR] Wrong selection.")
        else:
            n, d, s, f, slf = scripts[ctrl-1]

            user_data_file = "master-%s-%s-%s" %(s, today, now)
            slave_file = open(slf, 'r')
            userdata = slave_file.read()
            slave_userdata = base64.b64encode(userdata)

            if n == 1:
                print("\nSelect the image for your %s based master and your %s based WNs:" %(d, d)) 
                for m, b, g in SL_images:
                    print("%s: %s" % (m, b))
                image = input()
                try:
                    m, b, g = SL_images[int(image)-1]
                    if int(image) == 7:
                        print("\nInsert the EC2-id (something like ami-00000000)")
                        if int(major_version) < 3:
                            image_number = raw_input("ami-")
                        else:
                            image_number = input("ami-")
                        if len(image_number) == 8:
                            image_id = "%s%s" %(g, image_number)
                        else:
                            exit("Incorrect EC2-id.")
                    elif int(image) < 1:
                        exit("[ERROR] Wrong selection.")
                    else:
                        image_id = g
                except IndexError:
                    exit("[ERROR] Wrong selection.")
            elif n == 2:
                print("\nSelect the image for your %s based master and your %s based WNs:" %(d, d)) 
                for m, b, g in ubuntu_images:
                    print("%s: %s" % (m, b))
                image = input()
                try:
                    m, b, g = ubuntu_images[int(image)-1]
                    if int(image) == 2:
                        print("\nInsert the EC2-id (something like ami-00000000)")
                        if int(major_version) < 3:
                            image_number = raw_input("ami-")
                        else:
                            image_number = input("ami-")
                        if len(image_number) == 8:
                            image_id = "%s%s" %(g, image_number)
                        else:
                            exit("Incorrect EC2-id.")
                    elif int(image) < 1:
                        exit("[ERROR] Wrong selection.")
                    else:
                        image_id = g
                except IndexError:
                    exit("[ERROR] Wrong selection.")
            elif n == 3:
                print("\nSelect the image for your %s based master and your %s based WNs:" %(d, d)) 
                for m, b, g in cern_images:
                    print("%s: %s" % (m, b))
                image = input()
                try:
                    m, b, g = cern_images[int(image)-1]
                    if int(image) == 5:
                        print("\nInsert the EC2-id (something like ami-00000000)")
                        if int(major_version) < 3:
                            image_number = raw_input("ami-")
                        else:
                            image_number = input("ami-")
                        if len(image_number) == 8:
                            image_id = "%s%s" %(g, image_number)
                        else:
                            exit("Incorrect EC2-id.")
                    elif int(image) < 1:
                        exit("[ERROR] Wrong selection.")
                    else:
                        image_id = g
                except IndexError:
                    exit("[ERROR] Wrong selection.")
            elif n == 4:
                print("\nSelect the image for your %s based master and your %s based WNs:" %(d, d)) 
                for m, b, g in centos_images:
                    print("%s: %s" % (m, b))
                image = input()
                try:
                    m, b, g = centos_images[int(image)-1]
                    if int(image) == 3:
                        print("\nInsert the EC2-id (something like ami-00000000)")
                        if int(major_version) < 3:
                            image_number = raw_input("ami-")
                        else:
                            image_number = input("ami-")
                        if len(image_number) == 8:
                            image_id = "%s%s" %(g, image_number)
                        else:
                            exit("Incorrect EC2-id.")
                    elif int(image) < 1:
                        exit("[ERROR] Wrong selection.")
                    else:
                        image_id = g
                except IndexError:
                    exit("[ERROR] Wrong selection.")

            command = "mv master-* user_data_files.old/"
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "cp %s %s" %(f, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|access-key|$EC2_ACCESS_KEY| \" %s" %user_data_file
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|secret-key|$EC2_SECRET_KEY|g\" %s " %user_data_file
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|ec2-url|$EC2_URL|g\" %s" %user_data_file
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|instance-flavor|%s|g\" %s" %(flavor_vms, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|idle-time|%s|g\" %s " %(idle_time, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
        
            command = "sed -i \"s|max-vms|%s|g\" %s " %(max_vms, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|min-vms|%s|g\" %s " %(min_vms, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
        
            command = "sed -i \"s|image-id|%s|g\" %s " %(image_id, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|jobs-per-vm|%s|g\" %s " %(jobs_per_vm, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)

            command = "sed -i \"s|key-name|%s|g\" %s " %(key_name, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            command = "sed -i \"s|slave-userdata|%s|g\" %s " %(slave_userdata, user_data_file)
            cl_options = ""
            call([command, cl_options], shell=True)
            
            print("\nNow you can use the %s file to instantiate the master node of your elastic cluster." %user_data_file)

    except IndexError:
        exit("[ERROR] Wrong selection.")
