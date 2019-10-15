import socket
import threading
import tkinter
import tkinter.scrolledtext

localIP = "127.0.0.1"
locport = 20002
tamBuff = 1024

serverUDP = socket.socket(family = socket.AF_INET,type = socket.SOCK_DGRAM)
serverUDP.bind((localIP,locport))

def enviar():
    texto = cajaTexto.get()
    cajaTexto.delete(0,tkinter.END)
    message = str.encode(texto)
    dirServ = ("127.0.0.1",20001)

    todoTexto.config(state = "normal")
    todoTexto.tag_config("CR",foreground = 'red')
    todoTexto.insert(tkinter.INSERT,"SERVIDOR: ","CR")
    todoTexto.insert(tkinter.INSERT,texto)
    todoTexto.insert(tkinter.INSERT,"\n")
    todoTexto.config(state = "disabled")

    serverUDP.sendto(message,dirServ)

def limpio():
    todoTexto.config(state = "normal")
    todoTexto.delete("1.0",tkinter.END)
    todoTexto.config(state = "disabled")

def recibir():
    while(True):
        dataReceive = serverUDP.recvfrom(tamBuff)

        msgRecibido = dataReceive[0]
        #origenAdres = dataReceive[1]
        
        todoTexto.config(state = "normal")
        todoTexto.tag_config("CB",foreground = 'blue')
        todoTexto.insert(tkinter.INSERT,"CLIENTE: ","CB")
        todoTexto.insert(tkinter.INSERT,msgRecibido.decode())
        todoTexto.insert(tkinter.INSERT,"\n")
        todoTexto.config(state = "disabled")

mainW = tkinter.Tk()
mainW.configure(background = "purple")
mainW.title("Interfaz-Servidor")
mainW.geometry("400x287")

todoTexto = tkinter.scrolledtext.ScrolledText(mainW,height = 15,state = "disabled",width = 46)
todoTexto.place(x = 5,y = 5)

cajaTexto = tkinter.Entry(mainW,width = 39)
cajaTexto.place(x = 5,y = 260)

boton = tkinter.Button(mainW,command = enviar,text = "SEND",width = 8)
boton.place(x = 327,y = 256)

boton2 = tkinter.Button(mainW,command = limpio,text = "CLEAR",width = 8)
boton2.place(x = 255,y = 256)

t = threading.Thread(target = recibir)
t.start()
mainW.mainloop()