'''
author  :   monsef alahem (based on Dr.ally abbara algorithms)
email   :   m.alahem09@gmail.com
version :   1.0
start   :   09-08-2019

'''
import math

import kivy
kivy.require("1.9.0")

#necesary for utf
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from kivy.app import App
from kivy.clock import Clock
from kivy.compat import string_types
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.lang import Builder
from kivy.metrics import sp, dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup


#build app with kv language
Builder.load_string('''
<Converter>:

# config menu

    FloatLayout:
        id: menu
        text: 'menu'
        # position and size to the parent, root in this case
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        opacity: 1 if root.ismenu else 0

        Image:
            id: menu_bg
            size: menu.size
            pos: menu.pos
            #source: 'free.png'
            color: .2, .2, .2, .4
            allow_stretch: True

        # Button:
        #     id: close_menu
        #     text: 'X'
        #     size_hint: (.0, .07)
        #     pos_hint: {'x':.85, 'y':.93}
        #     on_press: root.hide_menu()

        Label:
            id: title
            #font_name: 'arial.ttf'
            text: "*date converter*" #utf code mean menu in arabic
            size_hint: (.66, .2)
            pos_hint: {'x':.17, 'y':.8}
            font_size: 40
            color: 1, 1, 0, 1

        Button:
            id: type_btn
            text: 'hijri'
            background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.08}
            on_press: root.change_type()
                

        BoxLayout:
            # position and size to the parent, menu in this case
            size_hint: (.9, .08)
            pos_hint: {'x':.05, 'y':.6}

            ScreenLabel:
                id: result
                size_hint: (1, 1)
                text: 'DD-MM-YYYY ex : 09-08-2019'

            # ConverterLabel:
            #     id: lbl_viw_siz
            #     text: 'void'
            #     markup: True
            #     # size_hint: (.25, .06)
            #     # pos: (0,440)




# custom keyboard

    GridLayout:
        id: kb
        size_hint: (.6, .40)
        pos_hint: {'x':.2, 'y':.2}
        rows: 6

        Button:
            text: u'1'
            on_press: root.enter_number(page_val, 1)
        Button:
            text: u'2'
            on_press: root.enter_number(page_val, 2)
        Button:
            text: u'3'
            on_press: root.enter_number(page_val, 3)

        Button:
            text: u'4'
            on_press: root.enter_number(page_val, 4)
        Button:
            text: u'5'
            on_press: root.enter_number(page_val, 5)
        Button:
            text: u'6'
            on_press: root.enter_number(page_val, 6)

        Button:
            text: u'7'
            on_press: root.enter_number(page_val, 7)
        Button:
            text: u'8'
            on_press: root.enter_number(page_val, 8)
        Button:
            text: u'9'
            on_press: root.enter_number(page_val, 9)

        Button:
            text: u'<-'
            #on_press: page_val.text = ''
            on_press: page_val.text = page_val.text[:-1]
        Button:
            text: u'0'
            on_press: root.enter_number(page_val, 0)
        Button:
            id: goto_page_btn
            #font_name: 'arial.ttf'
            #text: u'ok'#means done in arabic
            text: 'ok'
            on_press: root.convert(page_val)

        Button:
            text: u'clean'
            on_press: page_val.text = ''
            #on_press: page_val.text = page_val.text[:-1]
        ScreenLabel:
            id: page_val
            size_hint: (1, 1)
            text: ''
        ConverterLabel:
            opacity:0


    ''')



