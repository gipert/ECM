import datetime
import sys
import base64
from subprocess import call
from subprocess import PIPE
import subprocess

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

scripts = [(1, "Scientific Linux 6", "scientific", "master_files/SL6-master", "slave_files/SL6-slave"),
           (2, "Ubuntu", "ubuntu", "master_files/Ubuntu-master", "slave_files/Ubuntu-slave"),
           (3, "uCernVM", "ucernvm", "master_files/uCernVM-master", "slave_files/uCernVM-slave"),
           (4, "CentOS 6", "centos6", "master_files/CentOS6-master", "slave_files/CentOS6-slave"),
           (5, "CentOS 7", "centos7", "master_files/CentOS7-master", "slave_files/CentOS7-slave")]

#global variables

all_images = []
all_name_ami = []

#functions

def list_create():
   args = "euca-describe-images -I $EC2_ACCESS_KEY -S $EC2_SECRET_KEY --debug 2>&1 | grep '<imageId>' | uniq | sed 's/<imageId>//' |sed 's/<\/imageId>//'"
   command = ["/bin/bash", "-c", "%s" %args]
   p = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
   i, o = p.communicate()
   i = i.strip()
   ami = i.split('\n      ')

   args = "euca-describe-images -I $EC2_ACCESS_KEY -S $EC2_SECRET_KEY --debug 2>&1 | grep '<name>' | uniq |  sed 's/<name>//' |sed 's/<\/name>//'"
   command = ["/bin/bash", "-c", "%s" %args]
   p = subprocess.Popen(command, stdout=PIPE, stderr=PIPE)
   i, o = p.communicate()
   i = i.strip()
   names = i.split('\n      ')

   list_len=len(ami)/2
   ami = ami[0:list_len]
   names = names[0:list_len]
    
   n = 0
   
   for name in names:
      n_name = names[n]
      n_ami = ami[n]
      n = n+1
      n_name_ami = [n_name , n_ami]
      all_name_ami.append(n_name_ami)


def list_filter(filter):
   num = 1
   for name, ami in all_name_ami:
      if filter in name.lower():
         image = [num, name, ami]
         all_images.append(image)
         num = num+1
   last_line = [num, "Other image. [WARNING] You have to know the EC2-id of image", "ami-"]
   all_images.append(last_line)
   return (all_images, num)

def list_super_filter(filter, super_filter):
   num = 1
   for name, ami in all_name_ami:
      if filter in name.lower():
         if super_filter not in name.lower():
            image = [num, name, ami]
            all_images.append(image)
            num = num+1
   last_line = [num, "Other image. [WARNING] You have to know the EC2-id of image", "ami-"]
   all_images.append(last_line)
   return (all_images, num)

def select_so():
   print color.RED + '\nChoose the Operating System (OS) type that you want to use for your cluster:' + color.END
   for n, d, so, f, slf in scripts:
      print("%s: %s" % (n, d))
   which = input()
   try:
      ctrl=int(which)
      if ctrl < 1:
         print ('\n' + color.BOLD + '[ERROR] Wrong selection.' + color.END)
         select_so()
      else:
         n, d, s, f, slf = scripts[ctrl-1]
         return (n, d, s, f, slf)

   except Exception:
      print ('\n' + color.BOLD + '[ERROR] Wrong selection.' + color.END)
      select_so()

def insert_ami(g):
   print("\nInsert the EC2-id (something like ami-00000000)")
   if int(major_version) < 3:
      image_number = raw_input("ami-")
   else:
      image_number = input("ami-")
   if len(image_number) == 8:
      image_id = "%s%s" %(g, image_number)
      return image_id
   else:
      print ('\n' + color.BOLD +'Incorrect EC2-id.' + color.END )
      insert_ami(g) 
      
