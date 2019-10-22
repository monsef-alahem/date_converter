'''
author  :   monsef alahem (based on Dr.ally abbara algorithms)
email   :   m.alahem09@gmail.com
version :   1.0
start   :   09-08-2019

'''
import math

import kivy
kivy.require("1.11.1")

#necesary for utf
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')

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
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label



#import android, time





#build app with kv language
Builder.load_string('''
<Converter>:

#history page
    FloatLayout:
        id: history
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        opacity: 1 if root.ishist else 0

        ScrollView:
            id: hist_list
            pos: (0,0)
            BoxLayout:
                id: hist_box
                size_hint_x: 1
                size_hint_y: 0
                orientation: 'vertical'
                #on_touch_down: root.hide_kb()
        Button:
            id: ret_hist_btn
            text: 'return'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.7, 'y':.08}
            on_press: root.goto_main()
        Button:
            id: delete_btn
            text: 'delete'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.1, 'y':.08}
            on_press: root.activate_delete()


#main page
    FloatLayout:
        id: main
        size_hint: (1, 1)
        pos_hint: {'x':0, 'y':.0}
        orientation: 'vertical'
        opacity: 1 if root.ismain else 0




        Label:
            id: title
            #font_name: 'arial.ttf'
            text: "**" #utf code mean menu in arabic
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

        Button:
            id: hist_btn
            text: 'historique'
            #background_color: 0,2,1,1
            size_hint: (.2, .1)
            pos_hint: {'x':.4, 'y':.7}
            on_press: root.goto_hist()
                

        BoxLayout:
            size_hint: (.9, .08)
            pos_hint: {'x':.05, 'y':.6}

            ScreenLabel:
                id: result
                size_hint: (1, 1)
                text: 'DD-MM-YYYY ex : 09-08-2019'


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
                #on_press: root.print_coordinate()

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


converted_date = []

class Date:
    _hd = 0
    _hm = 0
    _hy = 0

    _gd = 0
    _gm = 0
    _gy = 0

    _day_week = 5

    _julien_day = 1
    _eqt = 0

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
    
    def check_hijri_date(self,day,month,year):
        if month > 12 or month <= 0:
            return False
        if day > 30 or day <= 0:
            return False
        return True

    def check_gregorien_date(self,day,month,year):
        months = [31,28,31,30,31,30,31,31,30,31,30,31]
        if year % 4 == 0:
            months[1] = 29
        if month > 12 or month <= 0:
            return False
        if day > 0 and day <= months[int(month)-1] and month <= 12 and month > 0:
            return True
        return False

    def tell_day(self):
        if not self.check_gregorien_date(self._gd,self._gm,self._gy):
            return "invalid date"
        if not self.check_gregorien_date(self._hd,self._hm,self._hy):
            return "invalid date"
        return (str(self.weekday[int(self._day_week)])\
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
        + str(int(self._gy)))

    # def calc_eqt(self):
    #     self.gregorien_to_julien()
    #     # jd is the given Julian date
    #     jd = self._julien_day
    #     d = jd - 2451545.0;  

    #     g = 357.529 + 0.98560028* d;
    #     q = 280.459 + 0.98564736* d;
    #     L = q + 1.915* math.sin(g) + 0.020* math.sin(2*g);

    #     R = 1.00014 - 0.01671* math.cos(g) - 0.00014* math.cos(2*g);
    #     e = 23.439 - 0.00000036* d;
    #     RA = math.atan2(math.cos(e)* math.sin(L), math.cos(L))/ 15; 

    #     # declination of the Sun
    #     D = math.asin(math.sin(e)* math.sin(L));  
    #     # equation of time
    #     eqt = q/15 - RA;
    #     return eqt

    #     # latitude (L)
    #     # longitude (Lng)
    #     # equation of time (EqT)
    #     # declination of the Sun (D)
    #     # Dhuhr = 12 + TimeZone - Lng/15 - calc_eqt()



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

    #bolean variables
    ishist = 0
    ismain = 1
    iskb = 1
    isfirsttime = 1
    isdelete = 0

    day = 1
    month = 1
    year = 1
    date_type = 'h'
    
    #ti = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(Converter, self).__init__(**kwargs)
        
    def update(self, dt):


        if self.isfirsttime:
            #self.hide_kb()
            self.isfirsttime = 0


        i = len(self.ids.hist_box.children)
        self.ids.hist_box.size_hint_y = .1 * (i + 0)
        #self.ids.hist_box.children[0].draw()




    #functions for buttons


    def show_main(self):
        if not self.ismain:
            self.ids.main.opacity = 1
            self.ids.main.size_hint_x = 1
            self.ismain = 1
    def show_hist(self):
        if not self.ishist:
            self.ids.history.opacity = 1
            self.ids.history.size_hint_x = 1
            self.ishist = 1

    def hide_main(self):
        if self.ismain:
            self.ids.main.opacity = 0
            self.ids.main.size_hint_x = .0
            self.ismain = 0
    def hide_hist(self):
        if self.ishist:
            self.ids.history.opacity = 0
            self.ids.history.size_hint_x = .0
            self.ishist = 0

    def goto_main(self):
        self.hide_hist()
        self.show_main()
        if self.isdelete:
            self.isdelete = 0
            self.ids.delete_btn.background_color = 1,1,1,1
    def goto_hist(self):
        self.hide_main()
        self.show_hist()

    def activate_delete(self):
        if self.isdelete:
            self.isdelete = 0
            self.ids.delete_btn.background_color = 1,1,1,1
        else :
            self.isdelete = 1
            self.ids.delete_btn.background_color = 3,0,0,1
    
    def auto_destruct(self, instance):
        if self.isdelete :
            converted_date.pop(int(instance.id))
            self.ids.hist_box.remove_widget(instance)
            print(instance.id + ' deleted')
        #print(instance.id[3])
        #converted_date[] = 
        #size = len(self.ids.hist_box.children)

        #self.ids.hist_box.ask_update()
        #self.ids.hist_box.canvas.draw()
    #for i in range(len(self.ids.hist_box.children)):
            #self.ids.hist_box.children[i].canevas.update()
            #self.ids.hist_box.children[i].draw()
        #pass
        #self.ids.hist_box.draw_point()



    def print_coordinate(self):
                    self.ids.page_val.text = 'hello'
                    # date = Date('g',int(12),int(12),int(2019))
                    # Dhuhr = 12 + 1 - 33.4567/15 - date.calc_eqt()

                    # ate = int(Dhuhr/1440)
                    # Hour = int((Dhuhr-ate*1440)/60)

                    # mint = int(Dhuhr-ate*1440)
                    # #mint = int((Dhuhr-ate*1440)-60*Hour)


                    # self.ids.page_val.text = str(Dhuhr)
        #self.ids.page_val.text = str(Hour) + str(mint)
        #droid = android.Android()
        #droid.startLocating()
        # print('reading GPS ...')
        # event= droid.eventWaitFor('location', 1000)
        # while 1:
        #     try :
        #         provider = event.result['data']['gps']['provider']
        #         if provider == 'gps':
        #             lat = str(event['data']['gps']['latitude'])
        #             lng = str(event['data']['gps']['longitude'])
        #             latlng = 'lat: ' + lat + ' lng: ' + lng
        #             print(latlng)
        #             self.ids.page_val.text = latlng
        #             break
        #         else:
        #             continue
        #     except KeyError:
        #        continue

    def enter_number(self, page_val, number):
        page_val.text += (str)(number)
        if len(page_val.text) == 2 or len(page_val.text) == 5:
            page_val.text += (str)('-')


    def convert(self, page_val):

        result = self.ids.result
        result.text = ''

        type_btn = self.ids.type_btn
        date_type = self.date_type

        if len(page_val.text) < 7 :
                result.text = "write like DD-MM-YYYY ex : 09-08-2019"
                return
        else :
            if page_val.text[2] != '-' or page_val.text[5] != '-' :
                result.text = "invalid date"
                return
        day, month, year = page_val.text.split('-', 2)
        date = Date(date_type,int(day),int(month),int(year))

        page_val.text = ''
        result.text = (str)(date.tell_day())

        #append it to history
        if result.text != "invalid date" :
            global converted_date
            size = len(converted_date)
            size2 = len(self.ids.hist_box.children)
            converted_date.append(result.text)
            
            btn = Button(text= converted_date[size], id= str(size))
            btn.bind(on_press= self.auto_destruct)
            self.ids.hist_box.add_widget(btn, size2)



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

        #restore last session auto-save
        try:
            f = open("save.dat")
            count = int(f.readline())
            for i in range(count):
                line = f.readline()
                #remove newline
                #size = len(converted_date[i])
                if line[int(len(line))-1] == '\n' :
                    line = line[:-1]
                converted_date.append(line)
                print(converted_date[i])
                #btn = Button(text= 'btn'+str(i), id= 'btn'+str(i), on_press= lambda a:self.wdg.auto_destruct())
                #btn = Button(text= converted_date[i], id='btn'+str(i))
                btn = Button(text= converted_date[i], id = str(i))
                btn.bind(on_press= self.wdg.auto_destruct)
                #btn = Button(text= converted_date[i], id= 'btn'+str(i))
                main_wdg.ids.hist_box.add_widget(btn, len(main_wdg.ids.hist_box.children))
            for i in range(10):
                img = Label(text= '')
                main_wdg.ids.hist_box.add_widget(img, 0)
            # main_wdg.ids.hist_box.size_hint_y= .1 * (i + 1)
            #btn0 = self.wdg.ids.btn0
            f.close()
        except:
            pass
        #main_wdg.ids.hist_box.remove_widget(main_wdg.ids.btn1)
        #print(main_wdg.ids.hist_box.children[0].id)
        print('kkjkjkkjk')

        # for i in range(0, 7):
        #     btn = Label(text= 'label')
        #     main_wdg.ids.hist_box.add_widget(btn, len(main_wdg.ids.hist_box.children))
        
        
    # initializing graphic objects that can't be on kv language

        Clock.schedule_interval(main_wdg.update, 1.0 / 30.0)
        return main_wdg

    #when user exit the app auto-save his session
    def on_stop(self):
        f = open("save.dat", "w")
        f.write(str(len(converted_date)))  
        for i in range(len(converted_date)):
            f.write("\n")
            f.write(converted_date[i])
        f.close()


if __name__ == '__main__':
    ConverterApp().run()