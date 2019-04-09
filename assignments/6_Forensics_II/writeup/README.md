# Writeup 6 - Forensics

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examniation.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (45 Pts)

#### 1.

The IP address that has been attacked is 142.93.136.81.



#### 2.

The log shows the attackers querying a myriad of commonly used ports, which suggests that they are using a port scanning tool.
This is similar to the behavior of nmap used with the fast option.
After this is complete, the remainder of the attack seems to be carried out manually.



#### 3.

The hackers' IP address is 159.203.113.181.
They appear to be located in Clifton, New Jersey.



#### 4.

The attackers are using port 21, the File Transfer Protocol control port, to steal files through port 20, the File Transfer Protocol data port.



#### 5.
  
The attackers stole the file `find_me.jpeg`, an image file.
This photo was taken in Maldonado Department, Uraguay, on December 23, 2018 at 5:16:24 PM.
It was taken with an iPhone 8 at an altitude of 4.5726 meters above sea level.



#### 6.

The attackers left a file called `greetz.fpff` on the server.



#### 7.
  
There are several potential countermeasures that may be implemented to prevent such attacks from happening in the future.
One approach would be to implement two-factor authentication for the login for FTP.
This would increase the difficulty of the attacker gaining access to the server, since they would need access to the physical device used for authentication.
Alternatively, they could implement an IP whitelist or blacklist, either only permitting known valid IP addresses for the intended user, or forbidding those that are known to be suspect (which in this case may be determined by the suspicious nmap behavior recorded at the beginning of the attack).



### Part 2 (55 Pts)

*Replace this text with your repsonse to our prompt for part 2!*
