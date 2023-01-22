from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty

from kivymd.app import MDApp
from kivymd.theming import ThemableBehavior
from kivymd.uix.list import OneLineIconListItem, MDList

from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.tab import MDTabsBase

from kivymd.font_definitions import fonts
from kivymd.icon_definitions import md_icons

from kivymd.uix.label import MDLabel

from kivymd.uix.menu import MDDropdownMenu
from kivy.clock import Clock

from kivymd.uix.picker import MDDatePicker
import datetime
import calendar

from kivy.graphics import Color, Rectangle, Line, Ellipse
from random import random as r

from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

from kivy.uix.textinput import TextInput

import locale

# print(locale.getlocale())
print(locale.getdefaultlocale())


# internationalized Kivy Application
# https://github.com/tito/kivy-gettext-example
import gettext
from os.path import dirname, join

from kivy.app import App
from kivy.lang import Observable
from kivy.properties import StringProperty
import pymysql
from config import host, user, password, db_name

def idlim():
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            dic = []
            with connection.cursor() as cursor:
                select_all_rows = "SELECT idUsers FROM Users ORDER BY `idUsers` DESC LIMIT 1"
                cursor.execute(select_all_rows)
                # cursor.execute("SELECT * FROM `users`")
                rows = cursor.fetchall()
                print(rows)
                for row in rows:
                    print(row.values())

                for key in row.values():
                    dic.append(key)
                    return key+1


        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)

