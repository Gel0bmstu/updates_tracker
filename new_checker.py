#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rpm
import os
import sys
import tempfile
import requests
import json
import re
import subprocess
import shutil
import argparse
from flask import Flask, jsonify, request, Response

<<<<<<< Updated upstream
github_headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36',
                  'Authorization': 'token {}'.format(os.getenv('GITHUB_TOKEN'))}
=======
home = os.environ.get('HOME')
project_version = 'master'
>>>>>>> Stashed changes

# Marshal http(s) response to JSON 

#update_spec('vim')
if __name__ == '__main__':
    weird_list = []
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', nargs='+', help='package to upgrade')
    parser.add_argument('--file', help='file with packages list')
    args = parser.parse_args()
    if args.file is not None:
        with open(args.file) as file:
            for line in file:

                # clear lists
                del nvss[:]
                del nvs[:]
                self.api_.logger.debug(line.strip())
                # Remove all spaces at the beginning and end of the line
                package = line.strip()
                err = self.check_version_(package)

                if 'Unable' in err:
                    self.api_.logger.error(err)
                else:
                    try:
                        self.api_.logger.debug('update_spec')
                        self.update_spec(package)
                    except Exception as e:
                        self.api_.logger.error('Unable to update packages from file: {}'.format(e))

    if args.package is not None:
        packages = [i for i in args.package if i is not None]
        for package in packages:
            # clear lists
            del nvss[:]
            del nvs[:]

            self.api_.logger.debug('Checjing version of packge ...')
            err = self.check_version_(package)
            if err is not None:
                self.api_.logger.error(err)
            else:
                self.api_.logger.debug('Updating package ...')
                self.update_spec(package)

