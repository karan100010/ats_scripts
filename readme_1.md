## Step to run start.py file

# Table of Contents

- ## [Setup Python](#setup-python-1)
- ## [Setup OpenSSL](#setup-openssl-1)
- ## [Install Python](#install-python-1)

# Setup Python

## 1. Installing Python 3.11 on CentOS 7
## Update System

This is recommended but an optional step. If you have other applications running on the system and afraid of dependencies breaking you can skip this step.

'sudo yum -y update'

After a successful update let’s reboot the system.

'sudo systemctl reboot'

## 2. Install Python 3.11 build tools
'sudo yum -y install epel-release'
'sudo yum install wget make cmake gcc bzip2-devel libffi-devel zlib-devel'

All Development Tools can be installed from package group with the commands below:

'sudo yum -y groupinstall "Development Tools"'

## 3. Confirm GCC version:
gcc --version

## 4. Install OpenSSL 1.1 on CentOS 7 =====================================================================================
To Install OpenSSL, Go through the table of Content then Install Python

# Install Python

## 5. Install Python 3.11 on CentOS 7

## After installing OpenSSL 1.1.1, verify by checking the version:
'openssl version'
OpenSSL 1.1.1t  7 Feb 2023

After installing OpenSSL 1.1.1, verify by checking the version:

## Download Python 3.11 source:
'wget https://www.python.org/ftp/python/3.11.4/Python-3.11.4.tgz'

## Extract downloaded archive
'tar xvf Python-3.11.4.tgz'

## Navigate into created directory
'cd Python-3.11*/'

## Configure the build
'LDFLAGS="${LDFLAGS} -Wl,-rpath=/usr/local/openssl/lib" ./configure --with-openssl=/usr/local/openssl'

## Make and install Python 3.11
'make'

'sudo make altinstall'

## Check Python version
'python3.11 --version'
Python 3.11.4

## Verify OpenSSL libs work
'python3.11'

## Import ssl module and check OpenSSL version
>>> import ssl
>>> ssl.OPENSSL_VERSION
'OpenSSL 1.1.1t  7 Feb 2023'

## Use exit() or Ctrl-D to exit
>>> Ctrl-D

## 6. Install Python modules using Pip3.11
## Check Pip version
'pip3.11 --version'
pip 22.3.1 from /usr/local/lib/python3.11/site-packages/pip (python 3.11)

## Upgrade Pip to the latest release
'pip3.11 install --upgrade pip'

## Install Python modules using Pip
'sudo pip3.11 install <module-name>'









# Setup OpenSSL

## Installing OpenSSL 1.1.x on CentOS 7

The version of OpenSSL available on CentOS 7 operating system is a bit old and some applications will give errors when compiling if it requires a newer release.

'sudo yum -y install openssl openssl-devel'

'openssl version'

OpenSSL 1.0.2k-fips  26 Jan 2017
As seen from the output the version available is 1.0.2. If installed remove it before you proceed.

## Prerequisites

Before installing OpenSSL 1.1.x, it's recommended to remove any existing versions:

'sudo yum -y remove openssl openssl-devel'

## Confirm the uninstallation:
'openssl version'
-bash: openssl: command not found

If the above command returns a "command not found" error, you're ready to proceed.

## Installation Steps

## 1.Install dependencies required for building OpenSSL:
'sudo yum -y groupinstall "Development Tools"'

## 2.Download the source code for OpenSSL 1.1.x:
'wget https://www.openssl.org/source/openssl-1.1.1w.tar.gz'

## Extract the downloaded file:
'tar xvf openssl-1.1.1w.tar.gz'

## Navigate to directory created from file extraction.
'cd openssl-1.1*/'

## 3. Configure OpenSSL with a specified prefix and openssldir:
'./config --prefix=/usr/local/openssl --openssldir=/usr/local/openssl'

## 4.Build OpenSSL using the make command:
'make'

## 5. Install OpenSSL 1.1.1:
'sudo make install'

## Update the shared libraries cache:
'sudo ldconfig'

## Update the system-wide OpenSSL configuration:
'sudo tee /etc/profile.d/openssl.sh <<EOF
export PATH=/usr/local/openssl/bin:\$PATH
export LD_LIBRARY_PATH=/usr/local/openssl lib:\$LD_LIBRARY_PATH
EOF'

## Reload the shell environment:
'source ~/.bash_profile'

Log out of the current shell session and log in again.

'logout'

## 6. Verify that OpenSSL 1.1.1 is installed:

'which openssl'

Output:
/usr/local/openssl/bin/openssl

'openssl version'

Output indicate the new version:
OpenSSL 1.1.1w  11 Sep 2023

##