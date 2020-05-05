# ENGR 498B - Engineering Design
# Team 19080
# Sponsered by Raytheon
# Basketball Shooting Machine (BSM)
# This script hopefully wirelessly connects the Raspberry pi to a laptop through sockets and using TCP.
# It then creates a Graphic User Interface (GUI) in which the user can request the BSM perform various tasks.


#!/usr/bin/python3
from tkinter import * # Import tkinter library
import socket # Import the socket module
import numpy as np
from scipy.optimize import fsolve
import math
import time


# Establish connection between RP and laptop
s=socket.socket() # Socket object
host = '172.20.10.7'
port = 50020 # Reserve Port
s.bind((host, port)) # Bind to the port

s.listen(5) # wait for the client connection
g = 9.8 #m/s^2
y = 2 #meters
while True:
    c,addr = s.accept()
    print("Got connection from", addr)
    c.send(b"Connected")


    # Main Window
    mainWin = Tk()
    mainWin.title("BSM - User Controller")
    mainWin.geometry('400x200')

    leftFrame = Frame(mainWin, height = 197, width = 197, bg ='light grey')
    leftFrame.pack(side=LEFT)
    rightFrame = Frame(mainWin, height = 197, width = 197, bg ='grey')
    rightFrame.pack(side=RIGHT)


    def EmerShutoffClicked():
        c.send(b"ShutOffNow")
        quit()
        
    
    def yesShoot():
        c.send(b"Shoot")
        shootingWin = Tk()
        shootingWin.title("Shooting")
        shootingWin.geometry('200x100')
        label = Label(shootingWin, text="Shooting, Please Wait...")
        label.pack()
        shootingWin.destroy


    def yesShutoff():
        c.send(b"ShutOffNow")
        c.close()
        quit()

    def manualPara():
        c.send(b"manParam")
        x = input("Enter in x distance to basket: ")
        x = float(x)
        def equations(p):
            theta, t, v = p
            f1 = (-v * math.cos(math.radians(theta)) * math.tan(math.radians(45))) + (-v * math.sin(math.radians(theta))) + (g * t) 
            f2 = y - (v * math.sin(math.radians(theta)) * t) + (.5 * g * t ** 2)
            f3 = x - (v * math.cos(math.radians(theta)) * t)
            return (f1, f2, f3)
        theta, t, v = fsolve(equations, (45, 5, 20))
        print ("Shooting Angle = %f" %theta)
        print("Time in the air = %f" %t)
        print("Initial Velocity = %f" %v)
        c.send(str(v).encode('utf8'))
        #distLbl.config(text="Distance from hoop: %f meters" %x)
        #velLbl.config(text="Calculated Shooting Velocity: %f m/s" %v)
        #angLbl.config(text="Calculated Shooting Angle: %f degrees" %theta)
        

    # Shot Window
    def shootClicked():
        shootWin = Tk()
        shootWin.title("Shooting GUI")
        shootWin.geometry('450x200')
        x = 0
        v = 0
        theta = 0
        distLbl = Label(shootWin, text="Distance from hoop: %f meters" %x)
        distLbl.pack()
        velLbl = Label(shootWin, text="Calculated Shooting Velocity: %f m/s" %v)
        velLbl.pack()
        angLbl = Label(shootWin, text="Calculated Shooting Angle: %f degrees" %theta)
        angLbl.pack()
        noButton = Button(shootWin, text="No", fg='red', width=7, command=shootWin.destroy)
        noButton.pack(side=RIGHT)
        yesButton = Button(shootWin, text="Yes", fg='green', width=7, command=yesShoot)
        yesButton.pack(side=RIGHT)
        manualButton = Button(shootWin, text="Enter parameteres manually", fg='orange', width=24, command = manualPara)
        manualButton.pack(side = LEFT)
        


    # Parameters Window
    #def calculateClicked():
     #   c.send(b"Calculate")
        
    #    calcWin = Tk()
    #    calcWin.title("Parameters GUI")
    #    calcWin.geometry('300x200')
    #    bottomFrame = Frame(calcWin)
    #    bottomFrame.pack(side=BOTTOM)
    #    distLbl = Label(calcWin, text="Distance from hoop: meters")
    #    distLbl.pack()
    #    velLbl = Label(calcWin, text="Calculated Shooting Velocity: m/s")
    #    velLbl.pack()
    #    angLbl = Label(calcWin, text="Calculated Shooting Angle: degrees")
    #    angLbl.pack()

    #   homeButton = Button(bottomFrame, text="Home", fg="black", width=12, command=calcWin.destroy)
    #    homeButton.pack(anchor=CENTER)


    # Shutoff Window
    def shutoffClicked():
        shutoffWin = Tk()
        shutoffWin.title("Shutoff GUI")
        shutoffWin.geometry('150x100')
        SOlbl = Label(shutoffWin, text="Shut off BSM?")
        SOlbl.pack()
        yesButton = Button(shutoffWin, text="Yes", fg='green', width=7, command=yesShutoff)
        yesButton.pack()
        noButton = Button(shutoffWin, text="No", fg='red', width=7, command=shutoffWin.destroy)
        noButton.pack()


    # Payload Window
    def payloadClicked():
        def BBclicked():
            PayloadSelection.configure(text="NCAA Basketball")
            c.send(b"NCAABB")
        def FBclicked():
            PayloadSelection.configure(text="Foam Ball")
            c.send(b"FoamBall")
        payloadWin = Tk()
        payloadWin.title("Payload GUI:")
        payloadWin.geometry('200x150')
        payLbl = Label(payloadWin, text="Payload Options: ")
        payLbl.pack()
        ncaaBBbutton = Button(payloadWin, text='NCAA Basketball', command = BBclicked)
        ncaaBBbutton.pack()
        FoamButton = Button(payloadWin, text='Foam Ball', command = FBclicked)
        FoamButton.pack()
        homeButton = Button(payloadWin, text="Home", fg="black", width=12, command=payloadWin.destroy)
        homeButton.pack(anchor=CENTER, side=BOTTOM)


    # HOME PAGE
    # Shoot button
    shootButton = Button(leftFrame, text="Shoot", fg="black", width=11, command = shootClicked)
    shootButton.pack(pady=5, padx=15)

    # Calculated parameters button
    #calculateButton = Button(leftFrame, text="Calculate", fg="black", width=11, command = calculateClicked)
    #calculateButton.pack(pady=5, padx=15)

    # Shutoff Machine Button
    shutoffButton = Button(leftFrame, text="Shut Off", fg="black", width=11, command = shutoffClicked)
    shutoffButton.pack(pady=5, padx=15)

    #Payload
    PayloadLbl = Label(rightFrame, text="Payload type: ")
    PayloadLbl.pack()
    PayloadSelection = Label(rightFrame, text="NCAA Basketball")
    PayloadSelection.pack()
    payloadButton = Button(rightFrame, text="Change Payload", width=14, command = payloadClicked)
    payloadButton.pack()

    #Emergency Shutoff
    EmergencyShutoff = Button(leftFrame, text="EMERGENCY SHUTOFF", fg="red", bg = "black", width=20, height= 5, command=EmerShutoffClicked)
    EmergencyShutoff.pack(pady=20, padx=20)

    mainWin.mainloop()

