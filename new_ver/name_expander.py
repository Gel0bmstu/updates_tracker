import rpm
import os
import sys
import tempfile
import requests
import json
import re

headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36'}

def get_nvs(spec):
    try:
       nvs = []
       ts = rpm.TransactionSet()
       rpm_spec = ts.parseSpec(spec)
       name = rpm.expandMacro("%{name}")
       version = rpm.expandMacro("%{version}")
       nvs.append(name)
       nvs.append(version)
       for (filename, num, flags) in rpm_spec.sources:
           if num == 0 and flags == 1:
               # prints htop.tar.gz
               tarball = filename.split("/")[-1]
               # full path
               # http://mirrors.n-ix.net/mariadb/mariadb-10.3.9/source/mariadb-10.3.9.tar.gz
               # print(filename)
               nvs.append(filename)
       return nvs
    except:
        return None


def check_version(package):
    url = "http://github.com/OpenMandrivaAssociation/{package}/raw/master/{package}.spec".format(package=package)
    resp = requests.get(url, headers=headers)
    temp = tempfile.NamedTemporaryFile(prefix=package, suffix=".spec")
    if resp.status_code == 404:
        print('requested package [{}] not found'.format(package))
    if resp.status_code == 200:
       spec = resp.content
       try:
           spec_path = temp.name
           # print("Created file is:", temp)
           # print("Name of the file is:", temp.name)
           temp.write(spec)
           temp.seek(0)
           names = get_nvs(spec_path)
           name = names[0]
           version = names[1]
           source0 = names[2]
#           print(source0)
#           print(name, version, source0)
           return name, version, source0
       except:
           return name, version, None
       finally:
           temp.close()

def github_check(upstream_url):
    split_url = upstream_url.split("/")[:-2]
#    print(split_url)
    project_url = '/'.join(split_url[:6]) + '/'
    try:
        apibase = 'https://api.github.com/repos' + '/' + split_url[3] + '/' +  split_url[4] + '/tags'
        print(apibase)
        github_json = requests.get(apibase, headers=headers)
        data = github_json.json()
        project_name = (data[0]['name'])
        if 'xf86' in project_url:
            category_match = re.search('[-]([\d.]*\d+)', project_name)
            upstream_version = category_match.group(1)
            print(upstream_version)
        else:
            category_match = re.search('\d+(?!.*/).*\d+', project_name)
            upstream_version = category_match.group(0)
            print(upstream_version)
        return upstream_version, project_url
    except:
        apibase = 'https://api.github.com/repos' + '/' + split_url[3] + '/' +  split_url[4] + '/releases'
#        print(apibase)
        github_json = requests.get(apibase, headers=headers)
        data = github_json.json()
        project_name = (data[0]['name'])
        # 'start'
#        print(project_name)
        category_match = re.search('\d+(?!.*/).*\d+', project_name)
        upstream_version = category_match.group(0)
        # good version here
        print(upstream_version, project_url)
        return upstream_version, project_url

def freedesktop_check(upstream_url, package):
    split_url = upstream_url.split("/")[:6]
    project_url = '/'.join(split_url[:6]) + '/'
    print(project_url)
    freedesktop_req = requests.get(project_url, headers=headers, allow_redirects=True)
    version_list = []
    if freedesktop_req.status_code == 404:
        print('requested url [{}] not found'.format(url))
    if freedesktop_req.status_code == 200:
        if 'x11-driver' in package:
            split_name = package.split("-")[:4]
            xf86base = 'xf86-' + (split_name[2]) + '-' + (split_name[3])
            category_match = re.finditer(xf86base+'[-]([\d.]*\d+)', freedesktop_req.content.decode('utf-8'))
            for match in category_match:
                version_list.append(match[1])
            upstream_max_version= max([[int(j) for j in i.split(".")] for i in version_list])
            upstream_version = ".".join([str(i) for i in upstream_max_version])
            return upstream_version, project_url
        elif not 'x11-driver' in package:
            pkg_notcare = re.compile(package+'[-]([\d.]*\d+)', re.IGNORECASE)
            category_match = re.finditer(pkg_notcare, freedesktop_req.content.decode('utf-8'))
            for match in category_match:
                version_list.append(match[1])
            upstream_max_version = max([[int(j) for j in i.split(".")] for i in version_list])
            upstream_version = ".".join([str(i) for i in upstream_max_version])
            print(upstream_version, project_url)
            return upstream_version, project_url

def check_upstream(package):
    upstream_name, our_ver, upstream_url = check_version(package)
    # htop 2.2.0 https://github.com/hishamhm/htop/archive/2.2.0.tar.gz
    print(upstream_name, our_ver, upstream_url)
    if 'github' in upstream_url:
        return github_check(upstream_url)
    if 'freedesktop' in upstream_url:
        return freedesktop_check(upstream_url, package)


#version = get_nvs('/home/omv/mariadb/mariadb.spec')

#check_upstream("libx11")
#check_upstream("x11-driver-video-amdgpu")
#check_github('https://api.github.com/repos/hishamhm/htop/tags', 'htop')
#print(version)
# name
#print(version[0])
# version
#print(version[1])
# source0
#print(version[2])
