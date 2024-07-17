import json
import typing


T = typing.TypeVar('T')


class ModelParser(typing.Generic[T]):
    def parse_json(self, file: str, many=False) -> typing.List[T]:
        with open(file) as f:
            data = json.load(f)
        return self.parse(data, many=many)

    def parse(self, data: dict, many=False) -> typing.List[T]:
        if not many:
            return [self.perform_parse(data)]
        return [self.perform_parse(item) for item in data['items']]

    def perform_parse(self, item: dict) -> T:
        raise NotImplementedError
