# Introduction

The following project is created in order to mitigate the problem of applying vulnerabilities to already existing machines for educational purposes. A vulnerability is a programmer's unintended mistake in a program’s source code, misconfiguration or hardware design mistake that can lead to a malicious or unexpected behavior. The field of cyber security involves a lot of practical assignments, competitions, trainings and hands-on hacking demonstrations. All the latter require a significant amount of preparation work and expert knowledge in case one needs to demonstrate how you can exploit various programs and devices. One type of practical competition is called “capture the flag“, where you need to exploit vulnerabilities to find a sequence of symbols called as ”flag” in the device area which should be protected from unauthorized access. For instance, creating a machine for a capture the flag event needs infrastructure configuration (virtual machine deployments, network configuration), vulnerability creation, flag injections, testing vulnerabilities, all the steps can take considerable amount of time. Furthermore, vulnerabilities, which are used for demonstrations are quickly getting out of date. The flag indicates that a person has found the vulnerability and exploited it correctly.
The purpose of this project is to reduce the amount of time required for preparing demonstration machines for educational purposes via a common vulnerability application framework. Applying a vulnerability is a scalable problem - once you have a script for applying a vulnerability in a machine 𝑋 with state requirements 𝑌, you can use exactly the same script for other machines with the same state requirements 𝑌. The script to create a vulnerability can be written by a community of people. One writes a new script - everybody benefits. The similar philosophy - ”Knowledge is power, especially when its shared” is already implemented in the Metasploit Project [4]. Metasploit is meant for verifying that an exploit exists, this project applies already existing vulnerability to a machine (creates a security hole). The goal of this project is to reduce the amount of time spent on preparing vulnerable machines by introducing a new framework architecture for applying vulnerabilities automatically in a generic manner (introduction of a new DSL - domain specific language). For the latter purpose the author proposes the framework architecture, analyzes the conflict resolution/avoidance within the framework and demonstrates that this approach is possible and saves time by implementing the prototype of the framework that targets UNIX-like systems.

# Requirements
- Python 3
- Ansible 2.5+

# Development
The development can be seperated to two parts - metapply core development and module development.

### Metapply core development
Metapply core is additional layer on top of Ansible for following reasons
- To improve conflict avoidance and detection
- To follow the precondition / postcondition lifecycle

### Module (vulnerability creation script) development
All the vulnerability creation scripts are written in Ansible and located in folder /vulnerabilities.
The Ansible folder structure follows the Ansible best practices (https://docs.ansible.com/ansible/2.5/user_guide/playbooks_best_practices.html)

The only difference is that precondition steps need to be tagged with 'precondition' and postcondition steps need to be tagged with 'postcondition' the Metapply framework will handle the rest.

# Structure
Vulnerability with metadata should be placed in folder vulnerabilities/<vulnerability_name>

```
name: Shellshock
description: Bashbug / shellshock vulnerability for Debian
version: 1.0
tags:
    - shellshock
    - bashbug
author: Artur Luik
CVCCv3BaseScore: 4
CVCCv3Vector: AV:N/AC:L/Au:N/C:C/I:C/A:C
CVE: CVE-2014-6271
CWE:
   - OS Command Injections
Reference: https://nvd.nist.gov/vuln/detail/CVE-2014-6271
```

In order to execute the vulnerability in the machine you need to define a scenario, for example
```
vulnerabilities:
  - shellshock=1.0
  - proftpd-1.3.3a-backdoor=1.0
targets:
  - 192.168.56.101
```

# Usage

Run the scenario
```
python3 src/run.py --scenario examples/example.yml
```

# License
    Metapply | Vulnerability application framework - collection of Ansible for creating vulnerabilities for demonstration purposes
    Copyright (C) 2018  Artur Luik

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

