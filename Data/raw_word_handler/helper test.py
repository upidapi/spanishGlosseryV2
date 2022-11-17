data = []

# class Pointer(list):
#     def __init__(self, *args):
#         super().__init__(args)


class PointerList:
    def __init__(self, *args):
        self.data = list(args)

    def __getitem__(self, pointer: list | int):
        if type(pointer) is slice:
            return self.data
        if type(pointer) is int:
            pointer = [pointer]
        temp_var = self.data[pointer[0]]
        if type(temp_var) is str:
            return temp_var
        return PointerList.__getitem__(temp_var, [pointer[1:]])

    def __setitem__(self, pointer: list | int, value):
        if type(pointer) is slice:
            self.data = value
            return self.data
        if type(pointer) is int:
            pointer = [pointer]
        if len(pointer) == 1:
            self.data[pointer[0]] = value
        else:
            if type(self.data) is PointerList:
                sub_value = PointerList.__setitem__(self.data[pointer[0]], pointer[:-1], value)
                self.data[pointer[0]] = sub_value
            else:
                # leave room for a str index at the end
                self.data[pointer[0]] = self.data[pointer[-1]]
        return self.data

    def __repr__(self):
        out_str = ""
        for i, item in enumerate(self.data):
            if type(item) is PointerList:
                out_str += item.__repr__()
            if type(item) is str:
                out_str += f"'{item}'"
            else:
                out_str += item.__str__()

            if i + 1 < len(self.data):
                out_str += ", "
        return f"[{out_str}]"


x = PointerList('hello', PointerList('hello', 'wa'), 'wut')
x[[0]] = 2
print(x[:])


# class OrStatement(list):
#     def __init__(self, *args):
#         super().__init__(args)
#
#
# print(type(OrStatement('a')) is list)
#
#
# def get_pointer_data(pointer, data):
#     scope = data
#     for part in pointer:
#         # might be unnecessary
#         if scope == '':
#             return ''
#         else:
#             scope = scope[part]
#     return scope
#
#
# def set_pointer_data(new_data, pointer, data):
#     full_data = new_data
#
#     for i in list(range(len(pointer)))[::-1]:
#         step_up_data = get_pointer_data(pointer[:i], data)
#         step_up_data[pointer[i]] = full_data
#         full_data = step_up_data
#
#     return full_data


# def get_next_open(pointer, data):
#     last_place = pointer[-1]
#     scope = get_pointer_data(pointer[:-1], data)
#     # if at end go upp
#     triggers = (
#         scope == "",
#         len(scope) == last_place + 1
#         scope
#     )
#     if scope == "" or len(scope) + 1 == last_place:
#         return get_next_open(pointer[:-1], data)
#     else:
#
#
