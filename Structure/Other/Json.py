from Structure.Helpers.custom_pointer_list import ChainStatement, OrStatement


def json_dump(self):
    if type(self) is str:
        return self

    sub_data = [part if type(part) is str else part.json_dump() for part in self.data]
    if type(self) is ChainStatement:
        return tuple(sub_data)
    if type(self) is OrStatement:
        return list(sub_data)


def json_load(inp):
    """
    converts the input into ChainStatements/OrStatements
    """

    if type(inp) is str:
        return inp

    sub_data = [part if type(part) is str else json_load(part) for part in inp]

    if type(inp) is tuple:
        return ChainStatement(*sub_data)
    if type(inp) is list:
        return OrStatement(*sub_data)