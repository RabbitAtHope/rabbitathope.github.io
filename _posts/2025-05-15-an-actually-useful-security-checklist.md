---
layout: post
title: The Actually Useful Security Checklist
subtitle: A security checklist you can actually use
cover-img: /assets/img/avatar.png
thumbnail-img: /assets/img/avatar.png
share-img: /assets/img/avatar.png
tags: [checklist, security]
category: Checklists
toc: true
---

This checklist is a personal reference tool for me, as well as a useful tool if you got a penetration test report saying vague stuff like "secure configuration" and "hardening" and you want to actually find out what to type into your keyboard.

---

# 🗄️ Servers

---

---

## 🔧 <span class='highlight'>Operating Systems</span>

---

<details markdown="1">
<summary>Expand...</summary>

The most basic, bread-and-butter starting point and the first step to harden a server is to make sure its operating system and packages are up to date and currently supported. Running only supported operating systems is the bare minimum requirement for having a secure server network.

{: .box-error}
⛔ If you're running unsupported operating systems, you are **actively accepting the risks and vulnerabilities associated with it**. However, realistically, there are always going to be those random outdated systems that are absolutely necessary for some business process to run, or that can't be brought up for one reason or another. Ideally, those servers should be taken off the public Internet and only be accessible internally while you work on upgrading or replacing them.

- **Packages**: Linux server installations will come with a package manager, i.e. `apt` or `yum`, and package updates can be applied to the server by running `apt update` / `apt upgrade` or `yum update` regularly. I personally use a maintenance script on our Ubuntu servers that runs both `apt update` / `apt upgrade` and `apt autoclean` / `apt autoremove` to also clean up obsolete or unnecessary packages. There are also open-source solutions (i.e. Ansible) and commercial RMMs (i.e. Atera, Kaseya, NinjaOne, Ubuntu Pro) that allow you to remotely manage packages and update them.
- **Operating System**: If you need to upgrade an unsupported Linux operating system or kernel to a supported version, Ubuntu LTS provides `apt dist-upgrade` and `do-release-upgrade`, and other Linux server distributions have similar commands and procedures.

</details>

---

## 🔧 <span class='highlight'>Services</span>

---

<details markdown="1">
<summary>Expand...</summary>

The specific configuration changes listed below should be applied to any services that a server, well, serves - whether that service is internal-only or externally facing. These configuration changes are extremely common findings in penetration tests that use Nessus scanners and other misconfiguration/vulnerability scanners.

---

## 🗄️ <span class='highlight'>Services</span>: <span class='highlight-green'>Database Services</span>

<details markdown="1">
<summary>Expand...</summary>

---

### 🗄️ <span class='highlight'>Services</span>: <span class='highlight-green'>Database Services</span>: MariaDB

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **3306***

</details>

---

### 🗄️ <span class='highlight'>Services</span>: <span class='highlight-green'>Database Services</span>: MySQL

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **3306***

The best way to quickly harden a MySQL installation is to run the built-in `mysql_secure_installation` script and follow all the instructions it gives you, but manual hardening steps are provided below.

#### 📌 Disable Remote Root Login

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
sudo mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host!='localhost'; FLUSH PRIVILEGES;"
```

</details>

#### 📌 Remove Anonymous Accounts

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
mysql -u root -p

SELECT User, Host FROM mysql.user WHERE User = '';

DELETE FROM mysql.user WHERE User = '';

FLUSH PRIVILEGES;

exit;
```

</details>

#### 📌 Set Strong Root Password

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
sudo mysql

ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '{password}';
FLUSH PRIVILEGES;

exit;
```

</details>

</details>

</details>

---

## 🔒 <span class='highlight'>Services</span>: <span class='highlight-green'>Secure Shell Services</span>

<details markdown="1">
<summary>Expand...</summary>

---

### 🔒 <span class='highlight'>Services</span>: <span class='highlight-green'>Secure Shell Services</span>: OpenSSH Server

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Package Name(s): **openssh-server** (apt)*<br>*Common Port(s): <strong>22</strong> (SSH)*

Unless otherwise stated, most of the configuration changes below will require you to reload or restart the service to fully apply them.

#### 📌 Disable Insecure Ciphers

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/ssh/sshd_config

MACs hmac-sha2-256,hmac-sha2-512,umac-64-etm@openssh.com,umac-128-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,chacha20-poly1305@openssh.com
```

</details>

#### 📌 Disable Root Login

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/ssh/sshd_config

PermitRootLogin no
```

</details>

#### 📌 Enforce Strong Passwords

<details markdown="1">
<summary>Expand...</summary>

You can enforce strong SSH passwords using PAM.

##### 🐧 Debian/Ubuntu:

Install the PAM package:

```console
apt install libpam-pwquality
```

Then enable PAM in the SSH configuration file:

```console
(editor) /etc/ssh/sshd_config

UsePAM yes
PasswordAuthentication yes
```

Then set your password requirements in the PAM configuration file:

```console
(editor) /etc/pam.d/common-password

