import wx
from collections import namedtuple

LinesInput = namedtuple('Lines',['start','end','offset','count','layer'])

linesInput = LinesInput({'name':u"起点",'value':complex(0,0)},
         {'name':u"终点",'value':complex(0,1000)},
         {'name':u"偏移",'value':complex(100,100)},
         {'name':u"线数",'value':10},
         {'name':u"层数",'value':3},
         )
#Arcs = (u"起点",u"终点",u"圆心",u"线数",u"层数")


class Lines:
  @staticmethod  
  def GetLines(input):
    '''生成多线数据'''
    lines = []
    offset = (input.offset['value'] - input.start['value']) / input.count['value']
    for i in range(input.count['value'] - 1):
      #起点
      start = input.start['value'] + offset * i
      #终点
      end = input.end['value'] + offset * i
      lines.append((start,end))
    return lines
  
  @staticmethod  
  def GetCode(lines,layer):
    code = ''
    #按层数打印
    for l in range(layer):
      code += ';LAYER:%d\n' % l
      #打印每层
      for line in lines:
        #起点
        code += 'G0 F9000 X%d Y%d Z0\n' % (line[0].real,line[0].imag)
        #划线
        code += 'G1 F1800 X%d Y%d E4\n' % (line[1].real,line[1].imag)
    return code


class InputWindow(wx.Dialog):
  def __init__(self, parent, title, data = linesInput):
    wx.Dialog.__init__(self, parent, title=title, size=(400, 400))
    self.data = data
    self.InitUI()  
    self.ShowModal()

  def InitUI(self):  
    panel = wx.Panel(self)  
          
    vbox = wx.BoxSizer(wx.VERTICAL)
    #增加输入框
    for it in self.data:      
      hbox1 = wx.BoxSizer(wx.HORIZONTAL)
      st1 = wx.StaticText(panel,label=it['name'])
      hbox1.Add(st1,flag=wx.RIGHT | wx.ALIGN_CENTER_VERTICAL,border=12)
      if type(it['value']) == complex:
        tc1 = wx.TextCtrl(panel,value = str(it['value'].real))
        hbox1.Add(tc1,proportion=1)      
        tc2 = wx.TextCtrl(panel,value = str(it['value'].imag))
        hbox1.Add(tc2,proportion=1)
        it['ctrl'] = (tc1,tc2)
      else:
        tc = wx.TextCtrl(panel,value = str(it['value']))
        hbox1.Add(tc,proportion=1)  
        it['ctrl'] = tc

      vbox.Add(hbox1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP | wx.ALIGN_CENTER_VERTICAL,border=10)
      vbox.Add((-1,10))
          
    #增加代码框    
    hbox3 = wx.BoxSizer(wx.HORIZONTAL)  
    self.txtCode = wx.TextCtrl(panel, style=wx.TE_MULTILINE)  
    hbox3.Add(self.txtCode, proportion=1, flag=wx.EXPAND)  
    vbox.Add(hbox3, proportion=1, flag=wx.LEFT|wx.RIGHT|wx.EXPAND,border=10)    
    vbox.Add((-1, 25))  
  
    #增加按钮栏
    hbox5 = wx.BoxSizer(wx.HORIZONTAL) 
    btnCode = wx.Button(panel, label=u'代码', size=(70, 30))  
    hbox5.Add(btnCode)       
    btnOk = wx.Button(panel, label=u'确认', size=(70, 30))  
    hbox5.Add(btnOk, flag=wx.LEFT|wx.BOTTOM, border=5)  
    btnClose = wx.Button(panel, label=u'关闭', size=(70, 30))  
    hbox5.Add(btnClose, flag=wx.LEFT|wx.BOTTOM, border=5)  
    vbox.Add(hbox5, flag=wx.ALIGN_RIGHT|wx.RIGHT, border=10) 

    #绑定事件
    self.Bind(wx.EVT_BUTTON, self.OnCode, btnCode)
    self.Bind(wx.EVT_BUTTON, self.OnOk, btnOk)
    self.Bind(wx.EVT_BUTTON, self.OnClose, btnClose)
          
    panel.SetSizer(vbox)

  #生成代码
  def OnCode(self, event):  
    for it in self.data:
      if type(it['value']) == complex:
        it['value'] = complex(float(it['ctrl'][0].GetValue()),float(it['ctrl'][1].GetValue()))
      else:
        it['value'] = int(it['ctrl'].GetValue())  
    
    #生成多线数据
    self.txtCode.SetValue(Lines.GetCode(Lines.GetLines(self.data),self.data.layer['value']))
              

  def OnOk(self, event):
    self.Destroy()

  def OnClose(self,event):
    self.Destroy()

class MainWindow(wx.Frame):
  def __init__(self, parent, title):
    wx.Frame.__init__(self, parent, title=title, size=(300, 300))
    panel = wx.Panel(self, -1)
    self.button = wx.Button(panel, -1, u"按钮", pos=(50, 20))
    self.Bind(wx.EVT_BUTTON, self.OnClick, self.button) 
    
    self.Show(True)

  def OnClick(self, event):  
      dialog = InputWindow(None, 'Small Editor',linesInput)
        #self.button.SetLabel("Clicked")  

app = wx.App(False)
frame = MainWindow(None, 'Small Editor')
app.MainLoop() 
