
from metapply.config import Config
from metapply.core.logger import Logger
import getpass
from pprint import pprint
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.task_result import TaskResult
import ansible.constants as C


class AnsibleResultCallback(CallbackBase):

    def __init__(self, on_success):
        super(AnsibleResultCallback, self).__init__()
        self.on_success = on_success

    def v2_playbook_on_task_start(self, task, is_conditional):
        Logger().debug('Starting task', task)

    def on_any(self, *args, **kwargs):
        try:
            # Hack to print more verbose result
            Logger().debug('Result', args[0][0]._result)
        except:
            pass

        Logger().debug('Process', args, kwargs)

    def v2_runner_on_failed(self, result, **kwargs):
        Logger().debug('Ansible play run failed', result._result)

    def v2_runner_on_ok(self, result, **kwargs):
        # Too verbose
        if ('ansible_facts' in result._result):
            del(result._result['ansible_facts'])
        Logger().debug('Ansible play successful', result._result)


Options = namedtuple('Options', [
    'connection',
    'tags',
    'forks',
    'become',
    'module_path',
    'sudo',
    'become_method',
    'become_user',
    'remote_user',
    'check',
    'diff']
)


class Ansible():

    def __init__(self):
        self.config = Config()
        self.logger = Logger()

        # Overwrite to use only frame roles ... (not good though)
        C.DEFAULT_ROLES_PATH = [self.config.get('vulnerabilities_path')]
        # C.DEFAULT_DEBUG = True

    def check_preconditions_for_scenario(self, scenario, on_success=(lambda: True), user=None):
        self.logger.info('Checking preconditions')
        self._execute(
            scenario,
            on_success=on_success,
            tags=['precondition'],
            user=user
        )

    def check_postconditions_for_scenario(self, scenario, on_success=(lambda: True), user=None):
        self.logger.info('Checking postconditions')
        self._execute(
            scenario,
            tags=['postcondition'],
            on_success=on_success,
            user=user
        )

    def execute_scenario(self, scenario, on_success=(lambda: True), user=None):
        if user is None:
            user = getpass.getuser()

        self.logger.debug('Executing ansible for scenario')
        self.logger.debug('Targets:', scenario.targets)
        self.logger.debug('Vulnerabilities:', scenario.get_ansible_roles())

        # TODO: figure out maybe _execute is async, doesn't look like it tho
        # Ansible somehow doesn't want to run twice the same role ... (bug? figure out pls)
        # self.check_preconditions_for_scenario(scenario, user=user)

        self._execute(scenario, user=user)

        # self.check_postconditions_for_scenario(
        #     scenario, on_success=on_success, user=user
        # )

    def _execute(self, scenario, tags=[], check=False, on_success=(lambda: True), user=None, gather_facts='true'):
        # initialize needed objects
        loader = DataLoader()
        options = Options(connection='ssh',
                          forks=100,
                          become=True,
                          module_path=None,
                          tags=tags,
                          sudo=True,
                          remote_user=user,
                          become_method='sudo',
                          become_user='root',
                          check=check,
                          diff=False)
        passwords = dict(vault_pass='secret')

        # Instantiate our ResultCallback for handling results as they come in
        results_callback = AnsibleResultCallback(on_success=on_success)

        hosts = ','.join(scenario.targets)

        # create inventory and pass to var manager
        # use path to host config file as source or hosts in a comma separated string
        inventory = InventoryManager(loader=loader, sources=hosts + ',')
        variable_manager = VariableManager(loader=loader, inventory=inventory)

        # create play with tasks
        play_source = dict(
            name="Dynamic ansible playbook - " + ' '.join(tags),
            hosts=hosts,
            gather_facts=gather_facts,
            roles=scenario.get_ansible_roles()
        )
        play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

        # actually run it
        tqm = None
        try:
            tqm = TaskQueueManager(
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords,
                stdout_callback=results_callback
            )
            self.logger.debug('Starting ansible with options', options, play)

            result = tqm.run(play)

            self.logger.debug('Play succesfully finished with result', result)
            on_success()
        except Exception as e:
            self.logger.debug('Error running the play', str(e))

        finally:
            if tqm is not None:
                tqm.cleanup()

            # Remove ansible tmpdir
            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)

            self.logger.debug('Ansible play cleaned up')