password requisite pam_pwquality.so retry=3 minlen={minimum length} ucredit=-{number of uppercase letters} lcredit=-{number of lowercase letters} dcredit=-{number of digits} ocredit=-{number of special characters}
```

Make sure the settings also match in this configuration file:

```console
(editor) /etc/security/pwquality.conf

minlen = {minimum length}
ucredit = -{number of uppercase letters}
lcredit = -{number of lowercase letters}
dcredit = -{number of digits}
ocredit = -{number of special characters}
```

You can also block common passwords like this:

```console
(editor) /etc/pam.d/common-password

password requisite ... dictcheck=1 (add to the end of the existing line)
```

```console
(editor) /etc/security/pwquality.conf

dictcheck = 1
dictpath = /usr/share/dict/cracklib-small (or a custom wordlist you made)
```

Some recommended "bad passwords" to block if you make a custom wordlist are:

```console
1234
123456
admin
letmein
password
qwerty
```

{: .box-success}
✅ **Verification**: Change a user's password with passwd (sudo passwd {user}) and verify that you can't set a password that does not conform to the configured requirements.

</details>

#### 📌 Whitelist Access

<details markdown="1">
<summary>Expand...</summary>

The OpenSSH service should only be accessible to a limited range of IP addresses, ideally off a whitelist that is enforced by the local firewall and/or by the OpenSSH service configuration file. You can use the `AllowUsers` and `AllowGroups` directives to make access as granular as possible.

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/ssh/sshd_config

Match Address {ip,ip,ip...}
    AllowUsers {user} {user} {user}...
```

</details>

</details>

</details>

---

## 🌎 <span class='highlight'>Services</span>: <span class='highlight-green'>Web Services</span>

<details markdown="1">
<summary>Expand...</summary>

---

### 🌎 <span class='highlight'>Services</span>: <span class='highlight-green'>Web Services</span>: Apache HTTP

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Package Name(s): **apache2** (apt), **httpd** (yum)*<br>*Common Port(s): <strong>80</strong> (HTTP), <strong>443</strong> (HTTPS), <strong>8080</strong> (Alternate HTTP), <strong>8443</strong> (Alternate HTTPS)*

Unless otherwise stated, most of the Apache configuration changes below will require you to reload or restart Apache to fully apply them, i.e.:

```console
service apache2 restart

systemctl restart apache2
```

File locations may also vary depending on how you set up your web server. You may also need to install or enable certain modules (**mod_headers**, **mod_rewrite**, **mod_status**) using `a2enmod` where needed.

#### 📌 Disable SSLv2/SSLv3/TLSv1/TLSv1.1

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(ssl config files)

SSLProtocol all -SSLv3 -SSLv2 -TLSv1 -TLSv1.1
```

{: .box-success}
✅ **Verification**: Use nmap with the <a href="https://nmap.org/nsedoc/scripts/ssl-enum-ciphers.html">ssl-enum-ciphers</a> script to scan open HTTP/HTTPS ports (usually 80/443) and verify that these ciphers don't appear in the response.

</details>

#### 📌 Disable TRACE

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/conf-enabled/security.conf

TraceEnable Off
```

{: .box-success}
✅ **Verification**: Use nmap with the <a href="https://nmap.org/nsedoc/scripts/http-methods.html">http-methods</a> script to scan open HTTP/HTTPS ports (usually 80/443) and verify that the TRACE method doesn't appear in the list of supported methods.

</details>

#### 📌 Enable Custom Error Page

<details markdown="1">
<summary>Expand...</summary>

The default Apache error page exposes version information and shows exactly what version and build of Apache you have on your server. To conceal this information, you should create a custom error page and set it as the default error page for 403 Forbidden, 404 Not Found, etc. in the Apache configuration file.

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(config files)

ErrorDocument 403 {file}
ErrorDocument 404 {file}
```

{: .box-success}
✅ **Verification**: Browse to a nonexistent directory and verify that you get the custom error page.

</details>

#### 📌 Hide Server Information

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/conf-enabled/security.conf

ServerSignature Off
ServerTokens Prod
```

{: .box-success}
✅ **Verification**: Use nmap with the service detection flag (`-sV`) to scan open HTTP/HTTPS ports (usually 80/443) and verify that the banner grab shows "Apache" instead of "Apache x.x.x".

</details>

#### 📌 Remove Unnecessary Files/Directories

<details markdown="1">
<summary>Expand...</summary>

Remove or conceal the following **dotfile** (hidden by default on Linux unless listed with `ls -la`) directories and files from `/var/www/html` (or whichever file location is tied to your web server setup):
- `.cache`
- `.config`
- `.env` (can leak hardcoded secrets)
- `.eslintrc`
- `.git` (can leak hardcoded secrets)
  - `/config` (can leak hardcoded secrets)
- `.gitattributes`
- `.github`
- `.gitignore`
- `.gitinfo`
- `.gitmodules`
- `.gnupg` (contains PGP information)
- `.jshintrc`
- `.nvmrc`
- `.travis.yml`
- `.viminfo`

