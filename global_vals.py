from data_form import data_0x1A5F, data_0x9910
from data_class import Data
from bs9_core import bishop9910_lib

class global_vals_lib(bishop9910_lib):
  def __init__(self) -> None:
    super().__init__()
    self.Textsuffix:list[str] = ['txt', 'js', 'html', 'css', 'md', 'ts', 'py', 'c', 'cpp']
    self.version:str = "1.2.185"
    self.date:str = "2026/04/15"
    self.data_obj:Data = Data(data_0x9910)
    self.coder_version:str = "data_0x9910"
    self.bs9_header_info:str = f"bs9_{self.version}_"
    self.bs9pck_header_info:str = f"bs9pck_{self.version}_"

global_vals: global_vals_lib = global_vals_lib()