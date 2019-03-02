# Writeup 3 - Operational Security and Social Engineering

Name: Daniel Kelly
Section: 0101

I pledge on my honor that I have not given or received any unauthorized assistance on this assignment or examniation.

Digital acknowledgement: Daniel Kelly

## Assignment Writeup

### Part 1 (40 pts)

Determining a novel pretext that would enable the covert collection of the answers to all five questions is a non-trivial task, particularly due to question 4.
The other four questions could likely be ascertained through a more varied and inventive approach, since these questions could be considered "personal trivia".
Someone is much less likely to reveal their ATM pin to an untrusted source, however.
As such, it is necessary to adopt a pretext of someone with perceived authority to be requesting semi-sensitive information.

For this exercise, I would call Elizabeth toward the end of a workday posing as a member of the bank's IT department.
I would spoof the phone number so it appears as though the call originated from within the bank's internal phone system.
Prior to the call, I would perform some recon via various OPINT techniques in order to gain as much familiarity with the company's organizational structure as possible.
This familiarity would be beneficial in allowing me to effectively pose as an employee within the company.

I would explain that there have been some internal connectivity problems within the company's network that have been causing user accounts to be locked out of network resources, and that in order to ensure smooth operation, the IT department was contacting all affected users in order to walk them through the process of reconnecting their account.
I would preface this call with a spoofed email earlier in the day appearing to come from the IT department.
The email would likewise explain the "connectivity problems", and prime Elizabeth to be more trusting.

After explaining the need for this connection reset process, I would tell her that I needed to ask her some preset questions in order to verify her identity before proceeding.
To "confirm" her identity, I would ask her mother's maiden name, the city she was born in, and the name of her first pet.
After she answers, I would confirm that she gave the "correct" answers, and that we could then proceed.

To begin the process, I would then direct her to open a webbrowser to begin the process, asking her which browser she typically user in order to "verify" that it would be a compatible browser for the connectivity repair process.
I would then direct her to a faked website I set up with a url that has the appearance of belonging to the bank, something like `133bank.mon.ey`.
This site would be mocked up to appear visually similar to the bank's actual website.
The page I would lead her to is one for "account network configuration" specifically, as it is a part of the site that would not exist on the actual site, so she would have no familiarity with it, and would not be suspect if things appeared different than expected.

The page would have a login prompt for her to enter her username and password, which would actually just accept any input provided.
Once "logged in", I would describe certain aspects of the page in order to "verify" that she is on the correct page.
This is trivial to do, as I would have full control over the contents of this fake site, and it would have the effect of further gaining her trust, as it presents me as someone with a level of familiarity with the internals of a "secure region" of the site.

Next, I would lead her to a particular tab on the page for "resetting the network connection", which would prompt for her ATM pin before performing such an action.
This is actually made much easier since she actually works for the bank, so her pin might seem like a valid credential for the bank's internal systems to request.
Morover, she wouldn't be directly relaying her pin to me, but entering it in to a seemingly secure connection, which is easier for her to trust.

The page would load for a bit with a dummy progress indicator, and then indicate success.
Finally, I would lead her to a fake network diagnostic page and ask her to check the status to confirm that the reset worked, and for her to read some fake nonsense information to make it seem more realistic.

During this process, she may be wary of my credentials.
I would use prior recon to gain as much familiarity with other actual members of the IT department, whom I could bring up in conversation early on in the event she grows suspicious having not hear of me working in IT before.
She also may ask about the reason behind the network problems, to which I would reply that a recent change in backend hardware forced a manual reset for a small group of users.

### Part 2 (60 pts)

#### Vulnerability 1- Weak password
The password used for Elizabeth's server login, `systemofadown`, is **very** weak.
This is not only because it is a string of exclusively lowercase alphabetic characters, but more importantly because it is a commonly used password.
Searching on `haveibeenpwned.com/Passwords` reveals that this particular password has been seen in *at least* 4,163 data breaches, making it easy for malicious actors to guess.

There are a number of possible rectifications for this issue.
One simple solution is to use a password manager to automatically generate and store a password for the server.
This makes the server password much harder to guess by an attacker, and easily allows for a unique password to be used for each service.
While the password manager itself may be copromised, it remains a better solution, as it can be kept offline, requiring physical access to retrieve the password.
Additionally, remembering a single difficult password for a manager is much easier than having to remember one for each service.

An additional layer of security may also be the implementation of two-factor authentication.
This would require a separate login confirmation through a physical device in the posession of the user.
Thus, even if the password is cracked, the hacker would not gain access to the account without the second factor.

#### Vulnerability 2- Exposed ports
The bank website exposes the publicly accessible port 1337 through which a user can log in to the internal system remotely.
Simply leaving this port open greatly reduces the work of a hacker, as it is an easy entrypoint into the main system.
As such, this port should be closed entirely.

It may be that employees require remote system access, and in such a case, the server should be configured with a VPN.
This adds an extra layer of security on top of the system login itself.
A good VPN from a reputable company is designed around strong cryptographic principals, which means that it is more difficult to break than a simple text password.
While there is the risk of a backdoor built into any VPN, this would jeopardize the credibility of the company that created it.
Thus, companies such as Cisco are incentivized to ensure such vulnerabilities are not present.

#### Vulnerability 3- Reused username
Elizabeth reused the same username from her social acccounts (Twitter, Reddit, Github) for her professional work account.
This cuts an attacker's work in half, as once they find the username associated with a particular person, they already have one half of the user's login.
It is generally better practice to use a disctinct username for one's work login, and refrain from reusing it in any social accounts.
While one's work username is not secret *per se*, making it distinct from personal accounts adds more work for the hacker at little cost to the user.

#### Vulnerability 3.5- Poor network monitoring
While this is not strictly a vulerability in the traditional sense, the system did very little monitoring for potential intrusions.
Many of the steps in the hacking process generate a lot of unusual network traffic which may be identified without much difficulty.

For example, scanning with nmap is a fairly noisy process, which is trivially detected server side.
Modern systems are likely to be scanned by far greater numbers of benign actors than malicious ones, but by logging the scans, one can correlate them with other unusual activity to construct a heuristic for probability of attack.

Rapid and repeated port access from a remote IP, such as that which occured during week 2's brute force password cracking, is also indicative of a potential attack, and should be recorded.

Finally, logging and placing restrictions on the number of incorrect logins for a given account is a trivial technique to mitigate brute force attacks.
There are varying approaches to handling cases of an exceeded number of incorrect logins.
A CAPTCHA can be deployed to further verify that a human user is attempting to login.
Alternatively, a temporary timeout can be applied, or the offending IP address can be blacklisted entirely.
The exact method can be tailored to the specific use case.

More sophisticated intrusion detection systems can corrrelate a wide array of factors, including those discussed above among others, in order to detect when an attack is underway.
While these represent a non-trivial financial investment, it may be worthwhile for a banking institution.
