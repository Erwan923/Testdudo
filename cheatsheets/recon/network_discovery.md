# Network Discovery Phase

## Initial Host Discovery
`nmap -sn {target}` # {description: Quick host discovery scan, threat_level: low}
`masscan -p1-65535 {target} --rate=1000` # {description: Fast port scan, threat_level: medium, prerequisites: ["target_is_authorized"]}

## Service Enumeration
`nmap -sV -sC {target}` # {description: Service version detection, threat_level: medium}
`nmap -p- -T4 {target}` # {description: Full port scan, threat_level: high, prerequisites: ["initial_scan_complete"]}

## SMB Enumeration
`enum4linux -a {target}` # {description: Full SMB enumeration, threat_level: medium}
`smbclient -L {target}` # {description: List SMB shares, threat_level: low}

## DNS Information Gathering
`dig axfr @{target}` # {description: DNS zone transfer attempt, threat_level: medium}
`dnsenum {target}` # {description: DNS enumeration and brute force, threat_level: medium}

## SSL/TLS Analysis
`sslscan {target}` # {description: SSL/TLS configuration analysis, threat_level: low}
`testssl.sh {target}` # {description: Comprehensive SSL/TLS security testing, threat_level: medium}