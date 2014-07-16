#! /usr/bin/env python
#coding=utf-8
import socket
import string
import struct
import win32api
import time
import random
import argparse

class DefaultMessage:
    def __init__(self,Rwcog=0,Ident=107,Param=0,Tag=0,Series=0):
        self.Rwcog = Rwcog #i
        self.Ident = Ident#2001 #H
        self.Param = Param #H
        self.Tag = Tag #H
        self.Series = Series #H
        
def Encode6BitBuf(msg):
    nRestCount = 0
    btRest = 0
    nDestPos = 0
    pDest = []
    for i in range(0,len(msg)):
        if nDestPos >= 12000: break
        btCh = ord(msg[i])
        btMade = ((btRest | (btCh >> (2 + nRestCount))) & 63) 
        btRest = ((( btCh << (8 - (2 + nRestCount))) >> 2)  & 63)
        nRestCount = nRestCount + 2

        if nRestCount < 6:
            pDest.insert(nDestPos,chr(btMade + 60))
            nDestPos = nDestPos + 1
        else:
            if nDestPos < 12000 - 1:
                pDest.insert(nDestPos,chr(btMade + 60))
                pDest.insert(nDestPos+1,chr(btRest + 60))
                nDestPos = nDestPos + 2
            else:
                pDest.insert(nDestPos,chr(btMade + 60))
                nDestPos = nDestPos + 1
            nRestCount = 0
            btRest = 0
    if nRestCount > 0:
        pDest.insert(nDestPos,chr(btRest + 60))
        nDestPos = nDestPos + 1
   # pDest.insert(nDestPos,chr(0))
    return pDest

def Decode6BitBuf(rmsg):
    Masks = [252,248,240,224,192]
    nBitPos = 2
    nMadeBit = 0
    nBufPos = 0
    btTmp = 0
    pbuf = []
    for i in range(0,len(rmsg)):
        if (ord(rmsg[i]) - 60) >= 0:
            btCh = ord(rmsg[i]) - 60
        else:
            nBufPos = 0
            break
        if nBufPos >= 100:break
        if (nMadeBit + 6) >= 8:
            btByte = btTmp | (( btCh & 63) >> (6 - nBitPos))
            pbuf.insert(nBufPos,chr(btByte))
            nBufPos = nBufPos + 1
            nMadeBit =0
            if nBitPos < 6:
                nBitPos = nBitPos + 2
            else:
                nBitPos =2
                continue
        btTmp = (btCh << nBitPos) & Masks[nBitPos-2]
        nMadeBit = nMadeBit + 8 - nBitPos
    #pbuf.insert(nBufPos,chr(0)) 
    return pbuf

def EncodeString(strmsg):
    resultmsg =""
    resultmsg = resultmsg.join(Encode6BitBuf(strmsg))
    #resultmsg = struct.unpack('s',resultmsg)
    return resultmsg

def DecodeString(strmsg):
    resultmsg =""
    resultmsg = resultmsg.join(Decode6BitBuf(strmsg))
    return resultmsg
    
def EncodeMessage(msg):
    strsendmsg = ""
    strdefalutmsg = struct.pack('iHHHH', msg.Rwcog, msg.Ident, msg.Param, msg.Tag, msg.Series)
    strsendmsg = strsendmsg.join(Encode6BitBuf(strdefalutmsg))
    return strsendmsg

def DecodeMessage(rmsg):
    strecimsg = ""
    strecimsg = strecimsg.join(Decode6BitBuf(rmsg))
    recimsgstr = struct.unpack('iHHHH',strecimsg)
    return recimsgstr
def DecodeMessagePacket(data):
    msglist = []
    if((data[1] == '+') or ( len(data) < 16)):
        return msglist
    sDefMsg = data[1:17]
    sBodyMsg = data[17:-1]
    msglist.append(DecodeMessage(sDefMsg))
    if sBodyMsg == "":
        msglist.append("")
    else:
        msglist.append(DecodeString(sBodyMsg))
    return msglist
def EncodeMessagePacket(code,sDefMsg,sBodyMsg = ""):
    if sDefMsg == "":
        msg = '#' + str(code) + EncodeString(sBodyMsg) + '!'
    else:
        msg = '#' +str(code) + EncodeMessage(sDefMsg) + EncodeString(sBodyMsg) + '!'
    return msg;

def MakeLong(x,y):
    return x | y << 16

