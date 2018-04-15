from metapply.model.scenario import Scenario


class ScenarioLoader():

    def __init__(self, vulnerability_loader):
        self.vulnerability_loader = vulnerability_loader

    def load(self, scenario_description):
        scenario = Scenario()
        for vulnerability_entry in scenario_description['vulnerabilities']:
            (name, version) = vulnerability_entry.split('=')
            scenario.add_vulnerability(
                self.vulnerability_loader.find_by_name_and_version(
                    name, version
                )
            )

        for target in scenario_description['targets']:
            scenario.add_target(target)

        return scenario
