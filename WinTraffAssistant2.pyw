import pyautogui
from random import randint
from tkinter import *
from tkinter import ttk
import time
import PIL.ImageGrab
import threading
import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if is_admin():
    # Global Variables
    MouseLocationListX = list()
    MouseLocationListY = list()
    PhaseLocationListX = list()
    PhaseLocationListY = list()
    Inputs = [0] * 38
    Phase_Assignment = [0] * 38
    Phase = [0] * 8
    Input_Status = [0] * 38
    Inputs_To_Be_Clicked = [0] * 38
    Det_Queue = [0] * 24
    Car_Speed = [0] * 24
    Car_Gaps = [0] * 24
    Random_Modifier = 10000
    Random_Requirement = [100] * 24
    Enable_Detector_List1 = [0] * 12
    Enable_Detector_List2 = [0] * 12
    Set_Det_Phase_List1 = [0] * 12
    Set_Det_Phase_List2 = [0] * 12
    Det_Queue_Message1 = [0] * 12
    Det_Queue_Message2 = [0] * 12
    Enable_PushButton_List = [0] * 8
    Enable_EVP_List = [0] * 4
    Enable_EVR_List = [0] * 2
    RR_Counter = 0
    RR_Interval = 0
    Set_RR_Timers = [0] * 3
    Keep_Alive = int()
    WinTraff_Input_Offset_X = [21, 42, 63, 84, 105, 126, 147, 168, 189, 210, 231, 252, 273, 294, 315, 336, 21, 42, 63,
                               84,
                               105, 126, 147, 168, 189, 210, 231, 252, 273, 294, 315, 336, 435, 456, 477, 498, 519, 540]
    WinTraff_Input_Offset_Y = [535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 535, 565, 565,
                               565, 565, 565, 565, 565, 565, 565, 565, 565, 565, 565, 565, 565, 565, 500, 500, 500, 500,
                               500, 500]
    WinTraff_Phase_Offset_X = [30, 70, 110, 150, 190, 230, 270, 310]
    WinTraff_Phase_Offset_Y = [175, 175, 175, 175, 175, 175, 175, 175]


    def input_lister():
        global Inputs
        global Phase_Assignment
        global Inputs_Message
        for i in range(0, len(Detector_List)):
            Inputs[i] = Detector_List[i].get()
        for i in range(0, len(Det_Phase_List)):
            Phase_Assignment[i] = Det_Phase_List[i].get()
        Inputs_Message.set("Set!")


    def position(i):
        global MouseLocation
        global WinTraff_Input_Offset_X
        global WinTraff_Input_Offset_Y
        global MouseLocationListX
        global MouseLocationListY
        global PhaseLocationListX
        global PhaseLocationListY
        global WinTraff_Phase_Offset_X
        global WinTraff_Phase_Offset_Y
        MouseLocation.set(pyautogui.position())
        mouse_location_string = MouseLocation.get()
        mouse_location_string = mouse_location_string.split(",")
        mouse_location_string_x = mouse_location_string[0]
        mouse_location_string_y = mouse_location_string[1]
        mouse_location_string_x = mouse_location_string_x.replace("(", "")
        mouse_location_string_y = mouse_location_string_y.replace(")", "")
        mouse_location_string_y = mouse_location_string_y.replace(" ", "")
        mouse_location_int_x = int(mouse_location_string_x)
        mouse_location_int_y = int(mouse_location_string_y)
        MouseLocationListX = [x + mouse_location_int_x for x in WinTraff_Input_Offset_X]
        MouseLocationListY = [x + mouse_location_int_y for x in WinTraff_Input_Offset_Y]
        PhaseLocationListX = [x + mouse_location_int_x for x in WinTraff_Phase_Offset_X]
        PhaseLocationListY = [x + mouse_location_int_y for x in WinTraff_Phase_Offset_Y]
        MouseLocation.set("Set!")


    def start_bind():
        root.bind("a", position)


    def end_bind():
        root.unbind("a")


    def get_phase_status():
        global Keep_Alive
        while Keep_Alive == 1:
            global PhaseLocationListX
            global PhaseLocationListY
            global Phase
            for i in range(0, 8):
                Phase[i] = str(PIL.ImageGrab.grab().load()[PhaseLocationListX[i], PhaseLocationListY[i]])
            time.sleep(0.5)


    def random_requirement():
        global Random_Requirement
        while Keep_Alive == 1:
            for i in range(0, 24):
                requirement = int(Veh_Modifier.get()) + randint(-int(Detector_Variance.get()),
                                                                int(Detector_Variance.get()))
                Random_Requirement[i] = requirement
            time.sleep(600)


    def random_modifier():
        global Random_Modifier
        global Random_Interval
        y = 1
        while Keep_Alive == 1:
            if y == 1:
                Random_Modifier = Random_Modifier - 1
                if Random_Modifier == 1:
                    y = 0
            if y == 0:
                Random_Modifier = Random_Modifier + 1
                if Random_Modifier == 10000:
                    y = 1
            Random_Interval.set(Random_Modifier / 10000)
            time.sleep(1)


    def queue():
        global Det_Queue
        for i in range(0, 24):
            if Inputs[i] == 1 \
                    and randint(1, 20000) <= (Random_Requirement[i] * (Random_Modifier / 10000)) \
                    and Det_Queue[i] <= 9:
                Det_Queue[i] = Det_Queue[i] + 1


    def rr_routine():
        global Dormant_Timer
        global Ped_Inhibit_Timer
        global RR_Preempt_Timer
        global RR_Counter
        global RR_Interval
        global Inputs_To_Be_Clicked
        global Inputs
        Dormant_Value = int(Dormant_Timer.get()) * 2
        Ped_Inhibit_Value = int(Ped_Inhibit_Timer.get()) * 2
        RR_Preempt_Value = int(RR_Preempt_Timer.get()) * 2
        if Inputs[36] == 1 and Inputs[37] == 1:
            if RR_Counter <= Dormant_Value and RR_Interval == 0:
                RR_Counter = RR_Counter + 1
            if RR_Counter >= Dormant_Value and RR_Interval == 0:
                RR_Counter = 0
                RR_Interval = 1
                Inputs_To_Be_Clicked[37] = 1
            if RR_Counter <= Ped_Inhibit_Value and RR_Interval == 1:
                RR_Counter = RR_Counter + 1
            if RR_Counter >= Ped_Inhibit_Value and RR_Interval == 1:
                RR_Counter = 0
                RR_Interval = 2
                Inputs_To_Be_Clicked[37] = 1
                Inputs_To_Be_Clicked[36] = 1
            if RR_Counter <= RR_Preempt_Value and RR_Interval == 2:
                RR_Counter = RR_Counter + 1
            if RR_Counter >= RR_Preempt_Value and RR_Interval == 2:
                RR_Counter = 0
                RR_Interval = 0
                Inputs_To_Be_Clicked[36] = 1


    def set_inputs():
        global Inputs_To_Be_Clicked
        global Det_Phase_List
        global Det_Queue
        global Car_Speed
        for i in range(0, 24):
            if Car_Speed[i] > 0 and Input_Status[i] == 1:
                Car_Speed[i] = Car_Speed[i] - 1
            if Car_Gaps[i] > 0 and Input_Status[i] == 0:
                Car_Gaps[i] = Car_Gaps[i] - 1
            if Inputs[i] == 1 \
                    and Car_Speed[i] == 0 \
                    and Input_Status[i] == 1 \
                    and Phase[(Phase_Assignment[i] - 1)] != '(255, 0, 0)' \
                    and Det_Queue[i] >= 1:
                Inputs_To_Be_Clicked[i] = 1
                Car_Speed[i] = randint(1, 4)
                Det_Queue[i] = Det_Queue[i] - 1
            if Inputs[i] == 1 \
                    and Det_Queue[i] >= 1 \
                    and Car_Gaps[i] == 0 \
                    and Input_Status[i] == 0:
                Inputs_To_Be_Clicked[i] = 1
                Car_Gaps[i] = randint(1, 4)
        for i in range(0, 8):
            if Inputs[i + 24] == 1 \
                    and Input_Status[i + 24] == 1:
                Inputs_To_Be_Clicked[i + 24] = 1
            if Inputs[i + 24] == 1 \
                    and randint(1, 20000) <= (int(Ped_Modifier.get()) * (Random_Modifier) / 10000) \
                    and Input_Status[i + 24] == 0:
                Inputs_To_Be_Clicked[i + 24] = 1
        for i in range(0, 4):
            if Inputs[i + 32] == 1 \
                    and randint(1, 20000) <= (int(EVP_Modifier.get()) * (Random_Modifier) / 10000) \
                    and Input_Status[i + 32] == 0:
                Inputs_To_Be_Clicked[i + 32] = 1
            if Inputs[i + 32] == 1 \
                    and randint(1, 25) == 1 \
                    and Input_Status[i + 32] == 1:
                Inputs_To_Be_Clicked[i + 32] = 1
        for i in range(0, 24):
            Det_Queue_List[i].set(Det_Queue[i])


    def clicker_function():
        global Inputs_To_Be_Clicked
        global Input_Status
        global MouseLocationListX
        global MouseLocationListY
        pyautogui.PAUSE = .01
        for i in range(0, 38):
            if Inputs_To_Be_Clicked[i] == 1 and Input_Status[i] == 0:
                pyautogui.click(x=MouseLocationListX[i], y=MouseLocationListY[i], clicks=1, button='left')
                Input_Status[i] = 1
                Inputs_To_Be_Clicked[i] = 0
            if Inputs_To_Be_Clicked[i] == 1 and Input_Status[i] == 1:
                pyautogui.click(x=MouseLocationListX[i], y=MouseLocationListY[i], clicks=1, button='left')
                Input_Status[i] = 0
                Inputs_To_Be_Clicked[i] = 0


    def thread_assign():
        global Keep_Alive
        Keep_Alive = 1
        threading.Thread.daemon = True
        a = threading.Thread(target=get_phase_status)
        a.start()
        b = threading.Thread(target=random_requirement)
        b.start()
        c = threading.Thread(target=random_modifier)
        c.start()
        d = threading.Thread(target=main_function)
        d.start()


    def main_function():
        global Clicker_Function
        global Keep_Alive
        Clicker_Function.set("Started!")
        try:
            while Keep_Alive == 1:
                start = time.time()
                queue()
                rr_routine()
                set_inputs()
                clicker_function()
                end = time.time()
                if (end - start) < 0.48:
                    time.sleep(0.5 - (end - start))
        except:
            Keep_Alive = 0
            Clicker_Function.set('Done!')


    root = Tk()
    root.title("WinTraff Assistant")

    MainFrame = ttk.Frame(root)
    DetectorFrame1 = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    DetectorFrame2 = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    PhaseFrame = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    PedestrianFrame = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    ButtonFrame = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    MessageFrame = ttk.Frame(MainFrame, borderwidth=5, relief="groove")
    RailFrame = ttk.Frame(MainFrame, borderwidth=5, relief="groove")

    MainFrame.grid(column=0, row=0)
    DetectorFrame1.grid(column=0, row=0, rowspan=2, sticky="W, N, E, S")
    DetectorFrame2.grid(column=1, row=0, rowspan=2, sticky="W, N, E, S")
    PedestrianFrame.grid(column=2, row=0, sticky="W, N, E, S")
    ButtonFrame.grid(column=0, row=2, columnspan=2, sticky="W, N, S")
    MessageFrame.grid(column=3, row=0, sticky="W, N, E")
    RailFrame.grid(column=2, row=1, sticky="W, N, E, S")

    MouseLocation = StringVar()
    Anchor = IntVar()
    Inputs_Message = StringVar()
    Clicker_Function = StringVar()
    Random_Interval = StringVar()

    Detector_List = [IntVar() for i in range(0, 38)]
    Det_Queue_List = [IntVar() for j in range(0, 24)]
    Det_Phase_List = [IntVar() for k in range(0, 24)]

    for i in range(0, 12):
        Enable_Detector_List1[i] = ttk.Checkbutton(DetectorFrame1, text="Detector " + str(i + 1),
                                                   variable=Detector_List[i],
                                                   onvalue=1, offvalue=0)
        Set_Det_Phase_List1[i] = OptionMenu(DetectorFrame1, Det_Phase_List[i], 1, 2, 3, 4, 5, 6, 7, 8)
        Det_Queue_Message1[i] = Message(DetectorFrame1, textvariable=Det_Queue_List[i], foreground="green", width=100)
        if i < 8:
            Enable_PushButton_List[i] = ttk.Checkbutton(PedestrianFrame, text="PushButton " + str(i + 1),
                                                        variable=Detector_List[i + 24], onvalue=1, offvalue=0)
        if i < 4:
            Enable_EVP_List[i] = ttk.Checkbutton(PedestrianFrame, text="EV" + str(i + 1),
                                                 variable=Detector_List[i + 32],
                                                 onvalue=1, offvalue=0)
        if i < 2:
            Enable_EVR_List[i] = ttk.Checkbutton(RailFrame, text="RR" + str(i + 1), variable=Detector_List[i + 36],
                                                 onvalue=1, offvalue=0)
    for i in range(12, 24):
        Enable_Detector_List2[i - 12] = ttk.Checkbutton(DetectorFrame2, text="Detector " + str(i + 1),
                                                        variable=Detector_List[i], onvalue=1, offvalue=0)
        Set_Det_Phase_List2[i - 12] = OptionMenu(DetectorFrame2, Det_Phase_List[i], 1, 2, 3, 4, 5, 6, 7, 8)
        Det_Queue_Message2[i - 12] = Message(DetectorFrame2, textvariable=Det_Queue_List[i], foreground="green",
                                             width=100)

    for i in range(0, 12):
        Enable_Detector_List1[i].grid(column=0, row=i, sticky="W")
        Set_Det_Phase_List1[i].grid(column=1, row=i, sticky="W")
        Det_Queue_Message1[i].grid(column=2, row=i, sticky="W")
        if i < 8:
            Enable_PushButton_List[i].grid(column=0, row=i, sticky="W")
        if i < 4:
            Enable_EVP_List[i].grid(column=0, row=i + 8, sticky="W")
        if i < 2:
            Enable_EVR_List[i].grid(column=0, row=i, sticky="W")
    for i in range(0, 12):
        Enable_Detector_List2[i].grid(column=0, row=i, sticky="W")
        Set_Det_Phase_List2[i].grid(column=1, row=i, sticky="W")
        Det_Queue_Message2[i].grid(column=2, row=i, sticky="W")

    Dormant_Timer = StringVar()
    Dormant_Timer.set("0")
    Ped_Inhibit_Timer = StringVar()
    Ped_Inhibit_Timer.set("0")
    RR_Preempt_Timer = StringVar()
    RR_Preempt_Timer.set("0")
    Detector_Variance = StringVar()
    Veh_Modifier = StringVar()
    Ped_Modifier = StringVar()
    EVP_Modifier = StringVar()
    Detector_Variance.set("370")
    Veh_Modifier.set("1848")
    Ped_Modifier.set("35")
    EVP_Modifier.set("14")
    Detector_Variance_Message = ttk.Entry(MessageFrame, textvariable=Detector_Variance).grid(column=0, row=4,
                                                                                             sticky="W, N, E, S")
    Veh_Modifier_Message = ttk.Entry(MessageFrame, textvariable=Veh_Modifier).grid(column=0, row=6, sticky="W, N, E, S")
    Ped_Modifier_Message = ttk.Entry(MessageFrame, textvariable=Ped_Modifier).grid(column=0, row=8, sticky="W, N, E, S")
    EVP_Modifier_Message = ttk.Entry(MessageFrame, textvariable=EVP_Modifier).grid(column=0, row=10,
                                                                                   sticky="W, N, E, S")
    Detector_Variance_Message = Message(MessageFrame, text="Det Variance (+/-)", width=100).grid(column=0, row=3,
                                                                                                 sticky="W")
    Veh_Modifier_Message = Message(MessageFrame, text="Veh Modifier", width=100).grid(column=0, row=5, sticky="W")
    Ped_Modifier_Message = Message(MessageFrame, text="Ped Modifier", width=100).grid(column=0, row=7, sticky="W")
    EVP_Modifier_Message = Message(MessageFrame, text="EVP Modifier", width=100).grid(column=0, row=9, sticky="W")

    Set_RR_Timers[0] = ttk.Entry(RailFrame, textvariable=Dormant_Timer).grid(column=0, row=3, sticky="W, N, E, S")
    Set_RR_Timers[1] = ttk.Entry(RailFrame, textvariable=Ped_Inhibit_Timer).grid(column=0, row=5, sticky="W, N, E, S")
    Set_RR_Timers[2] = ttk.Entry(RailFrame, textvariable=RR_Preempt_Timer).grid(column=0, row=7, sticky="W, N, E, S")
    Dormant_Message = Message(RailFrame, text="Dormant (sec)", width=100).grid(column=0, row=2, sticky="W")
    Ped_Inhibit_Message = Message(RailFrame, text="Ped Inhibit (sec)", width=100).grid(column=0, row=4, sticky="W")
    RR_Preempt_Message = Message(RailFrame, text="Preempt (sec)", width=100).grid(column=0, row=6, sticky="W")

    ListMaker = Button(ButtonFrame, text="Set Inputs", command=input_lister)
    EnableAnchor2 = Radiobutton(ButtonFrame, text="Lock Anchor", variable=Anchor, value=1, indicatoron=False,
                                command=end_bind)
    EnableAnchor = Radiobutton(ButtonFrame, text="Set Anchor", variable=Anchor, value=2, indicatoron=False,
                               command=start_bind)
    Start = Button(ButtonFrame, text="Start Clicker", command=thread_assign)
    Input_Lead = Message(MessageFrame, text="Inputs ", width=100)
    Inputs_Set = Message(MessageFrame, textvariable=Inputs_Message, foreground="green", width=100)
    Anchor_Lead = Message(MessageFrame, text="Anchor ", width=100)
    AnchorLocation = Message(MessageFrame, textvariable=MouseLocation, foreground="green", width=100)
    Clicker_Lead = Message(MessageFrame, text="Clicker ", width=100)
    Clicker_Set = Message(MessageFrame, textvariable=Clicker_Function, foreground="green", width=100)
    Random_Lead = Message(MessageFrame, text="Congestion", width=100)
    Random_Message = Message(MessageFrame, textvariable=Random_Interval, foreground="green", width=100)

    ListMaker.grid(column=0, row=0, sticky="W")
    EnableAnchor2.grid(column=1, row=0, sticky="W")
    EnableAnchor.grid(column=1, row=1, sticky="W")
    Start.grid(column=3, row=0, sticky="W")
    Input_Lead.grid(column=0, row=0, sticky="E")
    Inputs_Set.grid(column=1, row=0, sticky="W")
    Anchor_Lead.grid(column=0, row=1, sticky="E")
    AnchorLocation.grid(column=1, row=1, sticky="W")
    Clicker_Lead.grid(column=0, row=2, sticky="E")
    Clicker_Set.grid(column=1, row=2, sticky="W")
    Random_Lead.grid(column=0, row=11, sticky="E")
    Random_Message.grid(column=1, row=11, sticky="W")

    root.mainloop()

else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)