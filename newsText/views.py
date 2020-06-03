from django.shortcuts import render
from django.shortcuts import  HttpResponse
from newsText import textget


# Create your views here.
# 将请求定位到index.html文件中
def index(request):
    data = textget.mainMethod()
    return render(request,'index.html',{'data_weekly': data[0],'data_monthly':data[1],'data_daily':data[2],'number':[1,2,3,4,5,6,7,8,9,10]})

def search(request):
    return render(request,'search.html')
