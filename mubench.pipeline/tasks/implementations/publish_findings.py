import getpass
import logging
from typing import List, Dict
from urllib.parse import urljoin

from requests import RequestException

from data.experiments import Experiment
from data.finding import SpecializedFinding
from data.project import Project
from data.project_compile import ProjectCompile
from data.project_version import ProjectVersion
from data.run import Run
from data.snippets import SnippetUnavailableException
from utils.web_util import post, as_markdown


class PublishFindingsTask:
    def __init__(self, experiment: Experiment, dataset: str, compiles_base_path: str, review_site_url: str,
                 review_site_user: str= "", review_site_password: str= ""):
        super().__init__()
        self.max_files_per_post = 20  # 20 is PHP's default limit to the number of files per request

        self.experiment = experiment
        self.detector = experiment.detector
        self.dataset = dataset
        self.compiles_base_path = compiles_base_path
        self.review_site_url = review_site_url
        self.__upload_url = urljoin(self.review_site_url, "api/upload/" + self.experiment.id)
        self.review_site_user = review_site_user
        self.review_site_password = review_site_password

        self.logger = logging.getLogger("tasks.review_findings")

        if self.review_site_user and not self.review_site_password:
            self.review_site_password = getpass.getpass(
                "Enter review-site password for '{}': ".format(self.review_site_user))

        self.logger.info("Prepare findings of %s in %s for upload to %s...",
                         self.detector, self.experiment, self.__upload_url)

    def run(self, project: Project, version: ProjectVersion, detector_run: Run,
            version_compile: ProjectCompile) -> List:
        logger = self.logger.getChild("version")

        run_info = detector_run.get_run_info()
        potential_hits = detector_run.get_potential_hits()

        if detector_run.is_success():
            logger.info("Preparing findings in %s...", version)
            result = "success"
            logger.info("Found %s potential hits.", len(potential_hits))
        else:
            if detector_run.is_error():
                logger.info("Run on %s produced an error.", version)
                result = "error"
            elif detector_run.is_timeout():
                logger.info("Run on %s timed out.", version)
                result = "timeout"
            else:
                logger.info("Not run on %s.", version)
                result = "not run"

        try:
            logger.info("Publishing findings...")
            for potential_hits_slice in self.__slice_by_max_files_per_post(potential_hits):
                post_data_slice = []
                for potential_hit in potential_hits_slice:
                    postable_data = self._prepare_post(potential_hit, version_compile, logger)
                    post_data_slice.append(postable_data)

                file_paths = PublishFindingsTask.get_file_paths(potential_hits_slice)
                self.__post(project, version, run_info, result, post_data_slice, file_paths)
            logger.info("Findings published.")
        except RequestException as e:
            response = e.response
            if response:
                logger.error("ERROR: %d %s: %s", response.status_code, response.reason, response.text)
            else:
                logger.error("ERROR: %s", e)

    def __slice_by_max_files_per_post(self, potential_hits: List[SpecializedFinding]) -> List[List[SpecializedFinding]]:
        potential_hits_slice = []
        number_of_files_in_slice = 0
        for potential_hit in potential_hits:
            number_of_files_in_hit = len(potential_hit.files)
            if number_of_files_in_slice + number_of_files_in_hit > self.max_files_per_post:
                yield potential_hits_slice
                potential_hits_slice = [potential_hit]
                number_of_files_in_slice = number_of_files_in_hit
            else:
                potential_hits_slice.append(potential_hit)
                number_of_files_in_slice += number_of_files_in_hit

        yield potential_hits_slice

    def _prepare_post(self, finding: SpecializedFinding, version_compile, logger) -> Dict[str, str]:
        markdown_dict = self._to_markdown_dict(finding)

        try:
            snippets = finding.get_snippets(version_compile.original_sources_path)
        except SnippetUnavailableException as e:
            logger.warning("No snippets added for %s", e.file)
            logger.debug("Failed to find snippets: %s", e.exception)
            snippets = []

        markdown_dict["target_snippets"] = [snippet.__dict__ for snippet in snippets]
        return markdown_dict

    def __post(self, project, version, run_info, result, upload_data, file_paths):
        data = {}
        data.update(self._to_markdown_dict(run_info))
        data.update({
            "dataset": self.dataset,
            "detector": self.detector.id,
            "project": project.id,
            "version": version.version_id,
            "result": result,
            "potential_hits": upload_data
        })
        post(self.__upload_url, data, file_paths=file_paths,
             username=self.review_site_user, password=self.review_site_password)

    @staticmethod
    def get_file_paths(findings: List[SpecializedFinding]) -> List[str]:
        files = []
        for finding in findings:
            files.extend(finding.files)
        return files

    def _to_markdown_dict(self, finding: SpecializedFinding) -> Dict[str, str]:
        markdown_dict = dict()
        for key, value in finding.items():
            markdown_dict[key] = as_markdown(value)
        return markdown_dict