class PackageWorker:

    # Server variables
    api_ = ''
    port_ = ''
    adress_ = ''

    # Handlers variables
    
    # name version sources
    nvs_ = []
    nvss_ = []
    home_ = ''
    project_version_ = 'rosa2019.1'

    # headers
    github_headers_ = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36',
                  'Authorization': 'token ceb2aac7b18021638931aab946156095ad034e88'}
    headers_ = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.2171.95 Safari/537.36'}    

    def __init__(self, port=8888, adress='localhost'):
        self.api_ = Flask('RosaPackageWorker')
        self.port_ = port
        self.adress_ = adress
        self.home_ = os.environ.get('HOME')

        self.apply_routes()

        self.run()

    # Set handler functions to routes
    def apply_routes(self):
        self.api_.add_url_rule('/test', 'testpost', self.test_post, methods = ['POST'])
        self.api_.add_url_rule('/test', 'test', self.test, methods = ['GET'])
        self.api_.add_url_rule('/file', 'file', self.update_packages_by_file, methods = ['POST'])
        self.api_.add_url_rule('/packages', 'packages', self.update_packages, methods = ['POST'])

    # API functions

    # Return status code and data as json
    def json_request_(self, url, headers = None):
        # name is package name, i.e. vim
        if headers == None:
            pypi_json = requests.get(url)
        else:
            pypi_json = requests.get(url, headers=headers)
        exit_code = pypi_json.status_code
        if exit_code == 200:
            data = pypi_json.json()
            return exit_code, data
        else:
            return exit_code, None

    # Handlers
    # -----------------------------------------------------------------------------------

    # Getting package name, version and source links list from .spec file
    # path to which is passed to the function.
    # Example: ['vim', '8.1.1524', 'https://github.com/vim/vim/archive', 'https://github.com/vim/vim/archive/v8.1.1524.tar.gz']
    #          ['autofs', '5.1.5', 'https://www.kernel.org/pub/linux/daemons/autofs/v5', 'https://www.kernel.org/pub/linux/daemons/autofs/v5/autofs-5.1.5.tar.xz']
    def get_nvs_(self, spec):
        self.api_.logger.debug('extracting OMV version first')
        try:
            ts = rpm.TransactionSet()
            rpm_spec = ts.parseSpec(spec)
            name = rpm.expandMacro("%{name}")
            version = rpm.expandMacro("%{version}")
            self.nvs_.append(name)
            self.nvs_.append(version)
            
            for (filename, num, flags) in rpm_spec.sources:
                if num == 0 and flags == 1:
                    # path
                    # http://mirrors.n-ix.net/mariadb/mariadb-10.3.9/source/
                    source_link = '/'.join(filename.split("/")[:-1])
                    self.nvs_.append(source_link)
                    self.nvs_.append(filename)
            self.api_.logger.debug('omv version: [{}]'.format(version))
            self.api_.logger.debug('omv package name: [{}]'.format(name))
        except rpm.error:
            self.api_.logger.error('probably specfile damaged')
            return None

    def check_python_module_(self, package):
        try:
            name, omv_version, url, source0 = self.check_version_(package)
            # exclude python-
            split_name = re.split(r'python([\d]?)-', name)[-1]
            url = 'https://pypi.python.org/pypi/{}/json'.format(split_name)
            code, data = self.json_request_(url)
            if code == 200:
                upstream_version = data['info']['version'][:]
                project_url = data['info']['project_url'][:]
                download_url = data['urls']
                for item in download_url:
                    if item['python_version'] == 'source':
                        archive = item['url']
                return None, upstream_version, project_url, archive
            elif code == 404:
                # like pycurl
                # like pyOpenSSL
                split_name = 'py' + name.split("-")[1]
                # still can return 404
                module_request, data = json_request(split_name, url)
                upstream_version = data['info']['version'][:]
                project_url = data['info']['project_url'][:]
                download_url = data['urls']
                for item in download_url:
                    if item['python_version'] == 'source':
                        archive = item['url']
            # self.api_.logger.debug(json.dumps(download_url))
                return upstream_version, project_url, archive
        except Exception as e:
            return 'Unable to check python module: {}'.format(e), None, None, None

    def check_rust_module_(self, package):
        try:
            name, omv_version, url, source0 = check_version(package)
            # exclude python-
            split_name = name.split('rust-', 1)
            url = 'https://crates.io/api/v1/crates/{}'.format(split_name[-1])
            code, data = json_request(split_name, url)
            if code == 200:
                upstream_version = data['crate']['newest_version'][:]
                self.api_.logger.debug(upstream_version)
                return None, upstream_versionm, None
            if code == 404:
                return None, upstream_version, url
        except Exception as e:
            return 'Unable to check rust module: {}'.format(e), None, None

    def repology(self, package):
        url = 'https://repology.org/api/v1/project/{}'.format(package)
        self.api_.logger.debug(url)
        module_request, data = json_request(package, url)
        
        # Checkig package exists
        if not data:
            self.api_.logger.debug('Package "{}" not found.'.format(package))
            return None, None

        match = None
        for d in data:
            if all(k in d for k in ('status', 'repo')) and d['status'] == 'newest':
                match = d
                break
        repo = match['repo']
        self.api_.logger.debug(repo)
        upstream_version = match['version']
        return upstream_version, repo

    def any_other(upstream_url, package):
        split_url = upstream_url.split("/")[:6]
        project_url = '/'.join(split_url[:5])
        req = requests.get(project_url, headers=headers, allow_redirects=True)
        self.api_.logger.debug(project_url)
        version_list = []
        if req.status_code == 404:
            self.api_.logger.debug('requested url [{}] not found'.format(upstream_url))
        if req.status_code == 200:
            try:
                pkg_notcare = re.compile(package+'[-]([\d.]*\d+)', re.IGNORECASE)
                category_match = re.finditer(
                    pkg_notcare, req.content.decode('utf-8'))
                for match in category_match:
                    version_list.append(match[1])
                upstream_max_version = max(
                    [[int(j) for j in i.split(".")] for i in version_list])
                upstream_version = ".".join([str(i) for i in upstream_max_version])
                self.api_.logger.debug(upstream_version, project_url)
                return upstream_version, project_url
            except:
                category_match = re.finditer(
                    'href=[\'"]?([\d.]*\d+)', req.content.decode('utf-8'))
                for match in category_match:
                    version_list.append(match[1])
                upstream_max_version = max(
                    [[int(j) for j in i.split(".")] for i in version_list])
                upstream_version = ".".join([str(i) for i in upstream_max_version])
                self.api_.logger.debug(upstream_version, project_url)
                return upstream_version, project_url

    def check_version_(self, package):
        self.api_.logger.debug('Checking OpenMandriva ingit3 version for package [{}]'.format(package))
        url = "https://abf.io/import/{package}/raw/rosa2019.1/{package}.spec"
        # url = "http://github.com/OpenMandrivaAssociation/{package}/raw/master/{package}.spec".format(package=package)
        resp = requests.get(url, headers=self.headers_)
        
        if resp.status_code == 404:
            return 'requested package [{}] not found'.format(package)
        elif resp.status_code == 200:
            temp = tempfile.NamedTemporaryFile(prefix=package, suffix=".spec")
            spec = resp.content
            
            try:
                spec_path = temp.name
                self.api_.logger.debug("Name of the file is: {}".format(temp.name))
                self.api_.logger.debug("Path to the file is: {}".format(spec_path))
                temp.write(spec)
                temp.seek(0)
                self.get_nvs_(spec_path)
                # name = nvs[0]
                # version = nvs[1]
                # source = nvs[2]
                # source0 = nvs[3]
                self.api_.logger.debug('name:    {}'.format(self.nvs_[0]))
                self.api_.logger.debug('version: {}'.format(self.nvs_[1]))
                self.api_.logger.debug('source:  {}'.format(self.nvs_[2]))
                self.api_.logger.debug('source0: {}'.format(self.nvs_[3]))
                self.nvss_.extend(self.nvs_)
                return self.nvs_[0], self.nvs_[1], self.nvs_[2], self.nvs_[3]
            except Exception as e:
                return 'An error occurred while updating the spec file: {}'.format(e)
            finally:
                temp.close()

    def tryint_(self, x):
        try:
            return int(x)
        except ValueError:
            return x

    def splittedname_(self, s):
        return tuple(self.tryint_(x) for x in re.split('([0-9]+)', s))

    def github_check_(self, upstream_url):

        self.api_.logger.debug('Checking github apstream ...')

        split_url = upstream_url.split("/")[:-1]
        project_url = '/'.join(split_url[:6]) + '/'
        try:
