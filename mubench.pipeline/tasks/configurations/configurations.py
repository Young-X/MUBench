from typing import List

from data.detectors import find_detector
from data.experiments import ProvidedPatternsExperiment, TopFindingsExperiment, BenchmarkExperiment
from tasks.configurations.mubench_paths import MubenchPaths
from tasks.implementations import stats
from tasks.implementations.checkout import CheckoutTask
from tasks.implementations.collect_misuses import CollectMisusesTask
from tasks.implementations.collect_projects import CollectProjectsTask
from tasks.implementations.collect_versions import CollectVersionsTask
from tasks.implementations.compile import CompileTask
from tasks.implementations.dataset_check import DatasetCheckTask
from tasks.implementations.detect import DetectTask
from tasks.implementations.info import ProjectInfoTask, VersionInfoTask, MisuseInfoTask
from tasks.implementations.publish_findings import PublishFindingsTask
from tasks.implementations.publish_metadata import PublishMetadataTask
from utils.dataset_util import get_available_datasets


class TaskConfiguration(list):
    def __init__(self, paths: MubenchPaths, config):
        super().__init__()
        self.extend(self._tasks(paths, config))

    @staticmethod
    def mode() -> str:
        raise NotImplementedError

    def _tasks(self, paths: MubenchPaths, config) -> List:
        raise NotImplementedError


def get_task_configuration(paths: MubenchPaths, config) -> TaskConfiguration:
    mode = config.task
    if config.publish_task:
        mode += " " + config.publish_task

    requested_configurations = [task_config(paths, config) for task_config in
                                TaskConfiguration.__subclasses__() if task_config.mode() == mode]
    if len(requested_configurations) > 1:
        raise ValueError("Multiple configurations for {}".format(mode))
    if len(requested_configurations) == 0:
        raise ValueError("No configuration available for {}".format(mode))

    return requested_configurations[0]


class InfoTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "info"

    def _tasks(self, paths: MubenchPaths, _) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        collect_misuses = CollectMisusesTask()
        project_info = ProjectInfoTask(paths.CHECKOUTS_PATH, paths.COMPILES_PATH)
        version_info = VersionInfoTask(paths.CHECKOUTS_PATH, paths.COMPILES_PATH)
        misuse_info = MisuseInfoTask(paths.CHECKOUTS_PATH, paths.COMPILES_PATH)
        return [collect_projects, project_info, collect_versions, version_info, collect_misuses, misuse_info]


class CheckoutTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "checkout"

    def _tasks(self, paths: MubenchPaths, config):
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        checkout = CheckoutTask(paths.CHECKOUTS_PATH, config.force_checkout, config.use_tmp_wrkdir)
        return [collect_projects, collect_versions, checkout]


class CompileTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "compile"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        checkout = CheckoutTask(paths.CHECKOUTS_PATH, config.force_checkout, config.use_tmp_wrkdir)
        compile_ = CompileTask(paths.COMPILES_PATH, config.force_compile, config.use_tmp_wrkdir)
        return [collect_projects, collect_versions, checkout, compile_]


class DetectTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "detect"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        checkout = CheckoutTask(paths.CHECKOUTS_PATH, config.force_checkout, config.use_tmp_wrkdir)
        compile_ = CompileTask(paths.COMPILES_PATH, config.force_compile, config.use_tmp_wrkdir)
        detect = DetectTask(paths.COMPILES_PATH, _get_experiment(paths, config), config.timeout, config.force_detect)
        return [collect_projects, collect_versions, checkout, compile_, detect]


class PublishFindingsTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "publish findings"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        checkout = CheckoutTask(paths.CHECKOUTS_PATH, config.force_checkout, config.use_tmp_wrkdir)
        compile_ = CompileTask(paths.COMPILES_PATH, config.force_compile, config.use_tmp_wrkdir)
        detect = DetectTask(paths.COMPILES_PATH, _get_experiment(paths, config), config.timeout, config.force_detect)
        publish = PublishFindingsTask(_get_experiment(paths, config), config.dataset, paths.COMPILES_PATH,
                                      config.review_site_url, config.review_site_user, config.review_site_password)
        return [collect_projects, collect_versions, checkout, compile_, detect, publish]


class PublishMetadataTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "publish metadata"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        checkout = CheckoutTask(paths.CHECKOUTS_PATH, config.force_checkout, config.use_tmp_wrkdir)
        collect_misuses = CollectMisusesTask()
        publish = PublishMetadataTask(paths.COMPILES_PATH, config.review_site_url, config.review_site_user,
                                      config.review_site_password)
        return [collect_projects, collect_versions, checkout, collect_misuses, publish]


class StatsTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "stats"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        collect_misuses = CollectMisusesTask()
        calculator = stats.get_calculator(config.script)
        return [collect_projects, collect_versions, collect_misuses, calculator]


class DatasetCheckTaskConfiguration(TaskConfiguration):
    @staticmethod
    def mode() -> str:
        return "dataset-check"

    def _tasks(self, paths: MubenchPaths, config) -> List:
        collect_projects = CollectProjectsTask(paths.DATA_PATH)
        collect_versions = CollectVersionsTask()
        collect_misuses = CollectMisusesTask()
        dataset_check = DatasetCheckTask(get_available_datasets(paths.DATASETS_FILE_PATH), paths.CHECKOUTS_PATH,
                                         paths.DATA_PATH)
        return [collect_projects, collect_versions, collect_misuses, dataset_check]


def _get_experiment(paths, config):
    if config.experiment == 1:
        return ProvidedPatternsExperiment(__get_detector(paths, config), paths.FINDINGS_PATH)
    elif config.experiment == 2:
        try:
            limit = config.limit
        except AttributeError:
            limit = 0
        return TopFindingsExperiment(__get_detector(paths, config), paths.FINDINGS_PATH, limit)
    elif config.experiment == 3:
        return BenchmarkExperiment(__get_detector(paths, config), paths.FINDINGS_PATH)


def __get_detector(paths, config):
    java_options = ['-' + option for option in config.java_options]
    return find_detector(paths.DETECTORS_PATH, config.detector, java_options, config.requested_release)
