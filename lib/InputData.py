from typing import Union
import os
import sys


class InputData:
    def load(self) -> Union[str, None]:
        contents = self.__load_stdin()
        if not contents:
            # The first argument is the filename.
            sys.argv.pop(0)
            if len(sys.argv) == 1:
                contents = self.__load_file(sys.argv[0])
        return contents

    def __load_file(self, local_file: str) -> str:
        if not os.path.isfile(local_file):
            raise Exception('Input file does not exist: {0}'.format(local_file))

        with open(local_file, 'r') as f:
            contents = f.read().strip()

        if len(contents) == 0:
            raise Exception('Input file is empty: {0}'.format(local_file))

        return contents

    def __load_stdin(self) -> Union[str, None]:
        return None if sys.stdin.isatty() else sys.stdin.read().strip()
