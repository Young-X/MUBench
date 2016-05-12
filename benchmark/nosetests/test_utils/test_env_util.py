import yaml
from os import makedirs, chdir
from os.path import join, abspath, dirname, pardir
from pathlib import Path
from shutil import rmtree
from tempfile import mkdtemp

from benchmark.utils.io import safe_write


class TestEnv:
    def __init__(self):
        self.TEST_ENV_SOURCE_DIR = join(dirname(abspath(__file__)), 'test-env')
        self.TEST_ENV_INSTANCE_PATH = mkdtemp(prefix='mubench-test-env_')

        mubench = join(dirname(abspath(__file__)), pardir, pardir, pardir)
        chdir(mubench)  # set the cwd to the MUBench folder

        self.DATA = []

        self.DETECTOR = 'dummy-miner'

        self.FILE_DETECTOR_RESULT = 'result.txt'

        self.DATA_PATH = join(self.TEST_ENV_INSTANCE_PATH, 'data')
        self.RESULTS_PATH = join(self.TEST_ENV_INSTANCE_PATH, 'results', self.DETECTOR)
        self.CHECKOUT_DIR = join(self.TEST_ENV_INSTANCE_PATH, 'checkout')

        makedirs(self.RESULTS_PATH, exist_ok=True)

        self.REPOSITORY_GIT = join(self.TEST_ENV_INSTANCE_PATH, 'repository-git')
        self.REPOSITORY_SVN = Path(join(self.TEST_ENV_INSTANCE_PATH, 'repository-svn')).as_uri()

        self.TIMEOUT = None

        self.__create_yaml_data()

    # noinspection PyPep8Naming
    def tearDown(self):
        rmtree(self.TEST_ENV_INSTANCE_PATH, ignore_errors=True)

    def __create_yaml_data(self):
        git_yaml = self.__get_git_yaml()
        svn_yaml = self.__get_svn_yaml()
        synthetic_yaml = self.__get_synthetic_yaml()
        self.create_data_file('git.yml', git_yaml)
        self.create_data_file('svn.yml', svn_yaml)
        self.create_data_file('synthetic.yml', synthetic_yaml)

    def __get_git_yaml(self):
        repository = {'url': self.REPOSITORY_GIT, 'type': 'git'}
        files = [{'name': 'some-class.java'}]
        fix = {'repository': repository, 'revision': '', 'files': files}
        self.git_misuse_label = "someClass#this#doSomething"
        misuse = {'file': files[0], 'type': 'some-type', 'method': 'doSomething(Object, int)',
                  'usage': 'digraph { 0 [label="' + self.git_misuse_label + '"] }'}
        content = {'misuse': misuse, 'fix': fix}
        return content

    def __get_svn_yaml(self):
        content = {
            'fix': {'repository': {'url': self.REPOSITORY_SVN, 'type': 'svn'}, 'revision': '1',
                    'files': [{'name': 'some-class.java'}]}}
        return content

    @staticmethod
    def __get_synthetic_yaml():
        content = {
            'fix': {'repository': {'url': 'synthetic-close-1.java', 'revision': '', 'type': 'synthetic'},
                    'files': [{'name': 'synthetic.java'}]}}
        return content

    def create_data_file(self, file_name: str, content: dict):
        file = join(self.DATA_PATH, file_name)
        safe_write(yaml.dump(content), file, append=False)
        self.DATA.append((file, content))