def GetNextPosXY(dir,x,y):
    if dir ==0:
        x = x
        y = y-1
        return (x,y)
    elif dir == 1:
        x = x+1
        y = y-1
        return (x,y)
    elif dir == 2:
        x= x+1
        y = y
        return (x,y)
    elif dir == 3:
        x = x+1
        y = y+1
        return (x,y)
    elif dir == 4:
        x = x
        y = y+1
        return (x,y)
    elif dir == 5:
        x = x-1
        y = y+1
        return (x,y)
    elif dir == 6:
        x = x-1
        y = y
        return (x,y)
    elif dir == 7:
        x = x-1
        y = y-1
        return (x,y)


if __name__ == '__main__':

##    parser = argparse.ArgumentParser()
##    parser.add_argument('-u', action = "store", dest = "username")
##    parser.add_argument('-p', action = "store", dest = "password")
##    args = parser.parse_args()
##    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##    #服务器的主机名和端口
##    host="192.168.40.220"
##    port=7000
##    username =args.username
##    psw = args.password
##    print "asda:" + str(MakeLong(303,634)) 
##    msg = DefaultMessage()
##    try:
##        s.connect((host,port))
##    except socket.error:
##        print "连接失败"
##
##    msg11 = EncodeMessagePacket(1,msg)
##    print '发送:' + msg11
##    try:
##        s.sendall(msg11)
##    except socket.error:
##            print 'Send failed'
##    data=s.recv(1024)
##    print "接收: %s"  %data
##    print DecodeMessagePacket(data)
##
##    servername = DecodeMessagePacket(data)[1][:5]
##    msgSelectServer = DefaultMessage(0,104,0,0,0)
##    msg12 = EncodeMessagePacket(2,msgSelectServer,servername)
##    print '发送:' + msg12
##    try:
##        s.sendall(msg12)
##    except Exception:
##            print 'Send failed'
##    data = s.recv(1024)
##    print "接收: %s" % data
##   
##    print DecodeMessagePacket(data)
##    if DecodeMessagePacket(data)[0][1] == 530:
##        try:
##            msglogin = DefaultMessage(0,2001,0,0,0)
##            sendloginmsg = EncodeMessagePacket(3,msglogin,username + '/' + psw)
##            print '发送:' + sendloginmsg
##            s.sendall(sendloginmsg)
##        except socket.error:
##            print "Send failed"
##        data = s.recv(1024)
##        print "接收: %s" % data
##        datalist =  DecodeMessagePacket(data)
##        print datalist
##        if datalist[0][1] == 529:
##            s.close()
##            sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##            newhost = datalist[1].split('/')[0]
##            newport = int(datalist[1].split('/')[1])
##            Certification = datalist[1].split('/')[2]
##            print newhost,newport
##            try:
##
##                sock.connect((newhost,newport))
##                try:
##                    sysmsgdefault = DefaultMessage(0,100,0,0,0)
##                    sysmsg = EncodeMessagePacket(4,sysmsgdefault,username + '/' + Certification)
##                    print '发送:' + sysmsg
##                    sock.sendall(sysmsg)
##                except socket.error:
##                    print "发送失败"
##                data = sock.recv(1024)
##                print "接收: %s" %data
##                datalist =  DecodeMessagePacket(data)
##                print datalist
##                if '*' in datalist[1].split('/')[0]:
##                    rolename = datalist[1].split('/')[0][1:]
##                else:
##                    rolename = datalist[1].split('/')[0]
##                print rolename
##                try:
##                    queryroguemsgde = DefaultMessage(0, 50062, 0, 0, 0)
##                    queryroguemsg = EncodeMessagePacket(5,queryroguemsgde)
##                    print '发送:' + queryroguemsg
##                    sock.sendall(queryroguemsg)
##                except socket.error:
##                    print "send failed!"
##                data = sock.recv(1024)
##                print "接收: %s" %data
##                datalist = DecodeMessagePacket(data)
##                print datalist
##                try:
##                    randomcodemsgde = DefaultMessage(0, 108, 32, 0, 0)
##                    randomcodemsg = EncodeMessagePacket(6,randomcodemsgde)
##                    print '发送:' + randomcodemsg
##                    sock.sendall(randomcodemsg)
##                except socket.error:
##                    print "send failed!!!"
##                data = sock.recv(1024)
##                print "接收: %s" %data
##                datalist = DecodeMessagePacket(data)
##                print datalist
##                try:
##                    whispermsgde = DefaultMessage(0,103,0,0,0)
##                    whispermsg = EncodeMessagePacket(7,whispermsgde,username +'/' + rolename)
##                    print '发送:' + whispermsg
##                    sock.sendall(whispermsg)
##                except socket.error:
##                    print "send failed!!!"
##                data = sock.recv(1024)
##                print "收到: %s" %data
##                datalist = DecodeMessagePacket(data)
##                print datalist
##                if datalist[0][1] == 525:
##                    sock.close()
##                    sockt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
##                    newhost = datalist[1].split('/')[0]
##                    newport = int(datalist[1].split('/')[1])
##                    print newhost,newport
##                    try:
##                        sockt.connect((newhost,newport))
##                        try:
##                            startplaymsg = '**'+ username + '/' + rolename + '/'+str(int(Certification) ^ 1051903436)+'/'+str(int(Certification) ^ 1420911613)+'/'+str(134729835)+'/0'
##                            startplaymg = EncodeMessagePacket(8,"",startplaymsg)
##                            print '发送: %s' %startplaymg
##                            sockt.sendall(startplaymg)
##                        except socket.error:
##                            print "send failed!!!!"
##                        data = sockt.recv(1024)
##                        print "收到: %s" %data
##                        datalist = DecodeMessagePacket(data)
##                        print datalist
##                        print datalist[1].decode('gb2312').encode('utf-8')
##                        try:
##                            noticemsgde = DefaultMessage(win32api.GetTickCount(),1018,0,0,0)
##                            noticemsg = EncodeMessagePacket(9,noticemsgde)
##                            print "发送: %s"  %noticemsg
##                            sockt.sendall(noticemsg)
##                        except socket.error:
##                            print "send failed"
##                        data = sockt.recv(1024)
##                        print "收到mm: %s" %data
##                        datalist = DecodeMessagePacket(data)
##                        print datalist
##                        mapx = datalist[0][2]
##                        mapy = datalist[0][3]
##
##                        try:
##                            bagitemmsgde = DefaultMessage(0,81,0,0,0)
##                            bagitemmsg = EncodeMessagePacket(1,bagitemmsgde)
##                            print "发送: %s"  %bagitemmsg
##                            sockt.sendall(bagitemmsg)
##                        except socket.error:
##                            print "send failed"
##                        data = sockt.recv(1024)
##                        print "收到: %s" %data
##                        datam = []
##                        datam = data.split('#')
##                        for data in datam:
##                            print '#'+ data
##                            data = '#' + data
##                            #datalist = DecodeMessagePacket(data)
##                            #print datalist
##                        try:
##                            reginfomsgde = DefaultMessage(232344,5106,0,0,0)
##                            reginfomsg = EncodeMessagePacket(2, reginfomsgde)
##                            print "发送: %s"  %reginfomsg
##                            sockt.sendall(reginfomsg)
##                        except socket.error:
##                            print "发送失败"
##                        data = sockt.recv(1024)
##                        code = 3
##                        while True:
##                            try:
##                                if code >=10:
##                                    code = 3
##                                mass = random.randint(0,7)
##                                print MakeLong(mapx,mapy),mapx,mapy,3011,mass
##                                walkmsgde = DefaultMessage(MakeLong(mapx,mapy),3011,mass,0)
##                                mapx,mapy = GetNextPosXY(mass,mapx,mapy)
##                                walkmsg = EncodeMessagePacket(code,walkmsgde)
##                                code = code + 1
##                                time.sleep(0.5)
##                                print walkmsg
##                                sockt.sendall(walkmsg)     
##                            except socket.error:
##                                print "send failed!!!"
##                            data = sockt.recv(1024)
##                            print "收到： %s" %data
##                            #time.sleep(1)
##                    except socket.error:
##                        print "连接失败"
##            except socket.error:
##                print "连接失败"
##            
##        elif datalist[0][1] == 503:
##            print "密码验证未通过"
    
      print DecodeMessage('LAkB>_H<FLAk<\@<')
     # print DecodeMessage('#LAkB>_H<D<A\<\@<')
      print DecodeMessage('xlAT<hPG<<<B<<<<')
      print DecodeString('XrMoUCI`TSI`TSI`TRM]XrM]XrM]XrM]XrM]XrL')
##    print DecodeMessage('<<\C<KDO<<<<<<<<')
##    print DecodeMessage('4ElAn<hHG<<<><<<<')
##    print DecodeMessage('E\An<hHG<<<@<<<<')
##
