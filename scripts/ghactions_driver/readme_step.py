import subprocess
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, Template


class Step:
    """
    StepType in workflow
    """

    Environment = None

    @staticmethod
    def init_jinja_loader() -> Environment:
        jinja_folder_path = (
            Path(ReadmeStepsManage.git_base_dir())
            / "scripts"
            / "ghactions_driver"
            / "workflow_steps"
        )
        Step.Environment = Environment(
            loader=FileSystemLoader(jinja_folder_path.resolve())
        )

    def __init__(self, name: str) -> None:
        self.workflow_name = name

    def get_workflow_step(self) -> str:
        # virtual method for override
        return ""

    @staticmethod
    def get_workflow_template(step_file_name: str) -> Template:
        # virtual method for override
        if Step.Environment is None:
            Step.init_jinja_loader()
        template = Step.Environment.get_template(step_file_name)
        return template


class AzureLoginStep(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Azure Login")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_azure_login.yml.jinja2")
        return template.render(
            {
                "step_name": self.workflow_name,
            }
        )


class InstallDependenciesStep(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Prepare requirements")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_install_deps.yml.jinja2")
        return template.render(
            {
                "step_name": self.workflow_name,
                "working_dir": ReadmeSteps.working_dir,
            }
        )


class InstallDevDependenciesStep(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Prepare dev requirements")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_install_devdeps.yml.jinja2")
        return template.render(
            {
                "step_name": self.workflow_name,
                "working_dir": ReadmeSteps.working_dir,
            }
        )


class CreateAoaiFromYaml(Step):
    def __init__(self, yaml_name: str) -> None:
        Step.__init__(self, "Create AOAI Connection from YAML")
        self.yaml_name = yaml_name

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_yml_create_aoai.yml.jinja2")
        return template.render(
            {
                "step_name": self.workflow_name,
                "working_dir": ReadmeSteps.working_dir,
                "yaml_name": self.yaml_name,
            }
        )


class ExtractStepsAndRun(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Extract Steps")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_extract_steps_and_run.yml.jinja2")
        return template.render(
            {
                "step_name": self.workflow_name,
                "working_dir": ReadmeSteps.working_dir,
                "readme_name": (Path(ReadmeSteps.working_dir) / "README.md").as_posix(),
            }
        )


class CreateEnv(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Refine .env file")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_create_env.yml.jinja2")
        content = template.render(
            {"step_name": self.workflow_name, "working_dir": ReadmeSteps.working_dir}
        )
        return content


class CreateRunYaml(Step):
    def __init__(self) -> None:
        Step.__init__(self, "Create run.yml")

    def get_workflow_step(self) -> str:
        template = Step.get_workflow_template("step_create_run_yml.yml.jinja2")
        content = template.render(
            {"step_name": self.workflow_name, "working_dir": ReadmeSteps.working_dir}
        )
        return content


class ReadmeSteps:
    """
    Static class to record steps, to be filled in workflow templates and Readme
    """

    step_array = []  # Record steps
    working_dir = ""  # the working directory of flow, relative to git_base_dir
    template = ""  # Select a base template under workflow_templates folder
    workflow = ""  # Target workflow name to be generated

    @staticmethod
    def remember_step(step: Step) -> Step:
        ReadmeSteps.step_array.append(step)
        return step

    @staticmethod
    def get_length() -> int:
        return len(ReadmeSteps.step_array)

    # region steps
    @staticmethod
    def create_env() -> Step:
        return ReadmeSteps.remember_step(CreateEnv())

    @staticmethod
    def yml_create_aoai(yaml_name: str) -> Step:
        return ReadmeSteps.remember_step(CreateAoaiFromYaml(yaml_name=yaml_name))

    @staticmethod
    def azure_login() -> Step:
        return ReadmeSteps.remember_step(AzureLoginStep())

    @staticmethod
    def install_dependencies() -> Step:
        return ReadmeSteps.remember_step(InstallDependenciesStep())

    @staticmethod
    def install_dev_dependencies() -> Step:
        return ReadmeSteps.remember_step(InstallDevDependenciesStep())

    @staticmethod
    def create_run_yaml() -> Step:
        return ReadmeSteps.remember_step(CreateRunYaml())

    @staticmethod
    def extract_steps_and_run() -> Step:
        return ReadmeSteps.remember_step(ExtractStepsAndRun())

    # endregion steps

    @staticmethod
    def setup_target(working_dir: str, template: str, target: str) -> str:
        """
        Used at the very head of jinja template to indicate basic information
        """
        ReadmeSteps.working_dir = working_dir
        ReadmeSteps.template = template
        ReadmeSteps.workflow = target
        ReadmeSteps.step_array = []
        return ""

    @staticmethod
    def cleanup() -> None:
        ReadmeSteps.working_dir = ""
        ReadmeSteps.template = ""
        ReadmeSteps.workflow = ""
        ReadmeSteps.step_array = []


class ReadmeStepsManage:
    """
    # Static methods for manage all readme steps
    """

    repo_base_dir = ""

    @staticmethod
    def git_base_dir() -> str:
        """
        Get the base directory of the git repo
        """
        if ReadmeStepsManage.repo_base_dir == "":
            ReadmeStepsManage.repo_base_dir = (
                subprocess.check_output(["git", "rev-parse", "--show-toplevel"])
                .decode("utf-8")
                .strip()
            )
        return ReadmeStepsManage.repo_base_dir

    @staticmethod
    def write_workflow(workflow_name: str, pipeline_name: str) -> None:
        replacements = {
            "steps": ReadmeSteps.step_array,
            "workflow_name": workflow_name,
            "name": pipeline_name,
        }
        workflow_template_path = (
            Path(ReadmeStepsManage.git_base_dir())
            / "scripts"
            / "ghactions_driver"
            / "workflow_templates"
        )
        template = Environment(
            loader=FileSystemLoader(workflow_template_path.resolve())
        ).get_template(ReadmeSteps.template)
        target_path = (
            Path(ReadmeStepsManage.git_base_dir())
            / ".github"
            / "workflows"
            / f"{workflow_name}.yml"
        )
        content = template.render(replacements)
        with open(target_path.resolve(), "w", encoding="utf-8") as f:
            f.write(content)