<<<<<<< Updated upstream
            pkg_notcare = re.compile(package+'[-]([\d.]*\d+)', re.IGNORECASE)
            category_match = re.finditer(
                pkg_notcare, req.content.decode('utf-8'))
            for match in category_match:
                version_list.append(match[1])
            upstream_max_version = max(
                [[int(j) for j in i.split(".")] for i in version_list])
            upstream_version = ".".join([str(i) for i in upstream_max_version])
            print(upstream_version, project_url)
            return upstream_version, project_url
        except:
            category_match = re.finditer(
                'href=[\'"]?([\d.]*\d+)', req.content.decode('utf-8'))
            for match in category_match:
                version_list.append(match[1])
            upstream_max_version = max(
                [[int(j) for j in i.split(".")] for i in version_list])
            upstream_version = ".".join([str(i) for i in upstream_max_version])
            print(upstream_version, project_url)
            return upstream_version, project_url


# add here https://download.kde.org/stable/frameworks/


def check_version(package):
    print('checking Rosa-2019.1 ingit version for package [{}]'.format(package))
    url = "https://abf.io/import/{package}/raw/rosa2019.1/{package}.spec".format(package=package)
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
            get_nvs(spec_path)
            name = nvs[0]
            version = nvs[1]
            source = nvs[2]
            source0 = nvs[3]
            #print(name, version, source, source0)
            nvss.extend([name, version, source, source0])
            return name, version, source, source0
