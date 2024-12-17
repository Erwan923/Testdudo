## Web Attack Techniques

### Initial Scanning
* Basic web scan
        * `whatweb -v [target]`
* Directory enumeration
        * `gobuster dir -u [target] -w wordlist.txt`
* Subdomain discovery
        * `subfinder -d [target]`

### SQLi Techniques
* Basic injection test
        * `sqlmap -u [target] --dbs`
* Advanced options
        * `sqlmap -u [target] --risk=3 --level=5 --threads=10`
* Form testing
        * `sqlmap -u [target] --forms --batch`