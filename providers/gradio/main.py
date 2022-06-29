import argparse
import uuid
from argparse import ArgumentParser
from typing import List

from dstack import Provider, Job, App


# TODO: Provide job.applications (incl. application name, and query)
class Gradiorovider(Provider):
    def __init__(self):
        super().__init__(schema="providers/gradio/schema.yaml")
        self.file = self.workflow.data["file"]
        # TODO: Handle numbers such as 3.1 (e.g. require to use strings)
        self.python = str(self.workflow.data.get("python") or "3.10")
        self.version = self.workflow.data.get("version")
        self.args = self.workflow.data.get("args")
        self.requirements = self.workflow.data.get("requirements")
        self.environment = self.workflow.data.get("environment") or {}
        self.artifacts = self.workflow.data.get("artifacts")
        self.working_dir = self.workflow.data.get("working_dir")
        self.resources = self._resources()
        self.image = self._image()

    def parse_args(self):
        parser = ArgumentParser(prog="dstack run gradio")
        self._add_base_args(parser)
        if self.run_as_provider:
            parser.add_argument("file", metavar="FILE", type=str)
            parser.add_argument("args", metavar="ARGS", nargs=argparse.ZERO_OR_MORE)
        args, unknown = parser.parse_known_args(self.provider_args)
        self._parse_base_args(args)
        if self.run_as_provider:
            self.workflow.data["file"] = args.file
            _args = args.args + unknown
            if _args:
                self.workflow.data["args"] = _args

    def create_jobs(self) -> List[Job]:
        return [Job(
            image=self.image,
            commands=self._commands(),
            environment=self.environment,
            working_dir=self.working_dir,
            resources=self.resources,
            artifacts=self.artifacts,
            port_count=1,
            apps=[App(
                port_index=0,
                app_name="gradio",
            )]
        )]

    def _image(self) -> str:
        cuda_is_required = self.resources and self.resources.gpu
        return f"dstackai/python:{self.python}-cuda-11.1" if cuda_is_required else f"python:{self.python}"

    def _commands(self):
        commands = [
            "pip install gradio" + (f"=={self.version}" if self.version else ""),
        ]
        args_init = ""
        if self.args:
            if isinstance(self.args, str):
                args_init += " " + self.args
            if isinstance(self.args, list):
                args_init += " " + ",".join(map(lambda arg: "\"" + arg.replace('"', '\\"') + "\"", self.args))
        commands.append(
            f"GRADIO_SERVER_PORT=$JOB_PORT_0 GRADIO_SERVER_NAME=0.0.0.0 python {self.file}{args_init}"
        )
        return commands


if __name__ == '__main__':
    provider = Gradiorovider()
    provider.start()