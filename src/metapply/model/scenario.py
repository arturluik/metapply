

class Scenario():

    def __init__(self):
        self.targets = []
        self.vulnerabilities = []

    def add_vulnerability(self, vulnerability):
        self.vulnerabilities.append(vulnerability)

    def add_target(self, target):
        self.targets.append(target)

    def get_ansible_roles(self):
        return list(map(lambda x: x.name, self.vulnerabilities))
