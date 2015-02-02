from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log


'''
   This plugin lets users set a hostname for their cluster that
   can be used by other users for direct ssh access. This allows users
   to ssh using the standard username@hostname syntax, but using the
   same hostname regardless of the public IP address of the EC2 instance.
   Below is an example of using the plugin in the config file:

   ######################################################
   [plugin dynamic-dns]
   setup_class = dynamic_dns.SetupDynamicDNS

   username = samuelshaner
   password = yGL1x40ELVv0
   hostname = testcluster.ddns.net
   ######################################################
   
   Where username and password are the username and password for a noip.com
   account and hostname is a hostname that you have registered with
   noip.com (noip.com gives all users 3 free hostnames).

   Everytime you run this plugin on a cluster, it pings the noip.com servers
   and updates the IP address associated with the hostname with the public IP
   address of your EC2 instance.

'''
class SetupDynamicDNS(ClusterSetup):
  def __init__(self, username, password, hostname):
    self.username = username
    self.password = password
    self.hostname = hostname
    log.debug('setting up dynamic dns to %s' % hostname)

  def run(self, nodes, master, user, user_shell, volumes):
    for node in nodes:
      cmd = 'wget -O /dev/null http://' + self.username + ':' + self.password +\
            '@dynupdate.no-ip.com/nic/update?hostname=' + self.hostname
      node.ssh.execute(cmd)
