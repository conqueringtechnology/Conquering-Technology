from django.shortcuts import render
from django.http import HttpResponse, FileResponse
from django.views import View
from django.conf import settings
import os
import qrcode
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

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
def project_files(request, filename):
    # Determine the file type and folder based on the extension
    if filename.endswith('.pdf'):
        file_type = 'application/pdf'
        folder = 'pdf'
    elif filename.endswith('.zip'):
        file_type = 'application/zip'
        folder = 'zip'
    elif filename.endswith('.csv'):
        file_type = 'text/csv'
        folder = 'csv'
    else:
        # If the file extension is not supported, return an error message
        download_message = 'File type not supported.'
        download_message_type = 'danger'
        return render(request, 'projects.html', {'download_message': download_message, 'download_message_type': download_message_type})

    # Locate the file
    project_files_path = os.path.join(settings.BASE_DIR, 'static', 'docs', folder, filename)
    logging.debug(f"Looking for file at path: {project_files_path}")

    # Check if the file exists
    if os.path.exists(project_files_path):
        response = FileResponse(open(project_files_path, 'rb'))
        response['Content-Type'] = file_type
        
        # Check for the 'download' query parameter to set the Content-Disposition header
        if request.GET.get('download') == 'true':
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'inline; filename="{filename}"'
        
        return response
    else:
        # Display a message if the file is not found
        download_message = 'File not found.'
        download_message_type = 'danger'
        logging.error(f"File not found at path: {project_files_path}")
        return render(request, 'projects.html', {'download_message': download_message, 'download_message_type': download_message_type})


def project_files(request, filename):
    # Determine the file type and folder based on the extension
    if filename.endswith('.pdf'):
        file_type = 'application/pdf'
        folder = 'pdf'
    elif filename.endswith('.zip'):
        file_type = 'application/zip'
        folder = 'zip'
    elif filename.endswith('.csv'):
        file_type = 'text/csv'
        folder = 'csv'
    else:
        # If the file extension is not supported, return a 404 error
        download_message = 'File type not supported.'
        download_message_type = 'danger'
        return render(request, 'projects.html', {'download_message': download_message, 'download_message_type': download_message_type})

    # Locate the file
    project_files_path = os.path.join(settings.BASE_DIR, 'static', 'docs', folder, filename)
    logging.debug(f"Looking for file at path: {project_files_path}")

    # Serve the file
    if os.path.exists(project_files_path):
        response = FileResponse(open(project_files_path, 'rb'))
        response['Content-Type'] = file_type
        # Set Content-Disposition to 'inline' for PDFs and 'attachment' for others
        if file_type == 'application/pdf':
            response['Content-Disposition'] = f'inline; filename="{filename}"'
        else:
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        # Display a message if the file is not found
        download_message = 'File not found.'
        download_message_type = 'danger'
        logging.error(f"File not found at path: {project_files_path}")
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
        

