def roles(request):
    user = request.user
    return {
        'is_assistant': user.is_authenticated
                        and user.groups.filter(name='Assistant').exists()
    }