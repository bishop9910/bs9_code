from rich import print
from global_vals import data_obj
from methods import split_string
from tqdm import tqdm


def decode(content:str) -> str:
    print("[blue]decoding...[/blue]")
    output:str = ""
    indexs:list[str] = split_string(content)
    with tqdm(total=len(indexs), desc="Decoding") as pbar:
        for i in indexs:
            e = data_obj.get_data_by_index(i)
            if e == 'not found':
                output += i[0]
            else:
                output += e
            pbar.update(1)
    print("[bold green]Content decoded successfully[/bold green]")
    return output