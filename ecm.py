import datetime
import sys
from subprocess import call

scripts = [(1, "Scientific Linux", "scientific", "master_files/SL6-master"),
           (2, "Ubuntu", "ubuntu", "master_files/Ubuntu-master"),
           (3, "uCernVM", "ucernvm", "master_files/uCernVM-master")]

method = [(1, "Dashboard. [INFO] You use the genereted userdata file as portinstallation file."),
           (2, "Euca2ools. [WARNING] You have to have euca2ools.2.x installed in your PC."),
           (3, "Nova CLI. [WARNING] You have to have nova-client installed in your PC.")]
           
SL_images = [(1, "SL67-x86_64-20151017", "ami-09877a78"),
          (2, "SL66-x86_64-20150521", "ami-d558813f"),
          (3, "SL66-x86_64-20150309", "ami-55829d60"),
          (4, "SL66-x86_64-20150131", "ami-dc9da54c"),
          (5, "SL65-x86_64-20151029", "ami-d760f202"),
          (6, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
ubuntu_images = [(1, "ubuntu-trusty-20141025", "ami-84616f8f"),
          (2, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
cern_images = [(1, "uCernVM 3.4.3", "ami-fcfdc38d"),
          (2, "uCernVM 2.3-0", "ami-c84d00a7"),
          (3, "uCernVM 1.18.14", "ami-aebb6e5f"),
          (4, "uCernVM 1.18.13", "ami-7ad4ec84"),
          (5, "Other image. [WARNING] You have to know the EC2-id of image", "ami-")]
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
        k, v = line.split("=")
        params[k] = v.strip()
    w_flavor = params['WNS_FLAVOR']
    max_vms = params['MAX_VMS']
    min_vms = params['MIN_VMS']
    jobs_per_vm = params['JOBS_PER_VM']
    idle_time = params['IDLE_TIME']

    print("\nChose SO that you want to use for your master and worker nodes:")
    for n, d, so, f in scripts:
        print("%s: %s" % (n, d))
    which = input("Which SO do you prefer?\n")
    ctrl=int(which)

    try:
        if ctrl < 1:
            exit("[ERROR] Wrong selection.")
        else:
            n, d, s, f = scripts[ctrl-1]

            user_data_file = "master-%s-%s-%s" %(s, today, now)

            if n == 1:
                print("\nSelect the image for your %s based master and your %s based WNs:" %(d, d)) 
                for m, b, g in SL_images:
                    print("%s: %s" % (m, b))
                image = input()
                try:
                    m, b, g = SL_images[int(image)-1]
                    if int(image) == 6:
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
            
            command = "sed -i \"s|instance-flavor|%s|g\" %s" %(w_flavor, user_data_file)
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

            print("\nYou can use one of these methods:")
            for v, k in method:
                print("%s: %s" % (v, k))
            how = input("How do you prefer?\n")
            v = int(how)
            if v == 1:
                print("Now you can use the %s file to instantiate the master node of your elastiq cluster." %user_data_file)
            elif v == 2:
                print("\nInsert master flavor name:")
                if int(major_version) < 3:
                    m_flavor = raw_input()
                else:
                    m_flavor = input()
                if int(major_version) < 3:
                    group = raw_input("\nInsert master security group name:\n")
                else:
                    group = input("\nInsert master security group name:\n")
                if int(major_version) < 3:
                    key_name = raw_input("\nInsert master key pair name. [WARNING] If your key pair file name is my_key.pem you have to insert only my_key.\n")
                else:
                    key_name = input("\nInsert master key pair name. [WARNING] If your key pair file name is my_key.pem you have to insert only my_key.\n")
                print("\nNow we are instantiating your master node via euca2ools.\n")
                command = "euca-run-instances -t %s -k '%s' -f %s -g %s %s" %(m_flavor, key_name, user_data_file, group, image_id)
                cl_options = ""
                print(command)
                call([command, cl_options], shell=True)
            elif v == 3:
                print("\nInsert master name:")
                if int(major_version) < 3:
                    vm_name = raw_input()
                else:
                    vm_name = input()
                print("\nInsert master image name:")
                if int(major_version) < 3:
                    image_name = raw_input()
                else:
                    image_name = input()
                print("\nInsert master flavor name:")
                if int(major_version) < 3:
                    m_flavor = raw_input()
                else:
                    m_flavor = input()
                if int(major_version) < 3:
                    group = raw_input("\nInsert master security group name:\n")
                else:
                    group = input("\nInsert master security group name:\n")
                if int(major_version) < 3:
                    key_name = raw_input("\nInsert master key pair name. [WARNING] If your key pair file name is my_key.pem you have to insert only my_key.\n")
                else:
                    key_name = input("\nInsert master key pair name. [WARNING] If your key pair file name is my_key.pem you have to insert only my_key.\n")
                print("\nNow we are instantiating your master node via nova-cli.\n")
                command = "nova boot %s --image \"%s\" --flavor %s --user_data %s --key_name %s --security-group %s" %(vm_name, image_name, m_flavor, user_data_file, key_name, group)
                cl_options = ""
                print(command)
                call([command, cl_options], shell=True)
            else:
                exit("[ERROR] Wrong selection.")


    except IndexError:
        exit("[ERROR] Wrong selection.")
