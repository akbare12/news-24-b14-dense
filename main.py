import os
from PIL import Image, ImageDraw, ImageFont
W,H=1024,1024; OUT=os.path.join(os.environ.get('MAKEFUN_OUTPUT_DIR','out'),'entry.png')
CREAM=(250,246,235); INK=(20,20,22); RED=(178,34,34); NAVY=(24,42,78); TEAL=(18,110,105); GOLD=(176,132,28); GREY=(110,110,112); LGRN=(222,228,205); OCEAN=(198,222,235); LAND=(168,178,132)
def F(s,b=False,serif=False):
    p='/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf' if serif and b else '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf' if serif else '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf' if b else '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    try: return ImageFont.truetype(p,s)
    except Exception: return ImageFont.load_default()
def wrap(t,f,w,d):
    words=t.split(); lines=[]; cur=''
    for wd in words:
        s=(cur+' '+wd).strip()
        if d.textlength(s,font=f)<=w: cur=s
        else:
            if cur: lines.append(cur)
            cur=wd
    if cur: lines.append(cur)
    return lines
def txt(d,x,y,t,f,fill=INK,anchor='la'):
    d.text((x,y),t,font=f,fill=fill,anchor=anchor)
def para(d,x,y,t,f,w,fill=INK,lh=None):
    lh=lh or int(f.size*1.28)
    for i,ln in enumerate(wrap(t,f,w,d)): d.text((x,y+i*lh),ln,font=f,fill=fill)
    return y+len(wrap(t,f,w,d))*lh
CHIP={'CONFIRMED':(34,120,60),'OFFICIAL':(24,90,160),'REPORTED':(90,90,100),'CLAIM':(200,110,20),'ONGOING':(176,132,28)}
def chip(d,x,y,label):
    f=F(7,True); w=int(d.textlength(label,font=f))+10
    d.rounded_rectangle([x,y,x+w,y+11],2,fill=CHIP.get(label,(90,90,100))); d.text((x+5,y+1),label,font=f,fill=(255,255,255)); return x+w+4
CONT=[([(-168,66),(-140,70),(-125,71),(-110,68),(-95,69),(-85,66),(-80,73),(-70,62),(-65,60),(-55,47),(-60,46),(-70,42),(-75,35),(-80,32),(-81,26),(-84,30),(-90,21),(-97,26),(-105,23),(-110,24),(-114,29),(-120,34),(-125,40),(-124,48),(-130,55),(-140,60),(-155,58),(-165,60),(-168,66)]),([(-80,9),(-77,4),(-80,-3),(-81,-6),(-77,-12),(-72,-18),(-70,-23),(-70,-30),(-72,-37),(-73,-44),(-70,-52),(-68,-55),(-65,-50),(-62,-41),(-57,-38),(-52,-33),(-48,-28),(-41,-23),(-35,-9),(-35,-6),(-44,-3),(-50,0),(-55,5),(-60,8),(-68,11),(-75,10),(-80,9)]),([(-6,35),(10,37),(20,32),(30,31),(32,31),(35,28),(37,22),(40,15),(43,11),(48,11),(51,12),(44,2),(40,-5),(40,-12),(36,-18),(33,-26),(28,-33),(20,-35),(16,-29),(13,-18),(12,-6),(9,4),(4,6),(-8,5),(-13,8),(-17,15),(-17,21),(-16,28),(-10,31),(-6,35)]),([(-10,36),(-9,43),(-2,48),(-5,50),(0,51),(3,53),(8,57),(10,59),(5,60),(5,62),(12,65),(18,69),(25,71),(32,70),(40,68),(50,69),(60,69),(70,72),(80,73),(90,75),(100,76),(110,74),(120,73),(130,72),(140,72),(150,70),(160,69),(170,67),(178,65),(178,62),(170,60),(162,56),(158,52),(150,59),(142,54),(140,46),(135,43),(130,42),(127,40),(122,38),(120,32),(122,28),(118,25),(110,20),(108,12),(105,9),(100,7),(98,12),(95,16),(92,21),(89,22),(86,20),(80,15),(77,8),(75,12),(72,20),(68,23),(62,25),(57,26),(54,26),(52,25),(50,29),(48,30),(44,29),(40,28),(39,24),(35,29),(34,31),(30,36),(27,36),(23,36),(19,40),(15,44),(12,44),(8,44),(3,43),(0,40),(-2,37),(-6,36),(-10,36)]),([(113,-22),(114,-30),(115,-35),(120,-34),(124,-33),(129,-32),(132,-32),(135,-35),(137,-38),(140,-38),(145,-38),(150,-37),(153,-32),(153,-27),(150,-23),(146,-19),(142,-15),(142,-11),(141,-13),(136,-12),(135,-15),(132,-12),(130,-13),(126,-14),(122,-17),(118,-20),(113,-22)]),([(130,31),(132,33),(135,34),(137,35),(139,37),(140,39),(141,41),(143,42),(145,44),(143,42),(140,38),(136,34),(132,32),(130,31)]),([(95,5),(100,0),(105,-5),(110,-7),(114,-8),(118,-9),(120,-10),(125,-9),(130,-4),(135,-3),(140,-8),(138,-8),(132,-6),(126,-3),(120,0),(115,2),(110,4),(105,5)])]
def project(lon,lat,mx,my,mw,mh): return mx+(lon+180)/360*mw, my+(75-lat)/130*mh
def draw_map(d,mx,my,mw,mh):
    d.rectangle([mx,my,mx+mw,my+mh],fill=OCEAN,outline=NAVY,width=1)
    for poly in CONT:
        pts=[project(lo,la,mx,my,mw,mh) for lo,la in poly]; d.polygon(pts,fill=LAND,outline=(90,100,60))
    return
