# YZU_Auto_Select_Class Python version with OCR

this is just for YZU student.

## Install

1. PIL
2. python-tesseract

must to be installed.

## Setting

Modify the config.py to Login and Get the Class you want.
You can find the class info at

```
https://isdna1.yzu.edu.tw/CnStdSel/SelCurr/CosList.aspx 
```

You will find the info in the code for example

```
<a title="加選：CS312,A,3 ＵＮＩＸ系統概論" onclick="javascript:TmpSelCos('SelCos,CS312,A,1,F,3,Y,Chinese,CS312,A,3 ＵＮＩＸ系統概論,')"><img title="加選：CS312,A,3 ＵＮＩＸ系統概論" src="../Images/cls_sel_icon-2.gif" alt="" style="border-width:0px;"></a>
```

and the info of the class will be

```
SelCos,CS312,A,1,F,3,Y,Chinese,CS312,A,3 ＵＮＩＸ系統概論,
```