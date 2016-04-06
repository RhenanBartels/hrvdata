import datetime
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

import hrv.hrv as hrv

def index(request, filename):
    metadata = {'username':request.user, 'filename': filename, "date":
            datetime.date.today().strftime('%m-%d-%Y')}
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

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setFont("Helvetica", 25)
    p.drawString(90, 800, "Report gerenated from hrvdata.org")
    p.setFont("Helvetica", 14)
    p.drawString(20, 750, "File Name: " + metadata["filename"])
    p.drawString(450, 750, "Date: " + metadata["date"])

    p.line(20, 700, 570, 700)

    p.setFont("Helvetica-Bold", 20)
    p.drawString(240, 670, "USED SETTINGS")
    p.setFont("Helvetica", 16)
    p.drawString(70, 630, "Frequency Domain")
    p.drawString(400, 630, "Time Varying")

    p.setFont("Helvetica", 14)
    p.drawString(20, 600, "Method: Welch")
    p.drawString(380, 600, "Segment Size: 30")
    p.drawString(20, 580, "Segment Size: 256")
    p.drawString(380, 580, "Overlap Size: 0")
    p.drawString(20, 560, "Overlap Size: 128")
    p.drawString(20, 540, "Window Function: Hanning")
    p.drawString(20, 520, "Detrending Method: Linear")
    p.drawString(20, 500, "Zero Padding: 0")

    p.setFont("Helvetica-Bold", 20)
    p.drawString(260, 470, "RESULTS")
    #Draw the main results table
    p.line(120, 420, 520, 420)
    #Header
    p.setFont("Helvetica-Bold", 14)
    p.drawString(160, 435, "Time Domain")
    p.drawString(350, 435, "Frequency Domain")
    #Results
    p.setFont("Helvetica", 12)
    p.drawString(120, 405, "RMSSD (ms)")
    p.drawString(260, 405, "100")
    p.drawString(320, 405, "Total Power (ms)")
    p.drawString(455, 405, "10000.00")
    p.drawString(120, 385, "SDNN (ms)")
    p.drawString(260, 385, "100")
    p.drawString(320, 385, "VLF (ms)")
    p.drawString(460, 385, "100")
    p.drawString(120, 365, "pNN50 (%)")
    p.drawString(260, 365, "100")
    p.drawString(320, 365, "LF (ms)")
    p.drawString(460, 365, "100")
    p.drawString(120, 345, "mean RRi (ms)")
    p.drawString(260, 345, "100")
    p.drawString(320, 345, "HF (ms)")
    p.drawString(460, 345, "100")
    p.drawString(120, 325, "mean HR (bpm)")
    p.drawString(460, 325, "100")
    p.drawString(320, 325, "LF/HF")
    p.drawString(460, 325, "100")
#    p.drawString(120, 285, "mean HR (bpm)")
    p.drawString(320, 305, "LFn.u")
    p.drawString(460, 305, "100")
    p.drawString(320, 285, "HFn.u")
    p.drawString(460, 285, "100")
    p.line(120, 280, 500, 280)

#    p.setFont("Helvetica", 24)
#    p.drawString(260, 660, "Tachogram")
#
    #TODO:replace getip() for time in miliseconds

#    p.setFont("Helvetica", 16)

    fig_size = (6.25, 2.0)

    fig = plt.figure(frameon=False, figsize=fig_size)
    plt.plot(rri, 'y')
    plt.ylabel("RRi (ms)")
    plt.axis('tight')
    p.setFont("Helvetica-Bold", 14)
    p.drawString(270, 250, "Tachogram")

    tachogram_position = 46
    filename = '/tmp/guess_my_name.%s.png' % os.getpid()
    with open(filename, 'w') as tmpfile:
        fig.savefig(tmpfile, format="png") # File position is at the end of the file.
        tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
        p.drawImage(tmpfile.name, 0, tachogram_position)
    os.remove(filename)
    p.drawString(290, 25, "Time (s)")

    #Page Break
    p.showPage()

    tachogram_position = 600

    psd, _ = hrv.frequency_domain(rri)

    fig1, ax1 = plt.subplots(figsize=fig_size)
    ax1.plot(psd[0], psd[1])
    plt.ylabel(r"PSD ($ms^2/Hz$)")
    ax1.yaxis.get_major_formatter().set_powerlimits((0, 1))
    plt.fill_between(psd[0], psd[1], color="#0097ff")
    plt.xlim(0, 0.5)
    filename = '/tmp/psd.%s.png' % os.getpid()
    with open(filename, 'w') as tmpfile:
        fig1.savefig(tmpfile, format="png") # File position is at the end of the file.
        tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
        p.drawImage(tmpfile.name, 0, tachogram_position)
    os.remove(filename)

    p.setFont("Helvetica-Bold", 14)
    p.drawString(270, 575, "Frequency (Hz)")
    indices_names = ["RMSSD (ms)", "SDNN (ms)", "pNN50 (%)", "mean RRi (ms)",
            "mean HR (bpm)"]
    p.setFont("Helvetica-Bold", 18)
    p.drawString(250, 535, "Time Varying")
    p.setFont("Helvetica-Bold", 14)
    #Time Varying Figures
    cont = 1
    tv_indices = hrv.time_varying(rri)
    for name, indice in enumerate(tv_indices[1:len(tv_indices)]):
        fig_tv = plt.figure(frameon=False, figsize=fig_size)
        plt.plot(tv_indices[0], indice, 'o-')
        plt.ylabel(indices_names[name])
        filename = '/tmp/tv%f%s.png' % (os.getpid(), indice[0])
        with open(filename, 'w') as tmpfile:
            fig_tv.savefig(tmpfile, format="png") # File position is at the end of the file.
            tmpfile.seek(0) # Rewind the file. (0: the beginning of the file)
            timevarying_position = tachogram_position - cont * 270
            if timevarying_position < 0:
                timevarying_position = tachogram_position
                p.showPage()
                cont = 0
            p.drawImage(tmpfile.name, 0, timevarying_position)
            p.setFont("Helvetica-Bold", 14)
            p.drawString(270, timevarying_position - 25, "Time (s)")
            cont += 1
        os.remove(filename)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response