PINS=[(1,24.7,46.7,RED,0,0),(2,31.2,121.5,(200,110,20),0,0),(3,40.7,-74.0,NAVY,0,0),(4,47.8,35.2,(110,60,140),0,0),(5,14.7,-17.4,(34,120,60),0,0),(6,26.6,56.4,RED,0,0),(7,40.7,-74.0,NAVY,-13,9),(8,47.67,-122.12,NAVY,0,0),(9,39.8,30.5,(110,60,140),0,0),(10,10.4,-75.5,TEAL,-8,8),(11,12.8,45.0,RED,0,0),(12,13.0,44.9,RED,11,-9),(13,39.7,98.5,(200,110,20),0,0)]
def _scene(d,x,y,w,h,kind):
    d.rectangle([x,y,x+w,y+h],fill=(30,34,52) if kind in ('riyadh','drones') else (58,84,110) if kind in ('ship','strike') else (210,205,190) if kind=='court' else (235,228,205) if kind in ('shanghai','trophy') else (120,30,28) if kind=='datacenter' else (196,214,228) if kind=='chart' else (228,214,180))
    if kind=='riyadh':
        for bx,bw,bh in [(8,16,52),(30,20,66),(56,14,44),(76,18,58)]:
            d.rectangle([x+bx,y+h-bh,x+bx+bw,y+h],fill=(52,58,84),outline=(200,190,120))
            for wy in range(y+h-bh+6,y+h-4,9):
                for wx in range(x+bx+3,x+bx+bw-3,6): d.rectangle([wx,wy,wx+2,wy+3],fill=(240,210,110))
        d.polygon([(x+w*0.55,y+8),(x+w*0.55+16,y+34),(x+w*0.55+34,y+34),(x+w*0.55+18,y+8)],fill=(70,76,104))
        d.polygon([(x+w*0.55+8,y+2),(x+w*0.55+12,y+10),(x+w*0.55+16,y+2)],fill=(240,210,110))
        d.ellipse([x+w*0.72,y+18,x+w*0.72+26,y+44],fill=(240,120,40)); d.ellipse([x+w*0.72+6,y+24,x+w*0.72+32,y+50],fill=(250,180,60))
        d.ellipse([x+w*0.12,y+10,x+w*0.12+16,y+20],fill=(180,180,190)); d.line([x+w*0.12+8,y+20,x+w*0.12+8,y+30],fill=(180,180,190),width=2)
    elif kind=='shanghai':
        d.rectangle([x,y+h-46,x+w,y+h],fill=(120,30,28)); d.rectangle([x+w*0.3,y+14,x+w*0.7,y+h-46],fill=(150,40,36))
        d.polygon([(x+w*0.22,y+16),(x+w*0.5,y-2),(x+w*0.78,y+16)],fill=(90,20,20))
        d.rectangle([x+w*0.44,y+34,x+w*0.56,y+h-46],fill=(60,14,14))
        d.rectangle([x+w*0.1,y+h-38,x+w*0.34,y+h-8],fill=(245,240,225)); d.rectangle([x+w*0.66,y+h-38,x+w*0.9,y+h-8],fill=(245,240,225))
        for lx in (x+w*0.13,x+w*0.69):
            for ly in range(y+h-34,y+h-10,7): d.line([lx,ly,lx+w*0.18,ly],fill=(60,60,60),width=1)
        d.ellipse([x+w*0.82,y+6,x+w*0.82+14,y+20],fill=(240,210,110))
    elif kind=='court':
        d.rectangle([x,y+h-30,x+w,y+h],fill=(120,110,90))
        for cx in (x+8,x+w*0.42,x+w*0.78):
            d.rectangle([cx,y+18,cx+12,y+h-30],fill=(245,240,225),outline=(120,110,90))
            d.rectangle([cx-4,y+12,cx+16,y+18],fill=(200,190,170))
        d.polygon([(x+w*0.36,y+30),(x+w*0.5,y+8),(x+w*0.64,y+30)],fill=(176,132,28))
        d.rectangle([x+w*0.3,y+h-58,x+w*0.7,y+h-30],fill=(90,60,40)); d.ellipse([x+w*0.44,y+h-70,x+w*0.56,y+h-58],fill=(120,80,50))
    elif kind=='drones':
        d.rectangle([x,y+h-18,x+w,y+h],fill=(40,44,60))
        for bx,bw,bh in [(6,14,30),(26,18,44),(50,12,26),(70,16,36)]:
            d.rectangle([x+bx,y+h-18-bh,x+bx+bw,y+h-18],fill=(20,22,34))
            for wy in range(y+h-18-bh+5,y+h-20,8):
                for wx in range(x+bx+3,x+bx+bw-3,5): d.rectangle([wx,wy,wx+2,wy+2],fill=(240,200,90))
        d.ellipse([x+w*0.7,y+12,x+w*0.7+18,y+26],fill=(240,120,40)); d.ellipse([x+w*0.7+5,y+17,x+w*0.7+24,y+32],fill=(250,180,60))
        for dx,dy in [(0.2,0.25),(0.45,0.15),(0.62,0.3)]:
            cx,cy=x+w*dx,y+h*dy; d.ellipse([cx-7,cy-3,cx+7,cy+3],fill=(200,200,205)); d.line([cx-11,cy,cx+11,cy],fill=(160,160,165),width=2)
    elif kind=='trophy':
        d.ellipse([x+w*0.5-26,y+8,x+w*0.5+26,y+60],fill=(240,200,80),outline=(176,132,28),width=2)
        d.ellipse([x+w*0.5-14,y+18,x+w*0.5+14,y+50],fill=(250,220,120))
        d.rectangle([x+w*0.5-4,y+58,x+w*0.5+4,y+70],fill=(176,132,28)); d.rectangle([x+w*0.5-14,y+70,x+w*0.5+14,y+76],fill=(176,132,28))
        d.rectangle([x+6,y+h-16,x+w*0.32,y+h-6],fill=(34,120,60)); d.rectangle([x+w*0.68,y+h-16,x+w-6,y+h-6],fill=(178,34,34))
    elif kind=='ship':
        d.rectangle([x,y+h-26,x+w,y+h],fill=(40,90,120))
        d.rectangle([x+8,y+h-52,x+w-8,y+h-26],fill=(90,60,40)); d.rectangle([x+14,y+h-72,x+w*0.5,y+h-52],fill=(240,240,235))
        for cx in range(x+16,x+w-12,14): d.rectangle([cx,y+h-48,cx+8,y+h-40],fill=(40,90,120))
        d.rectangle([x+w*0.62,y+h-66,x+w*0.72,y+h-52],fill=(200,200,195))
        d.ellipse([x+w*0.8,y+10,x+w*0.8+16,y+26],fill=(240,120,40))
    elif kind=='chart':
        d.line([x+8,y+h-12,x+w-8,y+h-12],fill=(60,60,60),width=2)
        pts=[(x+10,y+h-30),(x+w*0.3,y+h-44),(x+w*0.5,y+h-38),(x+w*0.7,y+h-62),(x+w-10,y+h-70)]
        for a,b in zip(pts,pts[1:]): d.line([a,b],fill=(24,90,160),width=3)
        d.line([x+w*0.7,y+8,x+w*0.7,y+h-12],fill=(178,34,34),width=1)
        d.text((x+10,y+6),'50,000',font=F(11,True),fill=RED)
        d.rectangle([x+8,y+h-12,x+w-8,y+h-8],fill=(34,120,60))
    elif kind=='datacenter':
        for i in range(4):
            d.rectangle([x+8+i*24,y+10,x+8+i*24+18,y+h-10],fill=(40,40,48),outline=(200,60,50))
            for ry in range(y+16,y+h-14,8):
                d.rectangle([x+11+i*24,ry,x+14+i*24,ry+3],fill=(240,80,60) if i%2 else (80,200,120))
        d.text((x+w-34,y+2),'!',font=F(14,True),fill=(255,255,255))
    elif kind=='heli':
        d.ellipse([x+w*0.2,y+h*0.4,x+w*0.6,y+h*0.62],fill=(90,100,90))
        d.rectangle([x+w*0.6,y+h*0.46,x+w*0.92,y+h*0.54],fill=(90,100,90))
        d.line([x+w*0.1,y+h*0.42,x+w*0.7,y+h*0.42],fill=(60,60,60),width=3)
        d.polygon([(x+w*0.3,y+h*0.4),(x+w*0.36,y+h*0.2),(x+w*0.42,y+h*0.4)],fill=(70,80,70))
        d.polygon([(x+6,y+h-8),(x+w*0.4,y+h-34),(x+w*0.7,y+h-8)],fill=(120,110,90))
    elif kind=='market':
        d.rectangle([x,y+h-30,x+w,y+h],fill=(150,140,120))
        d.rectangle([x+8,y+14,x+w*0.45,y+h-30],fill=(240,235,220)); d.rectangle([x+w*0.55,y+22,x+w-8,y+h-30],fill=(220,210,190))
        for i in range(3):
            d.rectangle([x+14+i*14,y+22+i*6,x+14+i*14+9,y+h-34],fill=(34,120,60))
    elif kind=='desert':
        d.polygon([(x,y+h),(x+w*0.3,y+h-34),(x+w*0.6,y+h),(x+w,y+h)],fill=(210,190,140))
        d.polygon([(x+w*0.4,y+h),(x+w*0.7,y+h-26),(x+w,y+h)],fill=(190,170,120))
        d.rectangle([x+w*0.15,y+h-52,x+w*0.25,y+h-30],fill=(90,70,50)); d.rectangle([x+w*0.18,y+h-58,x+w*0.22,y+h-52],fill=(60,45,30))
    elif kind=='strike':
        d.rectangle([x,y+h-20,x+w,y+h],fill=(60,60,66))
        d.rectangle([x+w*0.2,y+16,x+w*0.8,y+h-20],fill=(200,200,195))
        d.rectangle([x+w*0.3,y+24,x+w*0.42,y+h-28],fill=(40,90,120)); d.rectangle([x+w*0.58,y+24,x+w*0.7,y+h-28],fill=(40,90,120))
        d.ellipse([x+w*0.44,y+10,x+w*0.44+14,y+24],fill=(240,120,40))
    else:
        d.polygon([(x+w*0.5,y+6),(x+w*0.62,y+h*0.5),(x+w*0.5,y+h-8),(x+w*0.38,y+h*0.5)],fill=(240,240,235),outline=(176,132,28))
        d.ellipse([x+w*0.44,y+h*0.42,x+w*0.56,y+h*0.58],fill=(240,120,40))
        d.rectangle([x+8,y+h-14,x+w-8,y+h-8],fill=(176,132,28))