class Date:
    _hd = 0
    _hm = 0
    _hy = 0

    _gd = 0
    _gm = 0
    _gy = 0

    _day_week = 5

    _julien_day = 1

    weekday = ["dimanche", "lundi", "mardi", "mercredi", "jeudi",
     "vendredi", "samedi"]
    hijri_month = ["moharam", "safar", "rabii I", "rabii II", "joumada I", "joumada II",
     "rajab", "chaaban", "ramadan", "chawal", "dou al qiida", "dou al hijaa"]
    gregorien_month = ["janvier", "fevrier", "mars", "avril", "mai",
     "juin", "juillet","aout","septembre","octobre","novembre","decembre"]

    #def __init__(self, **kwargs):
    def __init__(self, type, day, month, year):

        if type == 'h': 
            self._hd = day
            self._hm = month
            self._hy = year
            self.hijri_to_julien()
            self.julien_to_gregorien()

        if type == 'g':
            self._gd = day
            self._gm = month
            self._gy = year
            self.gregorien_to_julien()
            self.julien_to_hijri()
            
    def hijri_to_julien(self):
        YYH = self._hy
        MMH = self._hm
        DDH = self._hd
        KH1 = math.floor((YYH * 10631 + 58442583)/30)
        KH2 = math.floor((MMH * 325 - 320)/11)
        KH3 = DDH - 1
        self._julien_day = KH1 + KH2 + KH3
        KHS1 = (self._julien_day + 1.5)
        KHS2 = (KHS1/7)
        KHS3 = KHS2 - math.floor(KHS2)
        self._day_week = round(KHS3*7 + 0.000000000317) - 1
        self._hy = YYH
        self._hm = MMH
        self._hd = DDH

    def julien_to_gregorien(self):
        Z = math.floor(self._julien_day+0.5)
        F = self._julien_day+0.5 - Z
        if Z < 2299161:
            A = Z
        else:
            I = math.floor((Z - 1867216.25)/36524.25)
            A = Z + 1 + I - math.floor(I/4)
        
        B = A + 1524
        C = math.floor((B - 122.1)/365.25)
        D = math.floor(365.25 * C)
        T = math.floor((B - D)/ 30.6001)
        RJ = B - D - math.floor(30.6001 * T) + F
        JJ = math.floor(RJ)
        if T < 13.5:
            MM = T - 1
        else:
            if T > 13.5:
                MM = T - 13 
        if MM > 2.5:
            AA = C - 4716 
        else:
            if MM < 2.5: 
                AA = C - 4715

        self._gd = JJ
        self._gm = MM
        self._gy = AA

    def gregorien_to_julien(self):
        YY = self._gy
        MM = self._gm
        DD = self._gd

        GGG = 1
        if YY < 1582:
            GGG = 0
        if YY <= 1582 and MM < 10:
            GGG = 0
        if YY <= 1582 and MM == 10 and DD < 5:
            GGG = 0
        self._julien_day = -1 * math.floor(7 * (math.floor((MM + 9) / 12) + YY) / 4)
        S = 1
        if (MM - 9)<0:
            S=-1
        A = abs(MM - 9)
        J1 = math.floor(YY + S * math.floor(A / 7))
        J1 = -1 * math.floor((math.floor(J1 / 100) + 1) * 3 / 4)
        self._julien_day = self._julien_day + math.floor(275 * MM / 9) + DD + (GGG * J1)
        self._julien_day = self._julien_day + 1721027 + 2 * GGG + 367 * YY - 0.5
        K1 = (self._julien_day + 1.5)
        K2 = (K1/7)
        K3 = K2 - math.floor(K2)
        self._day_week = round(K3*7 + 0.000000000317)
        self._gy = YY
        self._gm = MM
        self._gd = DD

    def julien_to_hijri(self):
        Z = (self._julien_day + 0.5)
        AH = math.floor((Z * 30 - 58442554)/10631)
        R2 = Z - math.floor((AH * 10631 + 58442583)/30)
        M = math.floor((R2 * 11 + 330)/325)
        R1 = R2 - math.floor((M * 325 - 320)/11)
        J = R1 +1
        self._hy = AH
        self._hm = M
        self._hd = J
    
    def check_hijri_date(self,day,month):
        if month > 12 or month <= 0:
            return False
        if day > 30 or day <= 0:
            return False
        return True

    def check_gregorien_date(self,day,month):
        months = [31,28,31,30,31,30,31,31,30,31,30,31]
        if month > 12 or month <= 0:
            return False
        if day > 0 and day <= months[int(month)-1] and month <= 12 and month > 0:
            return True
        return False

    def tell_day(self):
        if not self.check_gregorien_date(self._gd,self._gm):
            return 'invalid date'
        if not self.check_gregorien_date(self._hd,self._hm):
            return 'invalid date'
        return str(self.weekday[int(self._day_week)])\
        + ' '\
        + str(int(self._hd))\
        + ' '\
        + str(self.hijri_month[int(self._hm)-1])\
        + ' '\
        + str(int(self._hy))\
        + ' / '\
        + str(int(self._gd))\
        + ' '\
        + str(self.gregorien_month[int(self._gm)-1])\
        + ' '\
        + str(int(self._gy))\



#custom label with solid background
class ConverterLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(.5, .5, .5, 1)
            Rectangle(pos=self.pos, size=self.size)

#same here with black color
class ScreenLabel(Label):
    def on_size(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 1)
            Rectangle(pos=self.pos, size=self.size)

class Converter(FloatLayout):

    ismenu = 1
    iskb = 1
    isfirsttime = 1

    day = 1
    month = 1
    year = 1
    date_type = 'h'
    global ype
    
    #ti = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Converter, self).__init__(**kwargs)
        
    def update(self, dt):


        if self.isfirsttime:
            #self.hide_kb()
            self.isfirsttime = 0





    #functions for buttons


    def show_kb(self):
        if not self.iskb:
            self.ids.kb.opacity = 1
            self.ids.kb.size_hint_x = .6
            self.iskb = 1

    def hide_kb(self):
        if self.iskb:
            self.ids.kb.opacity = 0
            self.ids.kb.size_hint_x = .0
            self.iskb = 0





    def enter_number(self, page_val, number):
        page_val.text += (str)(number)
        if len(page_val.text) == 2 or len(page_val.text) == 5:
            page_val.text += (str)('-')
        # if (int)(page_val.text) > 604:
        #     page_val.text = u'604'
        # if page_val.text == '0':
        #     page_val.text = u''

    def convert(self, page_val):

        result = self.ids.result
        result.text = ''

        type_btn = self.ids.type_btn
        date_type = self.date_type

        day, month, year = page_val.text.split('-', 2)
        date = Date(date_type,int(day),int(month),int(year))

        page_val.text = ''
        result.text = (str)(date.tell_day())


    def change_type(self):
        type_btn = self.ids.type_btn
        if self.date_type == 'h':
            self.date_type = 'g'
            type_btn.background_color = 0,1,2,1
            type_btn.text = "gregorien"
        else:
            self.date_type = 'h'
            type_btn.background_color = 0,2,1,1
            type_btn.text = "hijri"







class ConverterApp(App):

    #window object of the app
    global Window
    #principal widget of the app
    global wdg


    def build(self):

        Window.set_title('Converter')
        self.title = 'Converter'
        self.icon = 'converter.png'
        self.wdg = Converter(size= Window.size)
        main_wdg = self.wdg

        
        
    # initializing graphic objects that can't be on kv language

        Clock.schedule_interval(main_wdg.update, 1.0 / 30.0)
        return main_wdg

    #when user exit the app auto-save his session
    def on_stop(self):
        pass


if __name__ == '__main__':
    ConverterApp().run()