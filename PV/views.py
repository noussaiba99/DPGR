from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import PV,Acteur
import logging
from reportlab.lib.colors import blue , grey, black
from django.core import mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
logger = logging.getLogger(__name__)


def generer_pv(request, pv_id):
    if request.method == 'POST':
        from django.shortcuts import render
        from .models import PV
        import io
        from io import BytesIO
        from django.http import FileResponse
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.colors import blue , grey, black

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        pv = PV.objects.get(pk=pv_id)
        titre = pv.titre
        date= pv.date
        odj=pv.ordreDuJour
        pa=pv.pointAborde
        contenu= pv.contenu
        Desicions= pv.Decisions
        pres=pv.presents.all()
        p.setFillColor(blue)
        p.setFont("Helvetica-Bold",14)
        p.drawString(250,800,titre)
        p.setFillColor(grey)
        p.setFont("Helvetica",12)
        p.drawString(220,780,"Rédigé le "+str(date))
        p.setFillColor(black)
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,750,"Les présents:")

        #la variable i c'est pour gérer l'espace interlignes
        i=720
        p.setFont("Helvetica",12)
        for acteur in pres:
            p.drawString(60,i,str(acteur))
            i=i-20

        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"L'ordre du jour:")
        p.setFont("Helvetica",12)

        #l'instruction qui suit pour le saut de ligne
        # (on divise la chaine de caraactère à chaque fois qu'on rencontre un \n pcq reportlab ne reconnait pas le caractère de saut de ligne \n)
        listchaine=str(odj).split('\n')

        
        long=len(listchaine)
        
    
        i=i-40
        j=1
        #la boucle for pour afficher les lignes du paragraphe divisée en ligne dans les instructions en-dessus
        for l in listchaine:
            print(l)
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            j=j+1
            i=i-15
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Points abordées:")
        p.setFont("Helvetica",12)
        listchaine=str(pa).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            j=j+1
            i=i-15

        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Contenu du PV:")
        p.setFont("Helvetica",12)
    
        listchaine=str(contenu).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
        
            if(j<long):
            #la fonction rstrip pour omettre le dernier caractère de chaque ligne dans ce cas c'est \n 
            # sinn il va s'afficher comme un carré noir sur le pdf tu peux l'essayer 
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            i=i-15
            j=j+1
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Décisions finales:")
        p.setFont("Helvetica",12)
        listchaine=str(Desicions).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            i=i-15
            j=j+1
        p.showPage()
        p.save()
            # fName='PV'+ str(pv_id) +'.pdf'
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{titre}.pdf"'
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response    
    return HttpResponse(status=400)

def partager_pv(requestt,pv_i):
    if requestt.method == 'POST':
        from django.shortcuts import render
        from .models import PV
        import io
        from io import BytesIO
        from django.http import FileResponse
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.colors import blue , grey, black

        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        pv = PV.objects.get(pk=pv_i)
        titre = pv.titre
        date= pv.date
        odj=pv.ordreDuJour
        pa=pv.pointAborde
        contenu= pv.contenu
        Desicions= pv.Decisions
        pres=pv.presents.all()
        p.setFillColor(blue)
        p.setFont("Helvetica-Bold",14)
        p.drawString(250,800,titre)
        p.setFillColor(grey)
        p.setFont("Helvetica",12)
        p.drawString(220,780,"Rédigé le "+str(date))
        p.setFillColor(black)
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,750,"Les présents:")

        #la variable i c'est pour gérer l'espace interlignes
        i=720
        p.setFont("Helvetica",12)
        for acteur in pres:
            p.drawString(60,i,str(acteur))
            i=i-20

        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"L'ordre du jour:")
        p.setFont("Helvetica",12)

        #l'instruction qui suit pour le saut de ligne
        # (on divise la chaine de caraactère à chaque fois qu'on rencontre un \n pcq reportlab ne reconnait pas le caractère de saut de ligne \n)
        listchaine=str(odj).split('\n')

        
        long=len(listchaine)
        
    
        i=i-40
        j=1
        #la boucle for pour afficher les lignes du paragraphe divisée en ligne dans les instructions en-dessus
        for l in listchaine:
            print(l)
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            j=j+1
            i=i-15
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Points abordées:")
        p.setFont("Helvetica",12)
        listchaine=str(pa).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            j=j+1
            i=i-15

        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Contenu du PV:")
        p.setFont("Helvetica",12)
    
        listchaine=str(contenu).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
        
            if(j<long):
            #la fonction rstrip pour omettre le dernier caractère de chaque ligne dans ce cas c'est \n 
            # sinn il va s'afficher comme un carré noir sur le pdf tu peux l'essayer 
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            i=i-15
            j=j+1
        p.setFont("Helvetica-Bold",14)
        p.drawString(50,i-20,"Décisions finales:")
        p.setFont("Helvetica",12)
        listchaine=str(Desicions).split("\n")
        long=len(listchaine)
        i=i-40
        j=1
        for l in listchaine:
            if(j<long):
                l= str(l).rstrip(l[-1])
            p.drawString(50,i,l)
            i=i-15
            j=j+1
        p.showPage()
        p.save()
            # fName='PV'+ str(pv_id) +'.pdf'
        responsee = HttpResponse(content_type='application/pdf')
        responsee['Content-Disposition'] = f'attachment; filename="{titre}.pdf"'
        pdf = buffer.getvalue()
        buffer.close()
        responsee.write(pdf)
        
        fromaddr = "communication.dpgr.esi.2021@gmail.com"
        toaddr = "hn_aboutaleb@esi.dz"
        msg = MIMEMultipart()
        msg['From'] = fromaddr
        msg['To'] = toaddr
        msg['Subject'] = "[PV de la réunion]"+" ["+titre+" ]"+" [le   ]"
        body = "Write your message here"
        msg.attach(MIMEText(body, 'plain'))
        #msg.attach('file.pdf', p, 'image/png')
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(fromaddr, "DpgrEsi2021")
        text = msg.as_string()
        server.sendmail(fromaddr, toaddr, text)
        server.quit()
        return responsee    
    return HttpResponse(status=400)