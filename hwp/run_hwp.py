import win32com.client as win32
from io import BytesIO
import win32clipboard
import os 
# import psutil
import re
import pandas as pd 

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
        self.res=pd.DataFrame([self.res])
        
        
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
            for field in res.columns:
                self.hwp.PutFieldText(f"{field}{{{{{i}}}}}", str(res[field].iloc[i]))  

                
    def run(self):
        self.insert_word(self.res)
        # self.hwp.SaveAs(os.path.abspath(self.sav_path))
        
        print(self.sav_path)
        print(os.path.abspath(self.sav_path))
              
        self.hwp.SaveAs(os.path.abspath(self.sav_path), "HWPX", "lock:none")
        self.hwp.Quit()