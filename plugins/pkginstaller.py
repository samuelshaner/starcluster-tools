from starcluster.clustersetup import ClusterSetup
from starcluster.logger import log


'''
   This plugin replaces the StarCluster pkginstaller plugin which seems
   to be broken. This plugin allows users to install packages on a new 
   cluster using the apt-get -y install command. Below is an example of
   using the plugin in the config file:

   ######################################################
   [plugin OpenMOC]
   setup_class = pkginstaller.PackageInstaller

   pkgs_to_install = ccache, python-h5py
   ######################################################
   
'''
class PackageInstaller(ClusterSetup):
  def __init__(self, pkg_to_install):
    self.pkg_to_install = pkg_to_install
    log.debug('pkg_to_install = %s' % pkg_to_install)

  def run(self, nodes, master, user, user_shell, volumes):
    for node in nodes:
      for pkg in self.pkg_to_install.split(','):
        log.info("Installing %s on %s" % (pkg, node.alias))
        node.ssh.execute('apt-get -y install %s' % pkg)
