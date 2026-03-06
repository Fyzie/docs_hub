# Raspberry Pi Internet Routing Issue (WiFi + Ethernet)

## Issue
When both **WiFi (wlan0)** and **Ethernet (eth0)** are connected on a Raspberry Pi, the device may fail to access the internet through WiFi.

## Possible Reason
Multiple **default routes** exist in the routing table, and Linux selects the route with the **lowest metric**.  
If Ethernet has the lower metric, internet traffic will be routed through Ethernet instead of WiFi.

Since Ethernet is often used for **local communication (e.g., Jetson or other devices)** and not connected to a router, internet access fails.

---

## Example

Check the routing table:

```bash
ip route
````

Output example:

```bash
default via 192.168.1.254 dev eth0 metric 100
default via 10.0.0.150 dev wlan0 metric 600
```

Meaning:

| Interface | Metric | Priority |
| --------- | ------ | -------- |
| eth0      | 100    | Highest  |
| wlan0     | 600    | Lower    |

Linux always chooses the **lowest metric**, so internet traffic goes through **eth0**, which may not have internet access.

---

## Fix (Option 1)

Delete the Ethernet default route so that traffic goes through WiFi:

```bash
sudo ip route del default via 192.168.1.254 dev eth0
```

---

## Verify

Check the routing table again:

```bash
ip route
```

Expected result:

```bash
default via 10.0.0.150 dev wlan0
```

---

## Test Internet Connection

```bash
ping 8.8.8.8
```

If packets return successfully, the internet connection is working.

---

## Notes

* Ethernet can still be used for **local communication** (e.g., Raspberry Pi ↔ Jetson).
* WiFi will now handle **all internet traffic**.

---

## Fix (Option 2)
In case above solution is not working,
Edit network configuration:
```
sudo nano /etc/dhcpcd.conf
```

Add or modify:
```
interface wlan0
metric 100

interface eth0
metric 400
```

Reboot:
```
sudo reboot
```
