from django.shortcuts import render
import sys
from io import StringIO



def knzl_view(request):
    if 'runserver' in sys.argv:
        if request.method == 'POST':
            code = request.POST.get('code')  
            captured_output = ""
            output = StringIO()
            try:
                sys.stdout = output
                exec(code)
            except Exception as e:
                print(e)
            sys.stdout = sys.__stdout__
            captured_output = output.getvalue()
            captured_output = captured_output.strip().replace('\n', '\n')
            return render(request, 'knzl_new.html', {'out': captured_output, 'code':code})
        else:
             return render(request, 'knzl.html')
    else:
        print("La aplicación está en entorno de producción.")
        return render(request, 'notWorking.html')
    
def knzl_command(request):

    print("Test running !!!")
    return render(request, 'notWorking.html')
