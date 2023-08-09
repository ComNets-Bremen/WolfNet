from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.button import MDRaisedButton
from savetofile import MyRecord
from kivy.core.window import Window


class Example(MDApp):
    def build(self):
        record = MyRecord.showdata()       
        self.data_tables = MDDataTable(
            use_pagination=True,
            #check=True,
            column_data=[
                ("ID", dp(10)),
                ("Time", dp(25)),
                ("Sender ID", dp(25)),
                ("Receiver ID", dp(25)),
                ("Broadcast", dp(20)),
                ("Percent", dp(15)),
                ("Volt", dp(15)),
                ("Duration", dp(20)),
                ("Freq", dp(20)),
                ("RSSI", dp(20)),
                ("SNR", dp(20)),
            ],
            row_data=[
                (r.id, r.time, r.sendaddress, r.recaddress, r.broadcast, r.batteryperc, r.batteryvolt, r.duration, r.frequency, r.rssi, r.snr) for r in record            
            ],
            elevation=2,
        )
        self.data_tables.bind(on_row_press=self.on_row_press)
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def on_row_press(self, instance_table, instance_row):
        '''Called when a table row is clicked.'''
        print(instance_table, instance_row)
        
Window.maximize()
Example().run()
    