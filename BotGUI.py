import tweepy
import threading
from urllib.request import urlopen
from time import sleep
from datetime import datetime
from tkinter import *
from tkinter import messagebox
from PIL import Image,ImageTk
from random import shuffle
from pathlib import Path
root=Tk()
root.config(highlightbackground='red',highlightcolor='red',highlightthickness=5) 
root.title("TwitterBot")
root.iconphoto(False,PhotoImage(file=f'{Path(__file__).parent.absolute()}\\img\\icon.png'))
class botThread(threading.Thread):
    def run(self):
        rt()
class checkThread(threading.Thread):
    def run(self):
        follow(followers)
def follow(x):
    global api,TxtBox
    while True:
        try:
            if kill:
                break
            y = x #Antigos seguidores
            x = api.followers_ids(myID) #Novos seguidores
            for person in y:
                if person not in x:
                    unf=person
                    break
            for person in x:
                if person not in y:
                    fol=person
                    break
            if len(x)>len(y): #Se tiver mais novos do que antigos
                TxtBox.insert(END,f"\n@{api.get_user(fol).screen_name} FOLLOWED YOU.")
            elif len(x)<len(y): #Se tiver mais antigos do que novos
                try:
                    TxtBox.insert(END,f"\n@{api.get_user(unf).screen_name} UNFOLLOWED YOU")
                    TxtBox.yview(END)
                except:
                    TxtBox.insert(END,f"\nYOU HAVE -{len(y)-len(x)} FOLLOWER(S).")
                    TxtBox.yview(END)
                    pass
            sleep(60.1) #60s cooldown
        except Exception as e:
            messagebox.showwarning("TwitterBot Error",e)
            continue #Reiniciar o loop
def rt():
    global api,terminal,search,TxtBox,api2,actualAt
    while True: #Loop infinito 
        try:
            if kill:
                break
            for names in search: #Fazer todas as buscas
                if kill:
                    break
                for tweet in tweepy.Cursor(api2.search,q=names,result_type="recent").items(500): #Procurar tweets
                    try:
                        if kill:
                            break
                        if (names in tweet.text) and (not tweet.retweeted) and (tweet.user.screen_name.lower()!=actualAt.lower()):
                            try:
                                api.retweet(tweet.id) #Retweetar
                                TxtBox.insert(END,f"\nRETWEET FROM @{tweet.user.screen_name}: {tweet.text}")
                                TxtBox.yview(END)
                            except:
                                pass
                    except tweepy.TweepError as e:
                        if e.api_code==136:
                            pass
                        else:
                            messagebox.showwarning("TwitterBot Error",e)
                            continue #Reiniciar forloop
        except Exception as e:
            messagebox.showwarning("TwitterBot Error",e)
            continue #Reiniciar o loop
def start():
    try:
        global kill,at,start,myID,followers,at_str,pic,username,the_at,stop,settings,api,terminal,TxtBox,Sbar,actualAt
        kill = False
        at.grid_forget()
        at_str.grid_forget()
        myID=api.get_user(at.get()).id
        followers = api.followers_ids(myID)
        pic_src=ImageTk.PhotoImage(Image.open(urlopen(api.get_user(myID).profile_image_url_https)))
        pic=Label(root,image=pic_src)
        pic.image=pic_src
        pic.grid(row=0,rowspan=2,column=0)
        username=Label(root,text=api.get_user(myID).name,font='bold')
        username.grid(row=0,column=2,sticky=W)
        actualAt=at.get()
        the_at=Label(root,text=f"@{actualAt}")
        the_at.grid(row=1,column=2,sticky=W)
        terminal.grid(row=3,column=0,columnspan=4)
        root.config(highlightbackground='#61CD3B',highlightcolor='#61CD3B',highlightthickness=5)
        start.grid_forget()
        stop.grid(row=0,rowspan=2,column=3)
        settings.grid_forget()
        Sbar = Scrollbar(terminal)
        Sbar.pack(side=RIGHT,fill="y")
        TxtBox = Text(terminal,yscrollcommand=Sbar.set,bg='black',fg='white',highlightthickness=0,borderwidth=0)
        TxtBox.pack(anchor=W)
        Sbar.config(command=TxtBox.yview)
        TxtBox.insert(END,f"{datetime.now().strftime('%c')}: BOT STARTED.")
        checkT.start() #Iniciar thread 
        botT.start() #Iniciar thread
    except Exception as e:
        print(e)
