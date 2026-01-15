import csv
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .services.crawler import crawl_google_maps
from .models import Company

def index(request):
    return render(request, 'search/index.html')


def search(request):
    if request.method == 'POST':
        segment = request.POST.get('segment')
        city = request.POST.get('city')
        
        # Trigger crawler
        # Note: In production this should be a background task (Celery)
        # For this simple prototype, we run it synchronously (will block the page)
        results = crawl_google_maps(segment, city)
        
        return render(request, 'search/results.html', {'results': results, 'segment': segment, 'city': city})
    return redirect('index')

def export_csv(request):
    segment = request.GET.get('segment')
    city = request.GET.get('city')
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="companies_{segment}_{city}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Name', 'Segment', 'City', 'Phone', 'Website', 'Email', 'Social Media'])
    
    companies = Company.objects.filter(segment=segment, city=city)
    for company in companies:
        writer.writerow([
            company.name,
            company.segment,
            company.city,
            company.phone,
            company.website,
            company.email,
            company.social_media
        ])
        
    return response

def export_xml(request):
    segment = request.GET.get('segment')
    city = request.GET.get('city')
    
    companies = Company.objects.filter(segment=segment, city=city)
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<companies>\n'
    for company in companies:
        xml_content += '  <company>\n'
        xml_content += f'    <name>{company.name}</name>\n'
        xml_content += f'    <segment>{company.segment}</segment>\n'
        xml_content += f'    <city>{company.city}</city>\n'
        xml_content += f'    <phone>{company.phone if company.phone else ""}</phone>\n'
        xml_content += f'    <website>{company.website if company.website else ""}</website>\n'
        xml_content += f'    <email>{company.email if company.email else ""}</email>\n'
        # Simple representation for social media
        xml_content += f'    <social_media>{company.social_media}</social_media>\n'
        xml_content += '  </company>\n'
    xml_content += '</companies>'
    
    response = HttpResponse(xml_content, content_type='application/xml')
    response['Content-Disposition'] = f'attachment; filename="companies_{segment}_{city}.xml"'
    return response
