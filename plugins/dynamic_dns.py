from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class PackageInstaller(ClusterSetup):
  def __init__(self, user, passwd, domain):
    self.user = user
    self.passwd = passwd
    self.domain = domain
    log.debug('setting up dynamic dns to %s' % domain)

  def run(self, nodes, master, user, user_shell, volumes):
    for node in nodes:
      cmd = 'wget -O /dev/null http://' + self.user + ':' + self.passwd + \
            '@dynupdate.no-ip.com/nic/update?hostname=' + self.domain
      node.ssh.execute(cmd)
