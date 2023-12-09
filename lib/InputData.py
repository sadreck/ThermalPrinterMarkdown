from typing import Union
import os


class InputData:
    def load(self, source: str, type: str) -> Union[str, None]:
        if type == 'file':
            return self.__load_file(source)

        return None

    def __load_file(self, local_file: str) -> str:
        if not os.path.isfile(local_file):
            raise Exception('Input file does not exist: {0}'.format(local_file))

        with open(local_file, 'r') as f:
            contents = f.read().strip()

        if len(contents) == 0:
            raise Exception('Input file is empty: {0}'.format(local_file))

        return contents
