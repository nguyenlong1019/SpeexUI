from django.http import HttpResponse, JsonResponse 
from core.models.log import AccessLog 
from libs.utils import get_client_ip, get_headers_dict, get_ip_info 
import json 
from django.conf import settings 


def access_log_api(request):
    if settings.DB_MODE == 'production':
        data = json.loads(request.body)
        page_name = data.get('pn')
        ip = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        referer = request.META.get('HTTP_REFERER', '')
        headers = get_headers_dict(request)
        path = request.META.get('PATH_INFO', '')
        
        access_log = AccessLog.objects.create(
            page_name=page_name,
            ip_address=ip,
            user_agent=user_agent,
            referer=referer,
            headers=headers,
            request_path=path
        )

        ip_data = get_ip_info(ip)
        if ip_data:
            access_log.country = ip_data.get('country')
            access_log.country_code = ip_data.get('country_code')
            access_log.ip_json = ip_data.get('data')
            access_log.save()
        
    return JsonResponse({
        'msg': 'ok'
    }, status=200) 