def stop():
    global kill,start,at,at_str,stop,pic,username,the_at,settings,terminal,TxtBox,Sbar
    kill=True
    TxtBox.pack_forget()
    Sbar.pack_forget()
    the_at.grid_forget()
    stop.grid_forget()
    pic.grid_forget()
    username.grid_forget()
    terminal.grid_forget()
    at_str.grid(row=0,column=1,sticky=E)
    at.grid(row=0,column=2)
    root.config(highlightbackground='red',highlightcolor='red',highlightthickness=5)
    start.grid(row=0,rowspan=2,column=3)
    settings.grid(row=3,column=3)
def access():
    global key1,key2,key3,key4,rtt,fav,cmnt,cmntTxt,content
    Path('C:\Program Files\Twitterbot').mkdir(exist_ok=True)
    keysFile=open(f'C:\\Program Files\\TwitterBot\\settings.txt','w')
    keysFile.write(f"key1={key1.get()}\nkey2={key2.get()}\nkey3={key3.get()}\nkey4={key4.get()}\nSearch={content.get()}")
    keysFile.close()
    readfile()
    top.destroy()
def settings():
    global key1,key2,key3,key4,rtt,fav,cmnt,cmntTxt,content,top
    top=Toplevel()
    top.title('Bot Settings')
    top.iconphoto(False,PhotoImage(file=f'{Path(__file__).parent.absolute()}\\img\\gears.png'))
    Label(top,text="Keys & Tokens").grid(row=0,column=0,columnspan=5,pady=10)
    Label(top,text='API Key:').grid(row=1,column=0,sticky=E,pady=5)
    key1=Entry(top,width=50)
    key1.grid(row=1,column=1,columnspan=5,pady=5,sticky=W)
    Label(top,text='API Key Secret:').grid(row=2,column=0,sticky=E,pady=5)
    key2=Entry(top,width=50)
    key2.grid(row=2,column=1,columnspan=5,pady=5,sticky=W)
    Label(top,text='Access Token:').grid(row=3,column=0,sticky=E,pady=5)
    key3=Entry(top,width=50)
    key3.grid(row=3,column=1,columnspan=5,pady=5,sticky=W)
    Label(top,text='Access Token Secret:').grid(row=4,column=0,sticky=E,pady=5)
    key4=Entry(top,width=50)
    key4.grid(row=4,column=1,columnspan=5,pady=5,sticky=W)
    Label(top,text="Search for tweets:").grid(row=5,column=0,sticky=E,pady=5)
    content=Entry(top,width=50)
    content.grid(row=5,column=1,columnspan=5,pady=5,sticky=W)
    Button(top,text='ENTER',pady=10,padx=20,command=access).grid(row=8,column=0,columnspan=5,pady=10)
def readfile():
    global keysFileContent,api,search,api2
    keysFileContent=open(f'C:\\Program Files\\TwitterBot\\settings.txt','r').readlines()
    if keysFileContent == []:
        settings()
    else:
        keys=[]
        for x in range(4):
            keys.append(keysFileContent[x][5:-1])
        search=keysFileContent[4][7:].split(';')
        shuffle(search)
        auth = tweepy.OAuthHandler(keys[0],keys[1])
        auth.set_access_token(keys[2],keys[3])
        auth2 = tweepy.AppAuthHandler(keys[0],keys[1])
        api=tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        api2=tweepy.API(auth2,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
if not Path('C:\\Program Files\\TwitterBot\\settings.txt').exists(): 
    settings()
else:
    readfile()
botT=botThread(daemon=True)
checkT=checkThread(daemon=True)
at_str=Label(root,text='@:')
at_str.grid(row=0,column=1,sticky=E)
at=Entry(root)
at.grid(row=0,column=2)
start=Button(root,text='START BOT',command=start)
start.grid(row=0,rowspan=2,column=3)
stop=Button(root,text='STOP BOT',command=stop)
terminal=LabelFrame(root,text='Terminal',bg='black',fg='white',padx=10)
settings=Button(root,text='Settings',fg='#0066CC',relief=FLAT,command=settings,padx=0,pady=0)
settings.grid(row=3,column=3)
root.mainloop()