def database(arg, vall, tabl, quere):
    try:
        connection = pymysql.connect(
            host=host,
            port=3306,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        print("successfully connected...")
        print("#" * 20)

        try:
            dic = []
            with connection.cursor() as cursor:
                select_all_rows = "SELECT "+str(vall)+" FROM "+ str(tabl)+" WHERE "+ str(quere) +" =" + str(arg)
                cursor.execute(select_all_rows)
                # cursor.execute("SELECT * FROM `users`")
                rows = cursor.fetchall()
                print(rows)
                for row in rows:
                    print(row.values())

                for key in row.values():
                    dic.append(key)
                    return key


        finally:
            connection.close()

    except Exception as ex:
        print("Connection refused...")
        print(ex)


class Lang(Observable):
    observers = []
    lang = None

    def __init__(self, defaultlang):
        super(Lang, self).__init__()
        self.ugettext = None
        self.lang = defaultlang
        self.switch_lang(self.lang)

    def _(self, text):
        return self.ugettext(text)

    def fbind(self, name, func, args, **kwargs):
        if name == "_":
            self.observers.append((func, args, kwargs))
        else:
            return super(Lang, self).fbind(name, func, *args, **kwargs)

    def funbind(self, name, func, args, **kwargs):
        if name == "_":
            key = (func, args, kwargs)
            if key in self.observers:
                self.observers.remove(key)
        else:
            return super(Lang, self).funbind(name, func, *args, **kwargs)

    def switch_lang(self, lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = join(dirname(__file__), 'data', 'locales')
        locales = gettext.translation('langapp', locale_dir, languages=[lang])
        self.ugettext = locales.gettext
        self.lang = lang

        # update all the kv rules attached to this text
        for func, largs, kwargs in self.observers:
            func(largs, None, None)


tr = Lang("en")
# internationalized Kivy Application

# 1) download and install! http://gnuwin32.sourceforge.net/packages/gettext.htm
# https://mlocati.github.io/articles/gettext-iconv-windows.html
# 2) Copy files from "C:\Program Files (x86)\gettext-iconv\bin" to project folder!
# 3) run commands from Makefile


# Now all elements of interface are in file app_interface.kv
KV = open('app_interface.kv', 'r').read()


class ContentNavigationDrawer(BoxLayout):
    pass


class ItemDrawer(OneLineIconListItem):
    icon = StringProperty()
    text_color = ListProperty((0, 0, 0, 1))


class DrawerList(ThemableBehavior, MDList):
    def set_color_item(self, instance_item):
        """Called when tap on a menu item."""

        # Set the color of the icon and text for the menu item.
        for item in self.children:
            if item.text_color == self.theme_cls.primary_color:
                item.text_color = self.theme_cls.text_color
                break
        instance_item.text_color = self.theme_cls.primary_color


class Tab(FloatLayout, MDTabsBase):
    '''Class implementing content for a tab.'''


class ContentDialogSend(BoxLayout):
    pass


# https://stackoverflow.com/questions/2249956/how-to-get-the-same-day-of-next-month-of-a-given-day-in-python-using-datetime
def next_month_date(d):
    _year = d.year + (d.month // 12)
    _month = 1 if (d.month // 12) else d.month + 1
    next_month_len = calendar.monthrange(_year, _month)[1]
    next_month = d
    if d.day > next_month_len:
        next_month = next_month.replace(day=next_month_len)
    next_month = next_month.replace(year=_year, month=_month)
    return next_month


# https://kivy.org/doc/stable/examples/gen__canvas__canvas_stress__py.html



def draw_graph(wid, start_date, loan, months, interest, payment_type):
    # print(wid.x, wid.y)
    with wid.canvas:
        Color(.2, .2, .2, 1)
        Line(rectangle=(wid.x, wid.y, wid.width, wid.height), width=1)



def share(title, text):
    from kivy import platform

    print(platform)
    if platform == 'android':
        from jnius import autoclass

        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        Intent = autoclass('android.content.Intent')
        String = autoclass('java.lang.String')
        intent = Intent()
        intent.setAction(Intent.ACTION_SEND)
        intent.putExtra(Intent.EXTRA_TEXT, String('{}'.format(text)))
        intent.setType('text/plain')
        chooser = Intent.createChooser(intent, String(title))
        PythonActivity.mActivity.startActivity(chooser)


class cubeRubiks(MDApp):
    dialog = None
    lang = StringProperty('en')
    data_tables = None
    current_tab = 'tab1'
    payment_annuity = True
    menu = None # for recreate menu on lang change

    def on_lang(self, instance, lang):
        print('switched')
        tr.switch_lang(lang)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.theme_cls.primary_palette = "Brown"
        self.theme_cls.primary_hue = "A100"
        self.data_for_calc_is_changed = True

        self.screen = Builder.load_string(KV)
        # https://kivymd.readthedocs.io/en/latest/components/menu/?highlight=MDDropDownItem#center-position
        # menu_items = [{"icon": "git", "text": f"Item {i}"} for i in range(5)]
        menu_items = [{"icon": "format-text-rotation-angle-up", "text": tr._('annuity')},
                      {"icon": "format-text-rotation-angle-down", "text": tr._('differentiated')}]



    #https://kivymd.readthedocs.io/en/latest/components/menu/?highlight=MDDropdownMenu#create-submenu
    def update_menu(self):
        self.menu = None
        menu_items = [{"icon": "format-text-rotation-angle-up", "text": tr._('annuity')},
                      {"icon": "format-text-rotation-angle-down", "text": tr._('differentiated')}]
        self.menu = MDDropdownMenu(

            items=menu_items,
            position="auto",
            width_mult=4,
        )
        self.menu.bind(on_release=self.set_item)


    def on_focus(self, instance, value):
        if value:
            print('User focused', instance.name, instance.text)
            if instance.name == 'loan':
                self.screen.ids.loan.helper_text = "Please enter your username"
            elif instance.name == 'months':
                self.screen.ids.months.helper_text = "Please enter your datebirth"
            elif instance.name == 'interest':
                self.screen.ids.interest.helper_text = "Please enter only numbers, max 1000"
        else:
            print('User defocused', instance.name, instance.text)
            if instance.name == 'loan':
                self.screen.ids.loan.helper_text = ""
                if len(self.screen.ids.loan.text) > 9:
                    self.screen.ids.loan.text = self.screen.ids.loan.text[0:9]
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True
            elif instance.name == 'months':
                self.screen.ids.months.helper_text = ""
                if len(self.screen.ids.months.text) > 4:
                    self.screen.ids.months.text = self.screen.ids.months.text[0:4]
                if int(self.screen.ids.months.text) > 1200:
                    self.screen.ids.months.text = "1200"
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True
            elif instance.name == 'interest':
                self.screen.ids.interest.helper_text = ""
                if len(self.screen.ids.interest.text) > 4:
                    self.screen.ids.interest.text = self.screen.ids.interest.text[0:4]
                if float(self.screen.ids.interest.text) > 1000:
                    self.screen.ids.interest.text = "1000"
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True

    def validate_on_nums_input(self, instance_textfield, value):
        print(instance_textfield, value)
        # self.screen.ids.loan.error = True

    def set_item(self, instance_menu, instance_menu_item):
        def set_item(interval):
            self.screen.ids.payment_type.text = instance_menu_item.text
            instance_menu.dismiss()
            before_change = self.payment_annuity
            if tr._(self.screen.ids.payment_type.text) == tr._('annuity'):
                self.payment_annuity = True
            else:
                self.payment_annuity = False
            print(self.payment_annuity)
            if before_change != self.payment_annuity:
                print("value is changed for payment type")
                self.calc_1st_screen()
                self.data_for_calc_is_changed = True

        Clock.schedule_once(set_item, 0.5)

    def get_date(self, date):
        '''
        :type date: <class 'datetime.date'>
        '''
        pre_start_date = datetime.datetime.strptime(self.screen.ids.start_date.text, "%d-%m-%Y").date()
        print("Before: ", date, self.data_for_calc_is_changed, pre_start_date == date)
        self.screen.ids.start_date.text = date.strftime("%d-%m-%Y")  # str(date)
        if (pre_start_date != date):
            self.data_for_calc_is_changed = True
        print("After: ", date, self.data_for_calc_is_changed, pre_start_date == date)

    def build(self):
        # self.theme_cls.primary_palette = "Brown"
        # self.theme_cls.primary_hue = "A100"
        self.theme_cls.theme_style = "Light"  # "Dark"  # "Light"
        # return Builder.load_string(KV)
        return self.screen

    def calc_1st_screen(self):
       pass

    def on_start(self):

        self.calc_1st_screen()
        icons_item_menu_lines = {
            "account": "About author",
            "share-variant": "Share app",  # air-horn
            "shield-sun": "Dark/Light",
        }
        icons_item_menu_tabs = {
            "account": "Input",  # ab-testing
            "table-large": "Table",
            "chart-areaspline": "Graph",
            "chart-pie": "Chart",  # chart-arc
            "book-open-variant": "Sum",
        }
        for icon_name in icons_item_menu_lines.keys():
            self.root.ids.content_drawer.ids.md_list.add_widget(
                ItemDrawer(icon=icon_name, text=icons_item_menu_lines[icon_name])
            )

        pass

    def on_tab_switch(self, *args):
        self.current_tab = args[1].name
        # print(args)
        # print("tab clicked!" + instance_tab.ids.label.text)
        ############# instance_tab.ids.label.text = tab_text
        # print(instance_tab.ids.label.text)
        if self.data_for_calc_is_changed:
            self.calc_table(self, args)
            self.data_for_calc_is_changed = False
        pass

    def on_star_click(self):
        if self.lang == 'en':
            self.lang = 'ru'
        elif self.lang == 'ru':
            self.lang = 'en'
        print(self.current_tab)
        self.screen.ids.tabs.switch_tab(self.current_tab)
        self.calc_table(self)
        self.update_menu()
        pass

    def calc_table(self, *args):


        row_data_for_tab = []



        for i in range(1, idlim()):
            row_data_for_tab.append(
                [database(i, "idUsers", "Users", "idUsers"), database(i, "Login", "Users", "idUsers"), database(i, "First_Name", "Users", "idUsers"), database(i, "Email", "Users", "idUsers"),
                database(i, "idResults", "results", "idResults"), database(i, "Result_time", "results", "idResults")])



        # tab3


        # tab4


        # tab2
        # https://kivymd.readthedocs.io/en/latest/components/datatables/?highlight=datatable
        self.data_tables = MDDataTable(
            use_pagination=True,
            pagination_menu_pos='center',
            rows_num=idlim()-1,
            column_data=[
                ("№", dp(10)),
                (tr._('UserName'), dp(20)),
                (tr._('First_name'), dp(20)),
                (tr._('Email'), dp(20)),
                (tr._('Place'), dp(20)),
                (tr._('Time'), dp(20)),
            ],
            row_data=row_data_for_tab,
        )
        self.screen.ids.calc_data_table.clear_widgets()
        self.screen.ids.calc_data_table.add_widget(self.data_tables)

        # tab5

        pass

    def show_confirmation_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Share it:",
                type="custom",
                content_cls=ContentDialogSend(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL", text_color=self.theme_cls.primary_color
                    ),
                    MDFlatButton(
                        text="SEND", text_color=self.theme_cls.primary_color
                    ),
                ],
            )
        self.dialog.open()

    def share_it(self, *args):
        share("title_share", "this content to share!")


cubeRubiks().run()