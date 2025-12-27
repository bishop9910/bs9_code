from rich import print

class Data:
    def __init__(self, data:list[list[str]]) -> None:
        super().__init__()
        self.data = data

    def get_data(self) -> list[list[str]]:
        return self.data

    def get_data_by_index(self, index:str) -> str:
        index1 = index[0]
        index2 = index[1]
        if index2 == " ":
            return index1
        else:
            index1 = int(index1)
            index2 = int(index2)
        if self.data[index1][index2]:
            return self.data[index1][index2]
        else:
            return "not found"
        
    def get_data_by_value(self, value:str) -> str:
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if self.data[i][j] == value:
                    return str(i)+str(j)
        return "not found"
    
    def show_data(self) -> None:
        for i in self.data:
            for j in i:
                if j != "\n":
                    if j == None:
                            print(j, end=" ")
                    else:
                        if "a" <= j <= "z" or "A" <= j <= "Z":
                            out = f"[bold red]{j}[/bold red]"
                            print(out, end=" ")
                        else:
                            if j.isdigit():
                                out = f"[bold blue]{j}[/bold blue]"
                                print(out, end=" ")
                            else:
                                if j == "\\":
                                    out = "[bold green]\\"
                                    print(out, end=" ")
                                else:
                                    out = f"[bold green]{j}[/bold green]"
                                    print(out, end=" ")
                else:
                    print("[bold purple]\\n[/bold purple]", end=" ")
            print()
        return None