def scene(d,x,y,w,h,kind):
    if h>=90: _scene(d,x,y,w,h,kind); return
    tmp=Image.new('RGB',(int(w),96)); td=ImageDraw.Draw(tmp); _scene(td,0,0,int(w),96,kind); im.paste(tmp.resize((int(w),int(h))),(int(x),int(y)))
HERO=[('1','RIYADH','MIDDLE EAST','CONFIRMED','Houthi drone hits Riyadh\'s tallest tower again, 11 hurt','A Houthi drone struck the PIF tower, Riyadh\'s tallest, the second hit in a week. 11 hurt: 2 Saudis, 2 Indians, 3 Nepalis, 4 Egyptians.','Saudi officials · AP','riyadh'),('2','SHANGHAI','ASIA','OFFICIAL','China probes Shanghai party chief Chen Jining','Chen Jining, 62, is probed for "serious violations". He is the fourth Politburo member to fall in a probe this year.','CCDI','shanghai'),('3','NEW YORK','US/TECH','CONFIRMED','Huawei guilty on 10 of 12 counts','A US federal jury found Huawei guilty of trade-secret theft and bank fraud on 10 of 12 counts. It was cleared of racketeering.','US court','court')]
CARDS=[('4','ZAPORIZHZHIA','EUROPE/WAR','REPORTED','Russian attacks kill 9 across Ukraine in a day','Nine were killed and 81 hurt as Russia launched 96 drones; Kyiv says 73 were shot down or jammed.','Ukraine officials','drones'),('5','CAS · SENEGAL','AFRICA/SPORT','OFFICIAL','CAS hands Senegal back the AFCON title','Morocco forfeited 3-0, so Senegal won the final 1-0 and took the Africa Cup back.','CAS','trophy'),('6','HORMUZ','MIDDLE EAST','REPORTED','IRGC attacks container ship in Hormuz','A container ship was attacked at 18:58 UTC and its navigation was disabled near Khasab, Oman.','UKMTO','ship'),('7','NEW YORK','WORLD/MARKETS','CONFIRMED','Dow closes above 50,000 for the first time','The Dow closed at 50,018, its first finish above 50,000, while the Nasdaq fell 1.5% and Taiex set a record.','Market close','chart'),('8','REDMOND','WORLD/TECH','REPORTED',"Microsoft declares 'Code Red' after historic outage",'After a 24-hour outage, Microsoft set a one-hour global recovery target with five workstreams and AI diagnosis.','Reuters','datacenter'),('9','ESKISEHIR','EUROPE','REPORTED','Turkish military helicopter crash kills 5','An AS-532 military helicopter crashed in Eskisehir at 19:52 UTC, killing all five aboard.','Turkish officials','heli'),('10','CARTAGENA','AMERICAS','REPORTED','Supermarket hostages: 25 held in Cartagena','Gunmen held 25 people in a Cartagena supermarket; five elderly women were freed and flights were held 45 minutes.','Colombia officials','market'),('11','ADEN','MIDDLE EAST','REPORTED','Houthis advance within 60 km of Aden','Houthi forces advanced to within 60 km of Aden in Yemen at 16:51 UTC.','Wires','desert'),('12','LAHJ','MIDDLE EAST','REPORTED','Saudi strikes kill 25, wound 6 in Yemen','Saudi strikes on a bus and truck in Wadi Maabaq, Lahj, killed or left missing 25 people and wounded six.','Yemen officials','strike'),('13','JIUQUAN','WORLD/SPACE','OFFICIAL','China names first foreign astronaut for Tiangong',"Shenzhou-24's crew was named: Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali of Pakistan, the first foreigner on Tiangong.",'CMSA','rocket')]
ALSO=[('14','Ankara','Haftar visits Turkey for the first time'),('15','London','UK sanctions Houthis and 4 officials'),('16','Villavicencio','Car bomb injures 23'),('17','Gaza','Israel kills Hamas internal security chief'),('18','Baghdad','Iraq orders federal control of Kurdish oilfields'),('19','Gaza','Meningitis alert as cases hit 272 in October'),('20','DR Congo','Cessna 208 missing; rebels claim shootdown'),('21','Hanoi','Hot-pot blast kills at least 6'),('22','Gulf of Finland','Ukraine hits Russian ship Sparta II'),('23','Kuala Lumpur','Malaysia to return thousands of migrants'),('24','Ulleungdo','S. Korea shelter order as jets enter ADIZ'),('25','Dhaka','Hasina plans return on 16 December'),('26','The Hague','14 nations endorse ICJ Myanmar ruling'),('27','Jakarta','Indonesia nominates two VP candidates'),('28','Beijing','China sentences official Ma to death for spying'),('29','Brussels','NATO vows defence against space threat'),('30','Mexico City','US drone aided El Chapo capture'),('31','San Salvador','Bukele names 3 soldiers killed in Haiti'),('32','Ottawa','Pentagon rebukes Canada over jets'),('33','Washington','US adds Megaspeed to trade blacklist'),('34','Kyiv','Zelensky urges Ukraine-Russia-US-Europe talks'),('35','Ras Al Khaimah','Bus-truck crash kills 13'),('36','London','Record 5,258 heat deaths in summer'),('37','Kourou','Ariane 6 lofts 36 Amazon satellites'),('38','Cikande','Factory-fire toll rises to 26')]
UTC=[('02:15','NATO vows space defence'),('08:16','Hanoi blast kills 6'),('10:42','Saudi strikes Yemen'),('14:27','Riyadh tower hit'),('16:51','Houthis 60 km from Aden'),('18:58','Hormuz ship attack'),('20:41','Huawei guilty')]
NUMS=[('11','hurt in Riyadh'),('9','killed in Ukraine'),('50,018','Dow close'),('+8.99%','Taiex record'),('25','killed or missing in Yemen'),('26','toll in Cikande fire')]
REGS=[('Europe',7,(110,60,140)),('Middle East',8,RED),('Asia',9,(200,110,20)),('Africa',5,(34,120,60)),('Americas',5,TEAL),('Oceania',0,GREY),('World/Space',4,NAVY)]
im=Image.new('RGB',(W,H),CREAM); d=ImageDraw.Draw(im); M=14; CW=W-2*M
d.rectangle([0,0,W,6],fill=RED)
txt(d,M,10,'THE WORLD ON ONE DAY',F(11,True),RED); txt(d,W-M,10,'38 STORIES  ·  7 REGIONS  ·  14 FIELDS  ·  ALL FROM TUESDAY 24 NOVEMBER 2026',F(10,True),NAVY,anchor='ra')
txt(d,M,26,'Tuesday 24 November 2026',F(30,True,True)); d.line([M,64,W-M,64],fill=INK,width=2)
txt(d,M,68,'Riyadh tower hit again  ·  Shanghai party chief probed  ·  Huawei guilty on 10 of 12 counts',F(12,False,True),RED)
y=88; x=M
for name,n,col in REGS:
    w=40+int(d.textlength(name,font=F(10,True)))+int(d.textlength(str(n),font=F(12,True)))+16
    d.rectangle([x,y,x+w,y+20],fill=col); d.text((x+6,y+4),name,font=F(10,True),fill=(255,255,255)); d.text((x+w-16,y+3),str(n),font=F(12,True),fill=(255,255,255)); x+=w+4
