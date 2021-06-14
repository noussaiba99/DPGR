import os
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, Http404
from .models import PV,Acteur
import logging
from reportlab.lib.colors import blue , grey, black
from django.core import mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from django.core.mail import EmailMessage
from DPGR.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.db.models.functions import Cast
from django.db.models import CharField
from django.core.mail import send_mail
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
        datee=date.strftime('%d-%m-%Y')
        heure=date.strftime('%H:%M')
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
        p.drawString(220,780,"Rédigé le: "+datee+" à "+heure)
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
       
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="PV:{titre}"["{datee}].pdf"'
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
        datee=date.strftime('%d-%m-%Y')
        heure=date.strftime('%H:%M')
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
        p.drawString(220,780,"Rédigé le "+datee+" à "+heure)
        p.setFont("Helvetica-Bold",14)
        p.setFillColor(black)
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
        responsee = HttpResponse(content_type='application/pdf')
        responsee['Content-Disposition'] = f'attachment; filename="{titre}[{datee}].pdf"'
        pdf = buffer.getvalue()
        buffer.close()
        mailList=[a.email for a in pres]
        
        fromaddr = "communication.dpgr.esi.2021@gmail.com"
        subject = "[PV] ["+titre+" ]["+datee+"]"
        body = "Vous trouverez ci-joint le pv intitulé : "+titre+" rédigé le:"+datee+". \n\n Cordialement,\n DPGR"
        EmailMsg=EmailMessage(subject,body,fromaddr,mailList)
        EmailMsg.attach('PV_'+titre+'.pdf',pdf,'application/pdf')
        EmailMsg.send()
        #messages.info(requestt, 'Le pv a été généré avec succès!')
        messages.success(requestt, 'Le pv a été partagé avec succès!')
        return redirect('../../../PV/pv')

    return HttpResponse(status=400)