'''
Created on Dec 7, 2010

@author: borja
'''
from cPickle import dump, load, HIGHEST_PROTOCOL

class DGGrid(object):    
    
    def __init__(self):
        self.global_attributes = {}
        self.grid_nodes = []
        self.organizations = {}
        
    def add_organization(self, org):
        self.organizations[org.name] = org

    def add_org_node(self, org, node):
        self.grid_nodes.append(node)

    def add_node(self, node):
        self.grid_nodes.append(node)
        
    def get_nodes(self):
        nodes = self.grid_nodes[:]
        for org in self.organizations.values():
            nodes += org.get_nodes()
        return nodes
    
    def get_node_by_id(self, host_id):
        nodes = self.get_nodes()
        node = [n for n in nodes if n.demogrid_host_id == host_id]
        if len(node) == 1:
            return node[0]
        else:
            return None
    
    def get_users(self):
        users = []
        for org in self.organizations.values():
            users += org.get_users()
        return users    
    
    def gen_ruby_file(self, file):
        topology = ""

        for k,v in self.global_attributes.items():
            topology += "node.normal[:%s] = %s\n" % (k,v)
            
        topology += "\n"
      
        nodes = self.get_nodes()
        for n in nodes:
            topology += "if node.name == \"%s\"\n" % n.hostname
            for k,v in n.attrs.items():
                topology += "  node.normal[:%s] = %s\n" % (k,v)
            topology += "end\n\n"            

        for org in self.organizations.values():
            topology += "default[:orgusers][\"%s\"] = [\n" % org.name
            for u in org.users:
                topology += "{ :login       => \"%s\",\n" % u.login
                topology += "  :description => \"%s\",\n" % u.description
                topology += "  :password    => \"%s\",\n" % u.password
                topology += "  :password_hash => \"%s\",\n" % u.password_hash
                if u.gridenabled:
                    topology += "  :gridenabled => true,\n"
                    topology += "  :auth_type   => :%s}" % u.auth_type
                else:
                    topology += "  :gridenabled => false}"
                topology += ",\n"
            topology += "]\n"

        topologyfile = open(file, "w")
        topologyfile.write(topology)
        topologyfile.close()      
        
    def gen_hosts_file(self, filename, extra_entries = []):
        hosts = """127.0.0.1    localhost

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
fe00::0 ip6-localnet
ff00::0 ip6-mcastprefix
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
ff02::3 ip6-allhosts

"""
        for ip, hostname in extra_entries:
            hosts += "%s %s %s\n" % (ip, hostname, hostname.split(".")[0])
        
        nodes = self.get_nodes()
        for n in nodes:
            hosts += " ".join((n.ip, n.hostname, n.hostname.split(".")[0], "\n"))
        
        hostsfile = open(filename, "w")
        hostsfile.write(hosts)
        hostsfile.close()        
        
    def gen_csv_file(self, filename):
        attr_names = set()
        nodes = self.get_nodes()
        
        for n in nodes:
            attr_names.update(n.attrs.keys())
            
        attr_names = list(attr_names)
        csv = "org,hostname,role,ip," + ",".join(attr_names) + "\n"
        
        for n in nodes:
            if n.org:
                orgname = n.org.name
            else:
                orgname = ""
            fields = [orgname, n.hostname, n.role, n.ip]
            for name in attr_names:
                fields.append(n.attrs.get(name,""))
            csv += ",".join(fields) + "\n"
            
        csvfile = open(filename, "w")
        csvfile.write(csv)
        csvfile.close()                
        
    def save(self, filename):
        f = open (filename, "w")
        dump(self, f, protocol = HIGHEST_PROTOCOL)
        f.close()

   
class DGOrganization(object):    
    def __init__(self, name, subnet):
        self.name = name
        self.subnet = subnet
        self.nodes = []
        self.users = []
        self.server = None
        self.auth = None
        self.lrm = None

    def add_node(self, node):
        self.nodes.append(node)
        
    def get_nodes(self):
        return self.nodes
        
    def add_user(self, user):
        self.users.append(user)   
        
    def get_users(self):
        return self.users
    
class DGNode(object):
    def __init__(self, role, ip, hostname, org = None):
        self.role = role
        self.ip = ip
        self.hostname = hostname
        self.demogrid_hostname = hostname
        self.demogrid_host_id = hostname.split(".")[0]
        self.org = org
        self.attrs = {}
        
class DGOrgUser(object):
    def __init__(self, login, description, gridenabled, password, password_hash, auth_type=None):
        self.login = login
        self.description = description
        self.gridenabled = gridenabled
        self.auth_type = auth_type
        self.password = password
        self.password_hash = password_hash        