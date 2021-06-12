from django.shortcuts import render
from django.http import HttpResponse
from .models import PV
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def generer_pv(request,pv_id):
    
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pv = PV.objects.get(pk=pv_id)
    output = pv.titre
    #return HttpResponse(output)
    #output="haha"
    p.drawString(200, 500, output)
    p.showPage()
    p.save()
    #fName='PV'+ str(pv_id) +'.pdf'
    fName=output+'.pdf'
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename=fName)
    #return HttpResponse("Your PDF is created.")