=======
            apibase = 'https://api.github.com/repos' + '/' + \
                split_url[3] + '/' + split_url[4] + '/tags'
            self.api_.logger.debug('Api base url: {}'.format(apibase))
            code, data = self.json_request_(apibase, headers=self.github_headers_) 
            
            if code == 404:
                return 'Unable to get response form {}, satus code is: {}'.format(apibase, code), None, None
            
            project_name = (data[0]['name'])
            
            if 'xf86' in project_url:
                category_match = re.search('[-]([\d.]*\d+)', project_name)
                upstream_version = category_match.group(1)
            else:
                category_match = re.search('\d+(?!.*/).*\d+', project_name)
                upstream_version = category_match.group(0)

            return None, upstream_version, project_url
>>>>>>> Stashed changes
        except:
            apibase = 'https://api.github.com/repos' + '/' + \
                split_url[3] + '/' + split_url[4] + '/releases'
            
            code, data = self.json_request_(url=apibase, headers=self.github_headers_)
            
            if code == 404:
                return 'Unable to get response form {}, satus code is: {}'.format(apibase, code), None, None

            project_name = (data[0]['name'])
            category_match = re.search('\d+(?!.*/).*\d+', project_name)
            upstream_version = category_match.group(1)

            return None, upstream_version, project_url

    def kernel_rpi_(self):
        rpi3_raw = 'https://github.com/raspberrypi/linux/raw/rpi-4.19.y/Makefile'
        rpi_page = requests.get(rpi3_raw, headers=github_headers)
        version = re.search('VERSION\s=\s([^"\n]+)', rpi_page.content.decode('utf-8'))
        patchlevel = re.search('PATCHLEVEL\s=\s([^"\n]+)', rpi_page.content.decode('utf-8'))
        sublevel = re.search('SUBLEVEL\s=\s([^"\n]+)', rpi_page.content.decode('utf-8'))
        kernel_version = version.group(1) + '.' +  patchlevel.group(1) + '.' + sublevel.group(1)
        self.api_.logger.debug(kernel_version)
        upstream_url = 'https://github.com/raspberrypi/linux/'
        return kernel_version, upstream_url

    # Checkin upstream version of package
    def check_upstream_(self, package):
        
        upstream_name, our_ver, upstream_url, source0 = self.nvss_
        
        if 'github' in upstream_url:
            self.api_.logger.debug('Checking github upstream ...')
            err, upstream_version, upstream_url = self.github_check_(upstream_url)
            if err is not None:
                self.api_.logger.error(err)

            self.api_.logger.debug('upstream version is [{}]'.format(upstream_version))
            self.api_.logger.debug('upstream url is [{}]'.format(upstream_url))
            self.api_.logger.debug('=========================================')
            return upstream_version, upstream_url
        elif 'qt.io' in upstream_url:
            self.api_.logger.debug('Checking qt5 upstream ...')    
            err, upstream_version, upstream_url = self.qt5_check_(upstream_url)
            if err is not None:
                self.api_.logger.error(err)
                return 1

            self.api_.logger.debug('upstream version is [{}]'.format(upstream_version))
            self.api_.logger.debug('upstream url is [{}]'.format(upstream_url))
            self.api_.logger.debug('=========================================')
        elif 'python' in upstream_name:
            self.api_.logger.debug('Checking python upstream ...')
            err, upstream_version, upstream_url, archive = self.check_python_module_(package)
            if err is not None:
                self.api_.logger.error(err)
                return 1

            self.api_.logger.debug('upstream version is [{}]'.format(upstream_version))
            self.api_.logger.debug('upstream archive is [{}]'.format(archive))
            self.api_.logger.debug('=========================================')
            return upstream_version, upstream_url, archive
        elif 'rust' in upstream_name:
            self.api_.logger.debug('Checking rust upstream ...')
            err, upstream_version, url = self.check_rust_module_(package)
            if err is not None:
                self.api_.logger.error(err)
                return 1

            self.api_.logger.debug('upstream version is [{}]'.format(upstream_version))
            self.api_.logger.debug('upstream url is [{}]'.format(url))
            self.api_.logger.debug('=========================================')
            return upstream_version, upstream_url
        # add perl here
        # https://fastapi.metacpan.org/release/Class-Spiffy
        elif package == 'kernel-rpi3':
            upstream_version, upstream_url = self.kernel_rpi_()
            return upstream_version, upstream_url
        else:
            self.api_.logger.debug('any other')
            return repology(package)

    def compare_versions_(self, package):
        self.api_.logger.debug('Comparing package version ...')
        name, omv_version, url, source0 = self.nvss_
        self.api_.logger.debug('name: {}'.format(name))
        self.api_.logger.debug('omv_version: {}'.format(omv_version))
        self.api_.logger.debug('url: {}'.format(url))
        self.api_.logger.debug('source0: {}'.format(source0))

        upstream_ver, upstream_url, *archive = self.check_upstream_(package)
        self.api_.logger.debug(upstream_url)

        if len(archive) == 1:
            archive = archive[0]
        else:
            archive = None

        package_item = {
            'package': package,
            'omv_version': omv_version,
            'upstream_version': upstream_ver,
            'project_url': upstream_url
        }

        if archive is not None:
            package_item['archive'] = archive
        if self.splittedname_(omv_version) == self.splittedname_(upstream_ver):
            package_item['status'] = 'updated'
        if self.splittedname_(omv_version) < self.splittedname_(upstream_ver):
            package_item['status'] = 'outdated'
        if self.splittedname_(omv_version) > self.splittedname_(upstream_ver):
            package_item['status'] = 'unknown'
        return package_item

    def clone_repo_(self, package, project_version):
        self.remove_if_exist_(home + '/' + package)
        tries = 5
        # git_repo = 'git@github.com:OpenMandrivaAssociation/{}.git'.format(package)
        # git_repo = 'https://github.com/OpenMandrivaAssociation/{}.git'.format(package)
        git_repo = 'https://abf.io/olegsolovev/{}.git'.format(package)
        for i in range(tries):
            try:
                self.api_.logger.debug('cloning [{}], branch: [{}] to [{}]'.format(git_repo, project_version, home + '/' + package))
                subprocess.check_output(['/usr/bin/git', 'clone', '-b', self.project_version_, '--depth', '100', git_repo, package], cwd = home)
            except subprocess.CalledProcessError as e:
                if i < tries - 1:
                    time.sleep(5)
                    continue
                else:
                    return 'Unable to clone {} github repo: {}'.format(git_repo, e)
            break

        return None

    def remove_if_exist_(self, path):
        if os.path.exists(path):
            if os.path.isdir(path):
                try:
                    subprocess.check_output(
                        ['rm', '-rf', path])
                except subprocess.CalledProcessError as e:
                    self.api_.logger.debug(e.output)
                    return
            elif os.path.isfile(path):
                try:
                    subprocess.check_output(
                        ['rm', '-f', path])
                except subprocess.CalledProcessError as e:
                    self.api_.logger.debug(e.output)
                    return

    def lint_version_(self, version):
        return re.search('[a-zA-Z]', version) is not None

    def git_commit_(self, message, package):
        try:
            subprocess.check_call(['git', 'commit', '-am', '{}'.format(message)], cwd = home + '/' + package)
        except subprocess.CalledProcessError as e:
            sys.exit(1)
            self.api_.logger.debug(e)

    def git_push_(self, package):
        try:
            subprocess.check_call(['git', 'push'], cwd = home + '/' + package)
        except subprocess.CalledProcessError as e:
            sys.exit(1)
            self.api_.logger.debug(e)

    def upload_sources_(self, package):
        abf_yml = home + '/' + package + '/' + '.abf.yml'
        self.remove_if_exist_(abf_yml)
        try:
            subprocess.check_call(['abf', 'put'], cwd = home + '/' + package)
        except subprocess.CalledProcessError as e:
            print_log('uploading sources [{}] failed'.format(package), 'update.log')
            self.api_.logger.debug(e)

    def abf_build_(self, package):
        try:
            subprocess.check_call(['abf', 'chain_build', '-b', 'master', '--no-cached-chroot', '--auto-publish', '--update-type', 'enhancement', 'openmandriva/{}'.format(package)], cwd = home + '/' + package)
        except subprocess.CalledProcessError as e:
            print_log('abf build [{}] failed'.format(package), 'update.log')
            self.api_.logger.debug(e)
            return False

    def qt5_check_(self, upstream_url):
        split_url = upstream_url.split("/")[:6]
        project_url = '/'.join(split_url[:5])
        self.api_.logger.debug('upstream url: {}'.format(upstream_url))
        req = requests.get(project_url, headers=headers, allow_redirects=True)
        version_list = []
        # http://download.qt.io/official_releases/qt/5.11/
        true_version_list = []
        if req.status_code == 404:
            # self.api_.logger.debug('requested url [{}] not found'.format(upstream_url))
            return 'requested url [{}] not found'.format(upstream_url), None, None
        if req.status_code == 200:
            try:
                first_url = re.finditer(
                    'href=[\'"]?([\d.]*\d+)', req.content.decode('utf-8'))
                for match in first_url:
                    version_list.append(match[1])
                upstream_max_version = max(
                    [[int(j) for j in i.split(".")] for i in version_list])
                upstream_version = ".".join([str(i) for i in upstream_max_version])
                new_url = project_url + '/' + upstream_version
                self.api_.logger.debug(new_url)
                req2 = requests.get(new_url, headers=headers, allow_redirects=True)
                if req2.status_code == 404:
                    return 'requested url [{}] not found'.format(new_url), None, None
                if req2.status_code == 200:
                    try:
                        pkg_ver = re.finditer(
                            'href=[\'"]?([\d.]*\d+)', req2.content.decode('utf-8'))
                        for match in pkg_ver:
                            true_version_list.append(match[1])
                        upstream_max_version = max(
                            [[int(j) for j in i.split(".")] for i in true_version_list])
                        upstream_version = ".".join(
                            [str(i) for i in upstream_max_version])
                        self.api_.logger.debug(upstream_version)
                        return None, upstream_version, project_url
                    except Exception as e:
                        return 'Unable to check qt5 upstream: {}'.format(e), None, None
            except Exception as e:
                return 'Unable to check qt5 upstream: {}'.format(e), None, None

    def update_spec_(self, package):
        pkg_info = self.compare_versions_(package)
        self.api_.logger.debug('Package info: {}'.format(pkg_info))
        status = pkg_info['status']
        upstream_version = pkg_info['upstream_version']
        omv_version = pkg_info['omv_version']
        if 'archive' in pkg_info:
            new_source0 = pkg_info['archive']
            self.api_.logger.debug('New source: {}'.format(new_source0))
        else:
            new_source0 = None
        output = '/tmp/' + package + '.spec'
        self.remove_if_exist_(output)
        try:
            if self.lint_version_(upstream_version) is False and status == 'outdated':
                self.api_.logger.debug('linting passed')
                self.api_.logger.debug('update required')
                # find current version
                err = self.clone_repo_(package, project_version)

                if err is not None:
                    return err

                # Update verisol
                self.api_.logger.debug('Try to update version ...')
                version_pattern = 'Version:\w*(.*)'
                specname = self.home_ + '/' + package + '/' + package + '.spec'
                with open(specname) as f:
                    for line in f:
                        change_version = re.sub(version_pattern, 'Version:\t' + upstream_version, line)
                        with open(output, 'a') as outfile:
                            outfile.write(change_version)
                    target_spec = self.home_ + '/' + package + '/' + package + '.spec'
                    shutil.move(output, target_spec)

                # Increment release number
                self.api_.logger.debug('Try to increment release number ...')
                with open(specname) as f:
                    for line in f:
                        release_pattern = 'Release:\W(.*)'
                        change_release = re.sub(release_pattern, 'Release:\t' + '1', line)
                        with open(output, 'a') as outfile:
                            outfile.write(change_release)
                    target_spec = home + '/' + package + '/' + package + '.spec'
                    shutil.move(output, target_spec)

                # related to python packages
                if new_source0 is not None:
                    source_pattern = 'Source0:\W*(.*)'
                    with open(specname) as f:
                        for line in f:
                            change_source = re.sub(source_pattern, 'Source0:\t' + new_source0, line)
                            with open(output, 'a') as outfile:
                                outfile.write(change_source)
                        target_spec = self.home_ + '/' + package + '/' + package + '.spec'
                        shutil.move(output, target_spec)

                # Local mock
                # build_error, build_state = self.run_local_builder_(package, project_version, omv_version, upstream_version)

                # if build_state is False or build_state is None:
                #     return build_error

                # self.upload_sources_(package)
                self.git_commit_('version autoupdate [{}]'.format(upstream_version), package)
                self.git_push_(package)
                # self.abf_build_(package)
        except Exception as e:
            self.api_.logger.error('Unable to update spec: {}'.format(e))
            return 'Unable to update spec: {}'.format(e)

    def print_log_(self, message, log):
        self.api_.logger.debug(message)
        try:
            logFile = open(log, 'a')
            logFile.write(message + '\n')
            logFile.close()
        except:
            self.api_.logger.debug("Can't write to log file: " + log)

    def run_local_builder_(self, package, project_version, omv_version, upstream_version):
        if package == 'kernel-rpi3':
            return None, True

        try:
            self.api_.logger.debug('run local build with abf tool')
            subprocess.check_call(['spectool', '--get-files', package + '.spec'], cwd = home + '/' + package)
            subprocess.check_call(['abf', 'mock'], cwd = home + '/' + package)
        except subprocess.CalledProcessError as e:
            self.print_log_('local build [{}] failed, omv_version: {} upstream: {} error: {}'.format(package, omv_version, upstream_version, e), 'update.log')
            return 'local build [{}] failed, omv_version: {} upstream: {} error: {}'.format(package, omv_version, upstream_version, e), False
        
        self.print_log_('{} update successfull from {} to {}'.format(package, omv_version, upstream_version), 'update.log')
        return None, True

    def update_packages(self):
        content = request.json
        packages = [i for i in content['packages'] if i is not None]

        for package in packages:
            # clear lists
<<<<<<< Updated upstream
            del nvss[:]
            del nvs[:]
            check_version(package)
            #try:
            print('update_spec')
            update_spec(package)
            #except:
            #    pass
=======
            del self.nvss_[:]
            del self.nvs_[:]

            self.api_.logger.debug('Checjing version of packge ...')
            err = self.check_version_(package)
            if err is not None and type(err) is str:
                return jsonify({"error": err}), 409
            
            self.api_.logger.debug('Updating package ...')
            err = self.update_spec_(package)
            if err is not None:
                return jsonify({"status": "error", "message": err}), 409
            
        return jsonify({"message": "Packages {} updated successfully!".format(packages),
            "version": 8}), 200

    def update_packages_by_file(self):
        pass

    def test(self):
        content = request.json
        self.api_.logger.debug(content)
        return {
            "vsem" : "moim",
            "brat'yam" : "SALAAAM",  
        }

    def test_post(self):
        content = request.json
        if not content["packages"]: 
            return ":("

        packages = [i for i in content["packages"] if i is not None and i != ""]

        print(packages)

        return packages
    
    def run(self):
        
        self.api_.run(host = self.adress_,port = self.port_, debug=True)

pws = PackageWorker()
>>>>>>> Stashed changes
