print("Select the mode from the following Choices:\n1)Receiver\n2)Sender")
mode = input()

if mode=="1": #RCV
    print("Receiving Selected!")
    # goto listening mode and answer udp req
elif mode=="2": #SND
    print("Sending Selected!")
    # goto sending mode for clients
else:
    print("The Input")
