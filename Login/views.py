from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                rol = getattr(user, 'rol', None)

                if rol in ['admin', 'vendedor']:
                    login(request, user)
                    request.session['member_id'] = user.id
                    messages.success(request,'Sesion Iniciada!')
                    return redirect('Inicio')
                else:
                    messages.error(request, 'Tu rol no tiene acceso autorizado.')
            else:
                messages.error(request, 'Tu usuario está inactivo.')
        else:
            messages.error(request, 'Credenciales inválidas.')

        return redirect('/')

    return render(request, 'Login/login.html', {'form': form})


def logout_out(request):
    try:
        del request.session['member_id']
        logout(request)
        messages.success(request, 'Sesion Finalizada con Exito')
        return redirect('Login')
    except AttributeError:
        return redirect('/')