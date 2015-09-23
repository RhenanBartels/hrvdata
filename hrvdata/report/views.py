import tempfile
import os

from io import BytesIO

from reportlab.pdfgen import canvas
from django.http import HttpResponse

from PIL import Image
import matplotlib.pyplot as plt
from reportlab.lib.units import cm, mm, inch, pica

from upload.models import Tachogram
from analysis.views import get_file_information

import hrv

def index(request, filename):
    metadata = {'username':request.user, 'filename': filename}
    rri_obj = Tachogram.objects.get(owner=request.user, filename=filename)
    rri = get_file_information(rri_obj)
    return render_report(metadata, rri)

def render_report(metadata, rri):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="somefilename.pdf"'

    buffer = BytesIO()

    # Create the PDF object, using the BytesIO object as its "file."
    p = canvas.Canvas(buffer)

    fig_size = (6.25, 2.5)

    fig = plt.figure(frameon=False, figsize=fig_size)
    plt.plot(rri, 'y')
    plt.ylabel("RRi (ms)")
    plt.axis('tight')

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 700, "PDF report gerenate from hrvdata.org")
    p.drawString(100, 680, "File Name: " + metadata["filename"])
    p.drawString(300, 650, "Tachogram")
    p.drawString(300, 380, "Time (s)")

    tachogram_position = 400

    #TODO:replace getip() for time in miliseconds

    filename = '/tmp/guess_my_name.%s.png' % os.getpid()
    with open(filename, 'w') as tmpfile:
        fig.savefig(tmpfile, format="png") # File position is at the end of the file.
        tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
        p.drawImage(tmpfile.name, 0, tachogram_position)
    os.remove(filename)

    tachogram_position = 400

    psd, _ = hrv.frequency_domain(rri)
    fig1 = plt.figure(frameon=False, figsize=fig_size)
    plt.plot(psd[0], psd[1])
    plt.fill_between(psd[0], psd[1], color="#0097ff")
    plt.xlim(0, 0.5)
    filename = '/tmp/psd.%s.png' % os.getpid()
    with open(filename, 'w') as tmpfile:
        fig1.savefig(tmpfile, format="png") # File position is at the end of the file.
        tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
        p.drawImage(tmpfile.name, 0, tachogram_position)
    os.remove(filename)

#    indices_names = ["RMSSD (ms)", "SDNN (ms)", "pNN50 (%)", "mean RRi (ms)",
#            "mean HR (bpm)"]
#    #Time Varying Figures
#    cont = 1
#    tv_indices = hrv.time_varying(rri)
#    for name, indice in enumerate(tv_indices[1:len(tv_indices)]):
#        fig_tv = plt.figure(frameon=False, figsize=fig_size)
#        plt.plot(tv_indices[0], indice, 'o-')
#        plt.ylabel(indices_names[name])
#        filename = '/tmp/tv%f%s.png' % (os.getpid(), indice[0])
#        with open(filename, 'w') as tmpfile:
#            fig_tv.savefig(tmpfile, format="png") # File position is at the end of the file.
#            tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
#            timevarying_position = tachogram_position - cont * 250
#            if timevarying_position < 0:
#                timevarying_position = tachogram_position
#                p.showPage()
#                cont = 0
#            p.drawImage(tmpfile.name, 0, timevarying_position)
#            cont += 1
#        os.remove(filename)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