y=112; d.rectangle([M,y,W-M,y+38],fill=(255,255,255),outline=NAVY,width=1); txt(d,M+6,y+3,'THE DAY IN UTC',F(9,True),NAVY)
cw=int((CW-12)/7)
for i,(t,ev) in enumerate(UTC):
    xx=M+6+i*cw; txt(d,xx,y+15,t,F(10,True),RED); para(d,xx,y+26,ev,F(8),cw-4,INK,10)
y=152; d.rectangle([M,y,W-M,y+40],fill=NAVY)
txt(d,M+6,y+3,'THE DAY IN NUMBERS',F(9,True),(255,255,255))
nw=int((CW-12)/6)
for i,(v,lab) in enumerate(NUMS):
    xx=M+6+i*nw; txt(d,xx,y+14,v,F(15,True),(255,255,255)); para(d,xx,y+31,lab,F(8),nw-4,(255,255,255),9)
hy=196; hw=int((CW-16)/3); hh=210
for i,(num,loc,field,ch,hl,deck,src,kind) in enumerate(HERO):
    x=M+i*(hw+8); d.rectangle([x,hy,x+hw,hy+hh],fill=(255,255,255),outline=INK,width=1)
    scene(d,x+1,hy+1,hw-2,96,kind)
    yy=hy+102; txt(d,x+6,yy,f'{num}  {loc}',F(11,True),RED); txt(d,x+6,yy+13,field,F(8,True),NAVY)
    cx=chip(d,x+hw-46,yy+13,ch)
    para(d,x+6,yy+28,hl,F(13,True),hw-12,INK,16)
    para(d,x+6,yy+62,deck,F(9),hw-12,(40,40,40),11)
    txt(d,x+6,hy+hh-14,'('+src+')',F(8,False,True),GREY)
