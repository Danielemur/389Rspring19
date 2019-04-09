# Writeup 6 - Forensics

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examniation.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (45 Pts)

#### 1.

The IP address that has been attacked is 142.93.136.81, which is easily identified as it is the only one involved in every entry in the log.


#### 2.

By examining the logs, we see one particular IP address attempting to connect to many different ports (indicated by the `SYN` messsage sent).
The `RST, ACK` response indicates that the port is not open, while a `SYN, ACK` indicates that it is.

The log shows the attackers querying a myriad of commonly used ports, which suggests that they are using a port scanning tool.
This is similar to the behavior of nmap used with the fast option.
After this is complete, the remainder of the attack seems to be carried out manually.



#### 3.

The hackers' IP address is 159.203.113.181.
This is evident as it is both the most prevalent IP interacting with the server by far, but also because it is the IP involved in the suspicious behavor described above.
By entering this IP in an online geolocation lookup at `iplocation.net`, I found that they appear to be located in Clifton, New Jersey.



#### 4.

The attackers are using port 21, the File Transfer Protocol control port, to steal files through port 20, the File Transfer Protocol data port.



#### 5.
  
The attackers stole the file `find_me.jpeg`, an image file, which is evident by looking at the log entry with info `Request: RETR find_me.jpeg`, as well as the subsequent transmissions using the `FTP-DATA` protocol.
Using the command line tool exif, we find lat-long coordinates and a timestamp which indicate that this photo was taken in Maldonado Department, Uraguay, on December 23, 2018 at 5:16:24 PM.
The command also shows that was taken with an iPhone 8 at an altitude of 4.5726 meters above sea level.



#### 6.

The attackers left a file called `greetz.fpff` on the server, evidenced by the entry with info `Request: STOR greetz.fpff`



#### 7.
  
There are several potential countermeasures that may be implemented to prevent such attacks from happening in the future.
One approach would be to implement two-factor authentication for the login for FTP.
This would increase the difficulty of the attacker gaining access to the server, since they would need access to the physical device used for authentication.
Alternatively, they could implement an IP whitelist or blacklist, either only permitting known valid IP addresses for the intended user, or forbidding those that are known to be suspect (which in this case may be determined by the suspicious nmap behavior recorded at the beginning of the attack).



### Part 2 (55 Pts)

#### 1.

#### 2.

##### 1.

##### 2.

The file `greetz.fpff` was authored by `fl1nch`.

##### 3.

* Section 1:
  * Type: SECTION_ASCII
  * Data: 
* Section 2:
  * Type: SECTION_COORD
  * Data: (52.336035, 4.880673)
* Section 3:
  * Type: SECTION_PNG
  * Data: 'Hey you, keep looking :)'
* Section 4:
  * Type: SECTION_ASCII
  * Data: '}R983CSMC_perg_tndid_u0y_yllufep0h{-R983CSMC'
* Section 5:
  * Type: SECTION_ASCII
  * Data: 'Q01TQzM4OVIte2hleV9oM3lfeTBVX3lvdV9JX2RvbnRfbGlrZV95b3VyX2Jhc2U2NF9lbmNvZGluZ30='

##### 4.

##### 5.


