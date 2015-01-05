__author__ = 'mican'

import os
import sys

OPTIONS = [
    ('help', 0, 'h'),
    ('list', 0, 'l'),
    ('edit', 0, 'e'),
    ('group', 1, 'g'),
    ('domain', 1, 'd'),
    ('switch', 1, 's'),
    ('remove', 1, 'r'),
    ('Remove', 1, 'R'),
    ('version', 0, 'v'),
]

VERSION = 'hosts v1.0.0 Copyright (c) 2014 by micanzhang'


def is_windows():
    return sys.platform == 'win32'


def flush_dns():
    if is_windows():
        os.system("ipconfig /flushdns")


def host_file():
    if is_windows():
        return 'C:\Windows\System32\Drivers\etc\hosts'
    else:
        return '/etc/hosts'


def load_host():
    host_path = host_file()

    if not os.path.isfile(host_path):
        exit('hosts file doesn\'t exists!')

    f = open(host_path)
    buf = f.readlines()
    hosts = {}
    group = 'default'
    data = []
    for line in buf:
        if line.strip() == '':
            pass
        elif line.strip().find('#====') == 0 and line.strip().split('#===').pop() != '':
            hosts[group] = data
            data = []
            group = line.strip().split('#====').pop().strip()
        else:
            data.append(line.strip())

    return hosts


def echo(hosts):
    for group in hosts.keys():
        print "\nGroup name: " + group + "\n"
        for host in hosts[group]:
            print "\t" + host + "\n"


def h_help():
    helps = [
        '-h    --help this help text',
        '-l    --list list all hosts group by group name',
        '-e    --edit edit hosts file use default editor',
        '-s    --switch [group_name] set all hosts enable which belongs to group_name',
        '-g    --group [group_name] list hosts which group by group_name',
        '-d    --domain [domain] list all group_name domain belongs to',
        '-r    --remove [group_name] set hosts disable which belongs to group_name',
        '-R    --Remove [domain] set domain disable',
        '-v    --version version info',
    ]
    print "Useage: hosts [options...]\n"
    for h_text in helps:
        print h_text


def h_group(group):
    h_list(group)

def h_list(group=None):
    hosts = load_host()
    if group is not None:
        if group in hosts:
            echo({group: hosts[group]})
        else:
            print "Invalid group name: " + group + ".\n"
    else:
        echo(hosts)


def h_domain(domain):
    hosts = load_host()
    d_hosts = dict()

    for group in hosts:
        for host in hosts[group]:
            l = filter(lambda x: len(x) > 0, host.split(' '))
            if domain in l:
                if domain not in d_hosts:
                    d_hosts[group] = list()
                d_hosts[group].append(host)

    echo(d_hosts)


def h_switch(group):
    hosts = load_host()
    if not group in hosts:
        exit("hosts: invalid group name, try 'hosts -l' for more information\n")
    g_hosts = hosts[group]
    data = list()
    for host in g_hosts:
        data.extend(filter(lambda x: len(x) > 0 and x not in data, host.split(' ')[1:]))
    f = open(host_file(), 'r')
    lines = f.readlines()
    f.close()

    g = None
    f = open(host_file(), 'w')
    for line in lines:
        if line.strip() == '':
            pass
        elif line.strip().find('#====') == 0 and line.strip().split('#===').pop() != '':
            g = line.strip().split('#====').pop().strip()
        else:
            if g == group:
                line = line[1:] if line.strip().find('#') == 0 else line
            elif line.strip().find('#') != 0 and len(filter(lambda x: line.strip().find(x) != -1, data)) > 0:
                line = "#" + line
        f.write(line)
    f.close()
    flush_dns()


def h_remove(group):
    f = open(host_file(), 'r')
    lines = f.readlines()
    f.close()

    g = None
    f = open(host_file(), 'w')
    for line in lines:
        if line.strip() == '':
            pass
        elif line.strip().find('#====') == 0 and line.strip().split('#===').pop() != '':
            g = line.strip().split('#====').pop().strip()
        else:
            if g == group and line.strip().find('#') == -1:
                line = '#' + line
        f.write(line)
    f.close()
    flush_dns()


def h_Remove(domain):
    f = open(host_file(), 'r')
    lines = f.readlines()
    f.close()

    f = open(host_file(), 'w')
    for line in lines:
        if line.strip().find('#') == -1 and line.strip().find(domain) != -1:
            line = "#" + line
        f.write(line)
    f.close()
    flush_dns()


def h_edit():
    if is_windows():
        os.system('start ' + host_file())
    else:
        if os.system('command -v emacs') != 32512:
            cmd = 'emacs'
        elif os.system('command -v vim') != 32512:
            cmd = 'vim'
        else:
            cmd = 'vi'
        os.system(cmd + " " + host_file())


def parse_opt(opt):
    if opt.find('--') == 0:
        opt = opt[2:]
    elif opt.find('-') == 0:
        opt = opt[1:]

    for item in OPTIONS:
        if item[0] == opt or item[-1] == opt:
            return item
    return None


def parse_cmd():
    args = sys.argv[1:]
    opt = args[0].strip()
    opt_config = parse_opt(opt)
    if opt_config is None:
        exit("hosts: invalid option, try 'hosts -h' for more information\n")

    func = "h_" + opt_config[0]
    possibles = globals().copy()
    possibles.update(locals())
    if opt_config[1] is 0:
        method = possibles.get(func)()
    else:
        if len(args) < 2:
            exit("hosts:  miss parameters, try 'hosts -h' for more information\n")
        method = possibles.get(func)(args[1])
    #method(args[1:])
    '''
        list_options()
    elif opt_config[-1] == 'l':
        list_hosts()
    elif opt_config[-1] == 'e':
        edit_host()        
    elif opt_config[-1] == 'g':
        if len(args) < 2:
            exit("hosts: group name missing, try 'hosts -h' for more information\n")
        list_hosts(args[1])
    elif opt_config[-1] == 'd':
        if len(args) < 2:
            exit("hosts: domain missing, try 'hosts -h' for more information\n")
        domain_hosts(args[1])
    elif opt_config[-1] == 's':
        if len(args) < 2:
            exit("hosts: domain missing, try 'hosts -h' for more information\n")
        switch_hosts(args[1])
    elif opt_config[-1] == 'r':
        if len(args) < 2:
            exit("hosts: host name missing, try 'hosts -h' for more information\n")
        remove_group(args[1])
    elif opt_config[-1] == 'R':
        if len(args) < 2:
            exit("hosts: domain missing, try 'hosts -h' for more information\n")
        remove_domain(args[1])
    elif opt_config[-1] == 'v':
        exit(VERSION)
    else:
        exit("hosts: invalid option, try 'hosts -h' for more information\n")
    '''

if __name__ == '__main__':
    if len(sys.argv) < 2:
        exit("hosts: try 'hosts -h' for more information\n")

    parse_cmd()
