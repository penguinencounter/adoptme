"""a case function"""


def case(variable, possibilities: list, *functions, default=lambda *args: print("No default."), send: tuple):
    for i, x in enumerate(possibilities):
        if variable == x:
            print(f"Selected possibility {i+1} ({x}). Running function...")
            result = functions[i](*send)
            return result
    default(*send)

