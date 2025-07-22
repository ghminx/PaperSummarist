import win32com.client as win32
from io import BytesIO
import win32clipboard
import os 
import pandas as pd 
import tempfile
import pythoncom

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
        hwp.XHwpWindows.Item(0).Visible = False
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

    def remove_words(self):
        self.hwp.HAction.GetDefault("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.Execute("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.GetDefault("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HParameterSet.HFindReplace.Direction = self.hwp.FindDir("Forward")
        self.hwp.HParameterSet.HFindReplace.FindString = "*"
        self.hwp.HParameterSet.HFindReplace.ReplaceString = ""
        self.hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        self.hwp.HAction.Execute("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)

    def line(self):
        self.hwp.HAction.GetDefault("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.Execute("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.GetDefault("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HParameterSet.HFindReplace.Direction = self.hwp.FindDir("Forward")
        self.hwp.HParameterSet.HFindReplace.FindString = "###"
        self.hwp.HParameterSet.HFindReplace.ReplaceString = "\n"
        self.hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        self.hwp.HAction.Execute("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
                
    def run(self):
        self.insert_word(self.res)
        self.remove_words()
        self.line()
        self.hwp.SaveAs(os.path.abspath(self.sav_path))
              
        self.hwp.SaveAs(os.path.abspath(self.sav_path), "HWP", "lock:none")
        self.hwp.Quit()
        

class MakeResST():
    def __init__(self, frame_path, res) -> None:
        """
        Args:
            frame_path (str): Hwp Frame path
            res(dict): LLM 요약 결과
        """
        self.frame_path = frame_path
        self.res = pd.DataFrame([res])

        pythoncom.CoInitialize()  # ✅ COM 초기화 (중복 방지됨)
        self.hwp = self.hwp_open()

    def hwp_open(self):
        hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
        hwp.XHwpWindows.Item(0).Visible = False  # 배포용: True → False
        hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
        hwp.RegisterModule("Clipboard", "")  
        hwp.Open(os.path.abspath(self.frame_path))
        return hwp

    def insert_word(self):
        for _ in range(len(self.res) - 1):
            self.hwp.Run("PastePage")

        for i in range(len(self.res)):
            for field in self.res.columns:
                self.hwp.PutFieldText(f"{field}{{{{{i}}}}}", str(self.res[field].iloc[i]))

    def remove_words(self):
        self.hwp.HAction.GetDefault("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.Execute("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.GetDefault("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HParameterSet.HFindReplace.Direction = self.hwp.FindDir("Forward")
        self.hwp.HParameterSet.HFindReplace.FindString = "*"
        self.hwp.HParameterSet.HFindReplace.ReplaceString = ""
        self.hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        self.hwp.HAction.Execute("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)

    def line(self):
        self.hwp.HAction.GetDefault("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.Execute("ReplaceDlg", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HAction.GetDefault("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
        self.hwp.HParameterSet.HFindReplace.Direction = self.hwp.FindDir("Forward")
        self.hwp.HParameterSet.HFindReplace.FindString = "###"
        self.hwp.HParameterSet.HFindReplace.ReplaceString = "\n"
        self.hwp.HParameterSet.HFindReplace.ReplaceMode = 1
        self.hwp.HParameterSet.HFindReplace.IgnoreMessage = 1
        self.hwp.HAction.Execute("AllReplace", self.hwp.HParameterSet.HFindReplace.HSet)
                
                
    def run_and_return_file(self):
        self.insert_word()
        self.remove_words()
        self.line()
        
        with tempfile.NamedTemporaryFile(suffix=".hwp", delete=False) as tmp:
            tmp_path = tmp.name

        self.hwp.SaveAs(os.path.abspath(tmp_path), "HWP", "lock:none")
        self.hwp.Quit()
        return tmp_path