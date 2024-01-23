
def verification_status(request):
    return {'is_verified': request.session.get('is_profiled', False)}