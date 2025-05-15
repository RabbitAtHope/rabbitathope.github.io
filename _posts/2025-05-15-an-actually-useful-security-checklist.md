---
layout: post
title: The Actually Useful Security Checklist
subtitle: A security checklist you can actually use
cover-img: /assets/img/avatar.png
thumbnail-img: /assets/img/avatar.png
share-img: /assets/img/avatar.png
tags: [checklist, security]
category: Checklists
---

This checklist is a personal reference tool for me, as well as a useful tool if you got a penetration test report saying vague stuff like "secure configuration" and "hardening" and you want to actually find out what to type into your keyboard.

---

## 🔒 Secure Shell (SSH) Services: OpenSSH Server

<details markdown="1">
<summary>Expand...</summary>
{: .box-note}
*Package Name(s): openssh-server*<br>*Common Port(s): <strong>22</strong> (SSH)*
</details>

---

## 🌎 Web (HTTP/HTTPS) Services: Apache HTTP

<details markdown="1">
<summary>Expand...</summary>
{: .box-note}
*Package Name(s): apache2, httpd*<br>*Common Port(s): <strong>80</strong> (HTTP), <strong>443</strong> (HTTPS), <strong>8080</strong> (Alternate HTTP), <strong>8443</strong> (Alternate HTTPS)*

Unless otherwise stated, most of the Apache configuration changes below will require you to reload or restart Apache to fully apply them, i.e.:

```console
service apache2 restart

systemctl restart apache2
```

File locations may also vary depending on how you set up your web server.

### Disable SSLv2/SSLv3/TLSv1/TLSv1.1

<details markdown="1">
<summary>Expand...</summary>
#### Debian/Ubuntu:

```console
(editor) /etc/apache2/sites-enabled/(ssl config file)

SSLProtocol all -SSLv3 -SSLv2 -TLSv1 -TLSv1.1
```
</details>

### Disable TRACE

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

### Obscure Server Information

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

### Remove Unnecessary Files/Directories

<details markdown="1">
<summary>Expand...</summary>
Remove or conceal the following directories and files from `/var/www/html` (or whichever file location is tied to your web server setup):
- `.git`
- `.gitattributes`
- `.github`
- `.gitinfo`
- `.viminfo`

If desired, you can entirely block specific sensitive file types from being browsed in `/etc/apache2/conf-enabled/security.conf` (or wherever your Apache configuration files are):

```console
RedirectMatch 404 /\.git
RedirectMatch 404 /\.svn
```

{: .box-success}
✅ **Verification**: Browse to these directories and files in any web browser and verify that you receive either a 403 Forbidden or a 404 Not Found response. You can also use curl.
</details>

### Set HTTP Strict Transport Security (HSTS)

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

</details>

---

## 🌎 Web (HTTP/HTTPS) Services: Apache Tomcat

<details markdown="1">
<summary>Expand...</summary>
{: .box-note}
*Common Port(s): <strong>80</strong> (HTTP), <strong>443</strong> (HTTPS), <strong>8080</strong> (Alternate HTTP), <strong>8443</strong> (Alternate HTTPS)*
</details>