#!/usr/bin/env python
# Copyright 2021-2022 python-tuf contributors
# SPDX-License-Identifier: MIT OR Apache-2.0

"""Simple repository example application

The application stores metadata and targets in memory, and serves them via http.
Nothing is persisted on disk or loaded from disk. The application simulates a
live repository by adding new target files periodically.
"""

import argparse
import logging
import sys,os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from time import time
from typing import Dict, List

from _my_repo import SimpleRepository

from tuf.api.serialization.json import JSONSerializer

logger = logging.getLogger(__name__)


class ReqHandler(BaseHTTPRequestHandler):
    """HTTP handler for the repository example application

    Serves metadata, targets and a small upload API using a SimpleRepository
    """

    def do_POST(self):
        self.send_error(404)
        self.end_headers()

    def do_GET(self):
        """Handle GET: metadata and target files"""
        data = None

        # if self.path.startswith("/metadata/") and self.path.endswith(".json"):
        #     data = self.get_metadata(
        #         self.path[len("/metadata/") : -len(".json")]
        #     )
        # elif self.path.startswith("/targets/"):
        #     data = self.get_target(self.path[len("/targets/") :])
        print(f'{self.path}')
        if data is None:
            self.send_error(404)
        else:
            self.send_response(200)
            self.send_header("Content-length", len(data))
            self.end_headers()
            self.wfile.write(data)

    def get_metadata(self, ver_and_role: str):
        pass

    def get_target(self, targetpath: str):
        pass


class RepositoryServer(ThreadingHTTPServer):
    def __init__(self, port: int, repo_path: str):
        super().__init__(("127.0.0.1", port), ReqHandler)
        self.timeout = 1
        self.repo = SimpleRepository(repo_path)


def main(argv: List[str]) -> None:
    """Example repository server"""

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="count")
    parser.add_argument("-p", "--port", type=int, default=8001)
    parser.add_argument("-d", "--repo", type=str, default=f'{os.getcwd()}/repo')
    args, _ = parser.parse_known_args(argv)

    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(level=level)

    server = RepositoryServer(args.port, args.repo)
    last_change = 0
    counter = 0

    logger.info(
        f"Now serving. Root v1 at http://127.0.0.1:{server.server_port}/metadata/1.root.json"
    )

    while True:
        # Simulate a live repository: Add a new target file every few seconds
        # if time() - last_change > 10:
        #     last_change = int(time())
        #     counter += 1
        #     content = str(datetime.fromtimestamp(last_change))
        #     server.repo.add_target(f"file{str(counter)}.txt", content)

        server.handle_request()


if __name__ == "__main__":
    main(sys.argv)
