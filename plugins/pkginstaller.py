from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log

class PackageInstaller(ClusterSetup):
     def __init__(self, pkg_to_install):
          self.pkg_to_install = pkg_to_install
          log.debug('pkg_to_install = %s' % pkg_to_install)
     def run(self, nodes, master, user, user_shell, volumes):
          for node in nodes:
               for pkg in self.pkg_to_install.split(','):
                    log.info("Installing %s on %s" % (pkg, node.alias))
                    node.ssh.execute('apt-get -y install %s' % pkg)
