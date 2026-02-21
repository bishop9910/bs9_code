from global_vals import global_vals
from rich import print
from tqdm import tqdm

def encode(string:str)->str:
    print("[blue]encoding...[/blue]")
    output:str = ""
    with tqdm(total=len(string), desc="Encoding") as pbar:
        for i in string:
            e:str = global_vals.data_obj.get_data_by_value(i)
            if e != 'not found':
                output += e
            else:
                output += (i + " ")
            pbar.update(1)
    print("[bold green]Content encoded successfully[/bold green]")
    return output