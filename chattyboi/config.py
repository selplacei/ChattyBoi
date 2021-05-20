#  Copyright (c) 2021 Illia Boiko
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
import logging
import sys
from pathlib import Path

from PySide2.QtCore import QSettings, QStandardPaths

QT_APP_NAME = 'ChattyBoi'

LOG_FORMAT = '%(asctime)s:%(name)s: [%(levelname)s] %(message)s'
LOG_DATEFMT = '%H:%M:%S'
# TODO: better way to enable debug mode
LOG_LEVEL = logging.DEBUG if '--debug' in sys.argv else logging.WARNING

INSTALLATION_PATH = Path(__file__).parent.resolve()

DATA_PATH = Path(
    QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)
) / QT_APP_NAME
DATA_PATH.mkdir(parents=True, exist_ok=True)

settings = QSettings(QSettings.UserScope, QT_APP_NAME)
logging.basicConfig(format=LOG_FORMAT, datefmt=LOG_DATEFMT, level=LOG_LEVEL)


def reset():
    settings.clear()