cy=412; cw2=int((CW-24)/5); chh=120
for i,(num,loc,field,ch,hl,deck,src,kind) in enumerate(CARDS):
    r,c=divmod(i,5); x=M+c*(cw2+6); yy=cy+r*(chh+6)
    d.rectangle([x,yy,x+cw2,yy+chh],fill=(255,255,255),outline=INK,width=1)
    scene(d,x+1,yy+1,cw2-2,32,kind)
    txt(d,x+5,yy+36,f'{num}  {loc}',F(9,True),RED)
    chip(d,x+cw2-52,yy+35,ch)
    para(d,x+5,yy+48,hl,F(10,True),cw2-10,INK,12)
    para(d,x+5,yy+74,deck,F(8),cw2-10,(40,40,40),10)
    txt(d,x+5,yy+chh-11,'('+src+')',F(7,False,True),GREY)
my=676; mx=M; mw=486; mh=148
txt(d,M,662,'THE WORLD  ·  WHERE IT HAPPENED',F(11,True),NAVY)
draw_map(d,mx,my,mw,mh)
for num,lat,lon,col,dx,dy in PINS:
    px,py=project(lon,lat,mx,my,mw,mh); px+=dx; py+=dy
    d.ellipse([px-8,py-8,px+8,py+8],fill=col,outline=(255,255,255),width=1); d.text((px,py-5),str(num),font=F(8,True),fill=(255,255,255),anchor='mm')
