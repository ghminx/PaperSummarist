import pandas as pd 
import win32com.client as win32
import pandas as pd
from io import BytesIO
import win32clipboard
import os 
# import psutil
import re

class MakeRes():
    def __init__(self, frame_path, sav_path, res) -> None:
        """
        Args:
            frame_path (str): Hwp Frame path
            sav_path (str): result save path
            res(dict): result LLM
        """
        self.frame_path=frame_path
        self.sav_path=sav_path 
        self.res=res
        
        self.hwp=self.hwp_open()
        
    def hwp_open(self):
        hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
        hwp.XHwpWindows.Item(0).Visible = True
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.RegisterModule("Clipboard", "")  
        hwp.Open(os.path.abspath(self.frame_path))
        
        return hwp

    # 글자 삽입
    def insert_word(self, res):
    
        for _ in range(len(res) - 1):
            self.hwp.Run("PastePage")

        for i in range(len(res)):
            for k, v in res.items():
                    self.hwp.PutFieldText(f"{k}{{{{{i}}}}}", str(res[k]))   

    # 클립보드 초기화    
    def clear_clipborad(self):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.CloseClipboard()
                
    def run(self):
        self.clear_clipborad
        self.insert_word(self.res)