Remove or conceal the following other directories and files:
- `composer.json`
- `composer.lock`
- `docker-compose.yml` (exposes Docker configuration information and services)
- `Gruntfile.js`
- `npm-shrinkwrap.json` (exposes dependencies and version information)
- `package.json` (exposes dependencies and version information)
- `phpinfo` (exposes PHP version information)
- `phpinfo.php` (exposes PHP version information)

If desired, you can entirely block specific sensitive file types from being browsed in `/etc/apache2/conf-enabled/security.conf` (or wherever your Apache configuration files are):

```console
RedirectMatch 404 /\.git
RedirectMatch 404 /\.svn
```

{: .box-success}
✅ **Verification**: Browse to these directories and files in any web browser and verify that you receive either a 403 Forbidden or a 404 Not Found response. You can also use curl.

</details>

#### 📌 <span class='highlight'>mod_headers</span>: Enforce HTTP Strict Transport Security (HSTS) Header

<details markdown="1">
<summary>Expand...</summary>
The maximum age value can vary depending on your preferences, but the default value of 31536000 I usually use has never caused any issues.

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(config files)

Header always set Strict-Transport-Security max-age=31536000
```

{: .box-success}
✅ **Verification**: Browse to the site and verify that you receive a Strict-Transport-Security header in the HTTP response, and that it has the configured age value. You can see it using your web browser's Developer Tools (Network -> Headers), or through nmap and other header grabber tools.

</details>

#### 📌 <span class='highlight'>mod_rewrite</span>: Enforce HTTP To HTTPS Rewrite

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(config files)

RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}/$1 [R=301,L]
```

</details>

#### 📌 <span class='highlight'>mod_status</span>: Restrict Access To Server Status Page

<details markdown="1">
<summary>Expand...</summary>

##### 🐧 Debian/Ubuntu:

```console
(editor) /etc/apache2/mods-enabled/status.conf

<Location /server-status>
    SetHandler server-status
    Require local
    Require ip {ip ip ip...}
</Location>
```

</details>

</details>

---

### 🌎 <span class='highlight'>Services</span>: <span class='highlight-green'>Web Services</span>: Apache Tomcat

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **80** (HTTP), **443** (HTTPS), **8080** (Alternate HTTP), **8443** (Alternate HTTPS)*

Unless otherwise stated, you will usually have to run the Tomcat shutdown and startup scripts (or restart the service if it's configured as one) to fully apply these changes.

`$CATALINA_HOME` on most installations is something like `/home/tomcat/` or `/opt/tomcat/` (Debian/Ubuntu). If you need to manually tell the server where it is, you can do it like this:

```console
export CATALINA_HOME={directory}
```

#### 📌 Restrict Access To Manager Application

<details markdown="1">
<summary>Expand...</summary>

The `context.xml` file controls access to the Manager Application that comes bundled with Tomcat. You will usually want to restrict this to only localhost access (127.0.0.1).

##### 🐧 Debian/Ubuntu:

```console
(editor) $CATALINA_HOME/webapps/manager/META-INF/context.xml

<Context antiResourceLocking="false" privileged="true">
    <Valve className="org.apache.catalina.valves.RemoteAddrValve"
           allow="127\.\d+\.\d+\.\d+|::1" />
</Context>
```

If you want to also allow a specific IP address, i.e. **[1].[2].[3].[4]**, format it like **[1]\\.[2]\\.[3]\\.[4]** and add it to the allow statement with an "or" operator (`|`).

You can also configure a login requirement and a specific user that is authorized to view the page after entering a password:

```console
(editor) $CATALINA_HOME/conf/tomcat-users.xml

<tomcat-users>
  <user username="admin" password="{password}" roles="manager-gui"/>
</tomcat-users>

```

{: .box-success}
✅ **Verification**: Browse to `/manager/html` on your site and verify that you get a 403 Access Denied error page if you are not on the whitelist.

</details>

</details>

---

### 🌎 <span class='highlight'>Services</span>: <span class='highlight-green'>Web Services</span>: PHP

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **80** (HTTP), **443** (HTTPS), **8080** (Alternate HTTP), **8443** (Alternate HTTPS)*

</details>

</details>

---

</details>

---

# 🧩 Software

---

This section applies to any software that is not a service being provided by a server (for that, see the first section) and is instead commercially produced user-facing, customer-facing, client-facing, or enterprise software with a user interface that is sold by a vendor and receives patching and support from said vendor, i.e. Office 365, Teams, Zoom, etc.

Most modern security frameworks, such as NIST (SP 800-171 Control 3.4.8), require **software whitelisting** on workstations as part of your overall posture - that is, controlling what programs employees can install on their laptops and not allowing the installation of unknown or blacklisted programs. As such, this section will focus on common enterprise software and the policies, usage requirements, and configuration you should have for that software in your organization, as well as how to set up and manage updates and patching where needed.

<details markdown="1">
<summary>Expand...</summary>

---

## Something here...

---

</details>

---

# 🖥️ Workstations

---

This section covers posture management and configuration management concerns for employee workstations (i.e. laptops and computers) outside of software (for that, see the previous section).

<details markdown="1">
<summary>Expand...</summary>

---

## 🪟 Windows

---

## 🐧 Linux

---

</details>