def select_image(all_images, num):
   images =  [(values[0], values[1], values[2]) for values in all_images]
               
   print color.RED + '\nSelect the image for your ' + color.END + color.BOLD + '%s' %d + color.END + color.RED +' based cluster:' + color.END
   for m, b, g in images:
      print("%s: %s" % (m, b))
   image = input()
   try:
      m, b, g = images[int(image)-1]
      if int(image) == num:
         image_id = insert_ami(g)
         return image_id
      elif int(image) < 1:
         print ('\n' + color.BOLD + '[ERROR] Wrong selection.' + color.END)
         select_image(all_images, num)
      else:
         image_id = g
         return image_id   
   except Exception:
      print ('\n' + color.BOLD + '[ERROR] Wrong selection.' + color.END)
      select_image(all_images, num)
         
def file_date():
   today = datetime.date.today()
   now_time = "%s" %datetime.datetime.now().time()
   now_long, now_numeber = now_time.split(".")
   now_hour, now_min, now_sec = now_long.split(":")
   now = "%s.%s.%s" %(now_hour, now_min, now_sec)
   return (today, now)

def python_version():
   number_version, info_version=sys.version.split(" (default")
   major_version, minor_version, micro_version = number_version.split(".")
   return major_version

def params(file_name):
   file = open(file_name, 'r')
   
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
   return (flavor_vms, max_vms, min_vms, jobs_per_vm, idle_time, key_name)

# main
           
if __name__ == "__main__":

   (today, now) = file_date()
   major_version = python_version()
   
   (flavor_vms, max_vms, min_vms, jobs_per_vm, idle_time, key_name) = params('ecm.conf')

   list_create()
    
   (n, d, s, f, slf) = select_so()
       
   user_data_file = "master-%s-%s-%s" %(s, today, now)
   slave_file = open(slf, 'r')
   userdata = slave_file.read()
   slave_userdata = base64.b64encode(userdata)
       
   #SL6 cluster
   if n == 1:
      (all_images, num) = list_filter("sl6")
      image_id = select_image(all_images, num)
          
   #UBUNTU cluster
   elif n == 2:
      (all_images, num) = list_filter("ubuntu")
      image_id = select_image(all_images, num)

   #CernVM
   elif n == 3:
      (all_images, num) = list_filter("cern")
      image_id = select_image(all_images, num)

   #CentOS6
   elif n == 4:
      (all_images, num) = list_filter("centos 6")
      image_id = select_image(all_images, num)
         
   #CentOS7
   elif n == 5:
      (all_images, num) = list_super_filter("cent", "centos 6")
      image_id = select_image(all_images, num)

   command = "mv master-* user_data_files.old/"
   cl_options = ""
   call([command, cl_options], shell=True)
   
   command = "cp %s %s" %(f, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
       
   command = "sed -i.bak \"s|access-key|$EC2_ACCESS_KEY| \" %s" %user_data_file
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|secret-key|$EC2_SECRET_KEY|g\" %s " %user_data_file
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|ec2-url|$EC2_URL|g\" %s" %user_data_file
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|instance-flavor|%s|g\" %s" %(flavor_vms, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|idle-time|%s|g\" %s " %(idle_time, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
        
   command = "sed -i.bak \"s|max-vms|%s|g\" %s " %(max_vms, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|min-vms|%s|g\" %s " %(min_vms, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
        
   command = "sed -i.bak \"s|image-id|%s|g\" %s " %(image_id, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|jobs-per-vm|%s|g\" %s " %(jobs_per_vm, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)

   command = "sed -i.bak \"s|key-name|%s|g\" %s " %(key_name, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
            
   command = "sed -i.bak \"s|slave-userdata|%s|g\" %s " %(slave_userdata, user_data_file)
   cl_options = ""
   call([command, cl_options], shell=True)
    
   command = "mv *.bak user_data_files.old/"
   cl_options = ""
   call([command, cl_options], shell=True)
            
   print color.RED + '\nNow you can use the ' + color.END + color.BOLD + '%s ' %user_data_file + color.END + color.RED + 'file to instantiate the master node of your elastic cluster.\nThe slave nodes will be instatiated automatically.' + color.END

