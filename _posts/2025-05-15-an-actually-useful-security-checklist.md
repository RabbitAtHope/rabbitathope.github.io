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

# 🗄️ Database Services

---

## 🗄️ MariaDB

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **3306***

</details>

---

## 🗄️ MySQL

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **3306***

</details>

---

# 🔒 Secure Shell (SSH) Services

---

## 🔒 OpenSSH Server

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Package Name(s): **openssh-server** (apt)*<br>*Common Port(s): <strong>22</strong> (SSH)*

Unless otherwise stated, most of the configuration changes below will require you to reload or restart the service to fully apply them.

### 📌 Disable Insecure Ciphers

<details markdown="1">
<summary>Expand...</summary>

#### Debian/Ubuntu:

```console
(editor) /etc/ssh/sshd_config

MACs hmac-sha2-256,hmac-sha2-512,umac-64-etm@openssh.com,umac-128-etm@openssh.com
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers aes256-gcm@openssh.com,aes128-gcm@openssh.com,chacha20-poly1305@openssh.com
```

</details>

### 📌 Disable Root Login

<details markdown="1">
<summary>Expand...</summary>

```console
(editor) /etc/ssh/sshd_config

PermitRootLogin no
```

</details>

### 📌 Enforce Strong Passwords

<details markdown="1">
<summary>Expand...</summary>

You can enforce strong SSH passwords using PAM.

First, install the PAM package:

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

### 📌 Whitelist Access

<details markdown="1">
<summary>Expand...</summary>

The OpenSSH service should only be accessible to a limited range of IP addresses, ideally off a whitelist that is enforced by the local firewall and/or by the OpenSSH service configuration file. You can use the `AllowUsers` and `AllowGroups` directives to make access as granular as possible.

#### Debian/Ubuntu:

```console
(editor) /etc/ssh/sshd_config

Match Address {ip,ip,ip...}
    AllowUsers {user} {user} {user}...
```

</details>

</details>

---

# 🌎 Web (HTTP/HTTPS) Services

---

## 🌎 Apache HTTP

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Package Name(s): **apache2** (apt), **httpd** (yum)*<br>*Common Port(s): <strong>80</strong> (HTTP), <strong>443</strong> (HTTPS), <strong>8080</strong> (Alternate HTTP), <strong>8443</strong> (Alternate HTTPS)*

Unless otherwise stated, most of the Apache configuration changes below will require you to reload or restart Apache to fully apply them, i.e.:

```console
service apache2 restart

systemctl restart apache2
```

File locations may also vary depending on how you set up your web server.

### 📌 Disable SSLv2/SSLv3/TLSv1/TLSv1.1

<details markdown="1">
<summary>Expand...</summary>

#### Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(ssl config file)

SSLProtocol all -SSLv3 -SSLv2 -TLSv1 -TLSv1.1
```

</details>

### 📌 Disable TRACE

<details markdown="1">
<summary>Expand...</summary>

#### Debian/Ubuntu:

```console
(editor) /etc/apache2/conf-enabled/security.conf

TraceEnable Off
```

{: .box-success}
✅ **Verification**: Use nmap with the <a href="https://nmap.org/nsedoc/scripts/http-methods.html">http-methods</a> script to scan open HTTP/HTTPS ports (usually 80/443) and verify that the TRACE method doesn't appear in the list of supported methods.

</details>

### 📌 Enforce HTTP Strict Transport Security (HSTS)

<details markdown="1">
<summary>Expand...</summary>
The maximum age value can vary depending on your preferences, but the default value of 31536000 I usually use has never caused any issues.

#### Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(config files)

Header always set Strict-Transport-Security max-age=31536000
```

{: .box-success}
✅ **Verification**: Browse to the site and verify that you receive a Strict-Transport-Security header in the HTTP response, and that it has the configured age value. You can see it using your web browser's Developer Tools (Network -> Headers), or through nmap and other header grabber tools.

</details>

### 📌 Hide Server Information

<details markdown="1">
<summary>Expand...</summary>

#### Debian/Ubuntu:

```console
(editor) /etc/apache2/conf-enabled/security.conf

ServerSignature Off
ServerTokens Prod
```

{: .box-success}
✅ **Verification**: Use nmap with the service detection flag (`-sV`) to scan open HTTP/HTTPS ports (usually 80/443) and verify that the banner grab shows "Apache" instead of "Apache x.x.x".

</details>

### 📌 Remove Unnecessary Files/Directories

<details markdown="1">
<summary>Expand...</summary>
Remove or conceal the following directories and files from `/var/www/html` (or whichever file location is tied to your web server setup):
- `.config`
- `.env` (can leak hardcoded secrets)
- `.git` (can leak hardcoded secrets)
- `.gitattributes`
- `.github`
- `.gitignore`
- `.gitinfo`
- `.viminfo`
- `phpinfo` (can expose PHP version information)
- `phpinfo.php` (can expose PHP version information)

If desired, you can entirely block specific sensitive file types from being browsed in `/etc/apache2/conf-enabled/security.conf` (or wherever your Apache configuration files are):

```console
RedirectMatch 404 /\.git
RedirectMatch 404 /\.svn
```

{: .box-success}
✅ **Verification**: Browse to these directories and files in any web browser and verify that you receive either a 403 Forbidden or a 404 Not Found response. You can also use curl.

</details>

### 📌 <span class='highlight'>mod_status</span>: Restrict Access To Server Status Page

<details markdown="1">
<summary>Expand...</summary>

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

## 🌎 Apache Tomcat

<details markdown="1">
<summary>Expand...</summary>

{: .box-note}
*Common Port(s): **80** (HTTP), **443** (HTTPS), **8080** (Alternate HTTP), **8443** (Alternate HTTPS)*

Unless otherwise stated, you will usually have to run the Tomcat shutdown and startup scripts (or restart the service if it's configured as one) to fully apply these changes.

`$CATALINA_HOME` on most installations is something like `/home/tomcat/` or `/opt/tomcat/` (Debian/Ubuntu). If you need to manually tell the server where it is, you can do it like this:

```console
export CATALINA_HOME={directory}
```

### 📌 Restrict Access To Manager Application

<details markdown="1">
<summary>Expand...</summary>

The `context.xml` file controls access to the Manager Application that comes bundled with Tomcat. You will usually want to restrict this to only localhost access (127.0.0.1).

#### Debian/Ubuntu:

```console
(editor) $CATALINA_HOME/webapps/manager/META-INF/context.xml

<Context antiResourceLocking="false" privileged="true">
    <Valve className="org.apache.catalina.valves.RemoteAddrValve"
           allow="127\.\d+\.\d+\.\d+|::1" />
</Context>
```

If you want to also allow a specific IP address, i.e. **[1].[2].[3].[4]**, format it like **[1]\\.[2]\\.[3]\\.[4]** and add it to the allow statement with an "or" operator (`|`).

</details>

</details>

---