ly=my+mh+6; lx=M
for name,n,col in REGS:
    d.ellipse([lx,ly,lx+7,ly+7],fill=col); d.text((lx+9,ly-1),f'{name} {n}',font=F(8,True),fill=INK); lx+=int(d.textlength(f'{name} {n}',font=F(8,True)))+22
ax=514; txt(d,ax,662,'ALSO ON TUESDAY 24 NOVEMBER  —  25 MORE STORIES',F(11,True),NAVY)
colw=int((W-M-ax-8)/2)
for i,(num,city,hl) in enumerate(ALSO):
    c,r=divmod(i,13); xx=ax+c*(colw+8); yy=678+r*13
    t=f'{num}. {city}: {hl}'
    while d.textlength(t,font=F(8))>colw and len(t)>10: t=t[:-1]
    d.text((xx,yy),t,font=F(8),fill=INK)
dy=872; d.rectangle([M,dy,W-M,dy+104],fill=(255,235,235),outline=RED,width=2)
txt(d,M+8,dy+5,'DATE CHECK',F(11,True),RED)
para(d,M+8,dy+20,'Every story above happened or was first reported on Tuesday 24 November 2026. Wires read up to 23:00 UTC.',F(9),W-2*M-16,(40,40,40),12)
para(d,M+8,dy+44,'LEFT OUT (not 24 Nov): Hormuz mine claims on 4 tankers (Mon 23 Nov); Huang back as Nvidia CEO (Mon 23 Nov); EU sanctions package 22 (Mon 23 Nov); COP31 ends with no deal (Sun 22 Nov); corvette Merkury sunk (Sat 22 Nov); El Chapo Isidro arrested (Fri 20 Nov); Cikande factory fire started (Sat 21 Nov); Trump hush-money appeal ruling (Mon 23 Nov); ATP Finals (Sun 22 Nov); Las Vegas GP (Sat 21 Nov); Peru quake M6.7 (Fri 20 Nov).',F(9),W-2*M-16,(40,40,40),12)
para(d,M+8,dy+80,'NOT YET: Shenzhou-24 launch (Wed 25 Nov 00:18 UTC); MPR session picks VP (11 Dec); Huawei sentencing (Sep 2027); Hasina returns (16 Dec).',F(9),W-2*M-16,(40,40,40),12)
fy=984; d.line([M,fy,W-M,fy],fill=INK,width=1)
para(d,M,fy+5,'Sources: dailysummaryof.com/world/2026-11-24  ·  AP  ·  Reuters  ·  UKMTO  ·  CAS  ·  CMSA  ·  CCDI  ·  UKHSA  ·  wires.   CONFIRMED = 2+ outlets  ·  OFFICIAL = on record  ·  REPORTED = one outlet  ·  CLAIM = one side\'s claim.   Scenes are drawn illustrations, not photographs.',F(8),CW,GREY,11)
os.makedirs(os.path.dirname(OUT) or '.',exist_ok=True); im.save(OUT)
print('saved',OUT,im.size)
