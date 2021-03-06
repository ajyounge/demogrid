# -------------------------------------------------------------------------- #
# Copyright 2010, University of Chicago                                      #
#                                                                            #
# Licensed under the Apache License, Version 2.0 (the "License"); you may    #
# not use this file except in compliance with the License. You may obtain    #
# a copy of the License at                                                   #
#                                                                            #
# http://www.apache.org/licenses/LICENSE-2.0                                 #
#                                                                            #
# Unless required by applicable law or agreed to in writing, software        #
# distributed under the License is distributed on an "AS IS" BASIS,          #
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
# See the License for the specific language governing permissions and        #
# limitations under the License.                                             #
# -------------------------------------------------------------------------- #

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# RECIPE: Globus Toolkit 5.0.3 GRAM for Condor
#
# THis recipe assumes that the "gram" and "condor_head" recipes have been run, 
# and sets GRAM up to interface with Condor. 
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Since there is no binary distribution of GT5, and the gram5-condor package
# will only compile on a node that has Condor on it, we can't provide a pre-compiled
# version. So, we have to install the necessary compile tools + libraries, and
# compile gram5-condor. Fortunately, this doesn't take too long.
package "gcc"
package "libssl0.9.8"
package "libssl-dev"

# We'll need the pre-compiled source tarball.
install_tarball = "gt5.0.3-source-install.tgz"

# Make sure the globus user has all the Condor commands in its PATH.
ruby_block "globus.condor" do
  block do
    add_line("/home/globus/.profile", ". /usr/local/condor-7.4.3/condor.sh")
  end
end


# Compile and install gram5-condor

# TODO: Figure out how to determine if gram5-condor is already installed,
# so we can skip this step.

if ! File.exists?(node[:globus][:srcdir])
  cookbook_file "/var/tmp/#{install_tarball}" do
    source "#{install_tarball}"
    mode 0755
    owner "globus"
    group "globus"
  end
  
  execute "tar" do
    user "globus"
    group "globus"
    cwd "/var/tmp"
    command "tar xzf /var/tmp/#{install_tarball}"
    action :run
  end
end

if ! File.exists?("#{node[:globus][:dir]}/etc/grid-services/jobmanager-condor") 
  execute "make gram5-condor" do
    user "globus"
    group "globus"
    cwd node[:globus][:srcdir]
    command "make gram5-condor"
    action :run
  end
  
  execute "make install" do
    user "globus"
    group "globus"
    cwd node[:globus][:srcdir]
    command "PATH=/usr/local/condor-7.4.3/bin/:$PATH; make install"
    action :run
  end
end