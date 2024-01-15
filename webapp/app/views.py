from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views import View
from django.conf import settings
import os
import qrcode


# Main App View
def home(request):
    return render(request, 'home.html')

# Miguel's Resume & Download Resume View 
def resume(request):
    return render(request, 'resume.html')

# Miguels Projects View   
def projects(request):
    return render(request, 'projects.html')

# Contact Miguel View
def contact(request):
    return render(request, 'contact.html')


# QR Code
def generate_qr_code(request):
    website_url = "https://www.conqueringtechnology.com"

    # Adjust box_size for QR code size
    box_size = 2
    
    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=4,
    )
    qr.add_data(website_url)
    qr.make(fit=True)

    # Create an image from the QR code
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image or serve it directly in the response
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response


# View Project Files
def project_files(request, pdf_filename):
    # Locate the FIles
    project_files_path = os.path.join(settings.BASE_DIR, 'static', 'docs', 'pdf', pdf_filename)

    # Serve the Files
    if os.path.exists(project_files_path):
        response = FileResponse(open(project_files_path, 'rb'))
        response['Content-Type'] = 'application/pdf'
        return response
    else:
        # Display a message if the file is not found
        download_message = 'File not found.'
        download_message_type = 'danger'
    return render(request, 'projects.html', {'download_message': download_message, 'download_message_type': download_message_type})


# Download Miguel Resume
class DownloadResumeView(View):
    def get(self, request, *args, **kwargs):
        file_to_download = 'miguel_rocha_resume.pdf'
        resume_path = os.path.join(settings.BASE_DIR, 'static', 'docs', 'pdf', file_to_download)

        if os.path.exists(resume_path):
            response = FileResponse(open(resume_path, 'rb'))
            response['Content-Type'] = 'application/pdf'
            response['Content-Disposition'] = 'attachment; filename="miguel_rocha_resume.pdf"'
            return response
        else:
            # Display a message if the file is not found
            download_message = 'Resume not found.'
            download_message_type = 'danger'
            return render(request, 'resume.html', {'download_message': download_message, 'download_message_type': download_message_type})
        

