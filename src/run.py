import yaml
import argparse

from metapply.core.ansible import Ansible
from metapply.core.scenario_loader import ScenarioLoader
from metapply.core.vulnerability_loader import VulnerabilityLoader

ansible = Ansible()
vulnerability_loader = VulnerabilityLoader()
scenario_loader = ScenarioLoader(vulnerability_loader=vulnerability_loader)

parser = argparse.ArgumentParser(
    description='Metapply vulnerability application framework.'
)

parser.add_argument('--scenario', type=str, help='Scenario to start')
parser.add_argument('--search', type=str, help='Search vulnerabilities by keyword')
parser.add_argument('--user', type=str, help='User used to connect to remote target')

args = parser.parse_args()

with open(args.scenario, 'r') as stream:
    scenario = scenario_loader.load(yaml.load(stream))
    ansible.execute_scenario(scenario, user=args.user)
