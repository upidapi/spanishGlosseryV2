class PointerList:
    def __init__(self, *args):
        self.data = list(args)

    def __getitem__(self, pointer: list | int | slice):
        if type(pointer) is slice:
            return self.data[pointer]
        if type(pointer) is int:
            return self.data[pointer]
        if len(pointer) == 1:
            return self.data[pointer[0]]
        if len(pointer) == 0:
            return self

        sub_scope = self.data[pointer[0]]

        if type(sub_scope) is str:
            return sub_scope[pointer[1]]

        return sub_scope[pointer[1:]]

    def __setitem__(self, pointer: list | int, value):
        if type(pointer) is slice:
            self.data = value
            return self.data
        if type(pointer) is int:
            pointer = [pointer]

        change_data = self.data[pointer[0]]

        if len(pointer) == 1:
            self.data[pointer[0]] = value
        elif type(change_data) is str:
            self.data[pointer[0]] = change_data[:pointer[1]] + \
                                    value + \
                                    change_data[pointer[1] + 1:]
        else:
            self.data[pointer[0]][pointer[1:]] = value

        return self.data

    def __delitem__(self, pointer: list | int):
        if type(pointer) is int:
            pointer = [pointer]

        change_data = self.data[pointer[0]]

        if len(pointer) == 1:
            del self.data[pointer[0]]
        elif type(change_data) is str:
            self[pointer] = ''
        else:
            del change_data[pointer[1:]]

    def __iter__(self):
        for part in self.data:
            yield part

    def __len__(self):
        return len(self.data)

    def __eq__(self, other) -> bool:
        if issubclass(type(other), PointerList):
            if len(self) == len(other) and type(self) == type(other):
                return all(part == compare for part, compare in zip(self.data, other.data))
            return False
        else:
            return False
            # raise TypeError(f"cannot compare {type(self)} with {other} (anything not a subclass of PointerList)")

    def __bool__(self):
        return bool(self.data)

    def __repr__(self):
        out_str = ""
        for i, item in enumerate(self.data):
            if type(item) is str:
                out_str += f"'{item}'"
            else:
                out_str += item.__repr__()

            if i + 1 < len(self.data):
                out_str += ", "
        return f"[{out_str}]"

    def multi_line_print(self, indent=0):
        print(f'{"   " * indent}', end='')
        if all(type(part) is str for part in self.data):
            sub = ", ".join([f'"{part}"' for part in self.data])

            if type(self) is ChainStatement:
                print(f"[{sub}]", end='')
            elif type(self) is OrStatement:
                print(f"{{{sub}}}", end='')

        else:
            if type(self) is ChainStatement:
                print(f"[")
            elif type(self) is OrStatement:
                print(f"{{")

            for i, part in enumerate(self.data):
                if type(part) is str:
                    print(f'{"   " * (indent + 1)}', end='')
                    print(f'"{part}"', end='')
                else:
                    part.multi_line_print(indent+1)

                if i < len(self.data) - 1:
                    print(",")
                else:
                    print()

            print(f'{"   " * indent}', end='')
            if type(self) is ChainStatement:
                print(f"]", end='')
            elif type(self) is OrStatement:
                print(f"}}", end='')

        if indent == 0:
            print()


class OrStatement(PointerList):
    def __repr__(self):
        return f"*{super().__repr__()}*"


class ChainStatement(PointerList):
    def __repr__(self):
        return f"^{super().__repr__()}^"
