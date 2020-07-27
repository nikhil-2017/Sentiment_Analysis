import csv
from django.core.paginator import Paginator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from .models import fileupload, overall_rating, individual_rating, individual
from .form import fileUploadForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.shortcuts import render, render_to_response, redirect
import random
import datetime
import time
import os
from googletrans import Translator
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    TemplateView,
    ListView, 
    DetailView, 
    CreateView,
    UpdateView,
    DeleteView
)

def mailid(request,id):
    file = get_object_or_404(overall_rating, pk=id)
    form1 = file.positive
    form2 = file.negative
    form3 = file.neutral
    form4 = file.filename
    form5 = file.process_date
    form6 = file.rat
    form7 = file.rating
    host = "smtp.gmail.com"
    port = 587
    username = "email@gmail.com"
    password = "pwd"
    from_email = 'email@gmail.com'
    to_list = ['second_mail@gmail.com']
    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = str("Report {}".format(form4))
        the_msg["From"] = from_email
        the_msg["To"] = to_list[0]
        plain_txt = "Testing the message"
        html_txt ="""\
        <html>

<head>
    
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
    <style>
        @page {
            @bottom-right {
                content: counter(page) " of " counter(pages);
            }
        }
        .table-bordered > tbody > tr > td{
            border:1px solid black;
}
    </style>
</head>
        <div class="container" style="page-break-before: always;">
        <div class="row">
            
        </div><br>
        
       
        
        <table class="table table-bordered table-condensed">
            <tbody>
              
                <tr>
                    <td>
                        <h4>
                            <strong>File name:</strong>
                        </h4>
                        <span>"""+str(form4)+"""</span><br>
                        <span><small class="text-muted">Date&Time : """+str(form5)+"""</small></span>
                    </td>
                </tr>
                <tr>
                    <td>

                        <h4>
                            <strong>Overall Rating:</strong>
                        </h4>
                        <span>""" +str(form6)+"""</span><br>

                        <h4>
                            <strong>Rating:</strong>
                        </h4>
                        <span>Positive:""" +str(form1)+"""</span><br>
                        <span>Negative: """+str(form2)+"""</span><br>
                        <span>Neutral: """+str(form3)+"""</span><br>
                        <span>Rating: """+str(form7)+"""</span>

                    </td>
                </tr>
              </tbody>
            </table><br>
</body>
</html>

        """
        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, "html")
        the_msg.attach(part_1)
        the_msg.attach(part_2)
        email_conn.sendmail(from_email, to_list, the_msg.as_string())
        email_conn.quit()
    except smtplib.SMTPException:
        print("error sending message")


    return render(request,'sentiment/analysis.html')


def mail(request):
    file = overall_rating.objects.latest('id')
    form1 = file.positive
    form2 = file.negative
    form3 = file.neutral
    form4 = file.filename
    form5 = file.process_date
    form6 = file.rat
    form7 = file.rating
    host = "smtp.gmail.com"
    port = 587
    username = "email@gmail.com"
    password = "pwd"
    from_email = 'email@gmail.com'
    to_list = ['second_email@gmail.com']
    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = "Report"
        the_msg["From"] = from_email
        the_msg["To"] = to_list[0]
        plain_txt = "Testing the message"
        html_txt ="""\
        <html>

<head>
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['corechart']});
      google.charts.setOnLoadCallback(drawChart);

      function drawChart() {

        var graph = document.getElementById('p');
        var data = google.visualization.arrayToDataTable([
          ['Review', 'Rating'],
          ['Positive', """+str(form1)+"""],
          ['Negative', """+str(form2)+"""],
          ['Neutral',  """+str(form3)+"""],
        ]);

        var options = {
          title: 'Overall Ratings'
        };

        var chart = new google.visualization.PieChart(document.getElementById('piechart'));

        chart.draw(data, options);
      }
    </script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
    <style>
        @page {
            @bottom-right {
                content: counter(page) " of " counter(pages);
            }
        }
        .table-bordered > tbody > tr > td{
            border:1px solid black;
}
    </style>
</head>
        <div class="container" style="page-break-before: always;">
        <div class="row">
            
        </div><br>
        
       
        
        <table class="table table-bordered table-condensed">
            <tbody>
              
                <tr>
                    <td>
                        <h6>
                            <strong>File name:</strong>
                        </h6>
                        <span>"""+str(form4)+"""</span><br>
                        <span><small class="text-muted">"""+str(form5)+"""</small></span>
                    </td>
                </tr>
                <tr>
                    <td>
                        <h6>
                            <strong>Rating:</strong>
                        </h6>
                        <span>Positive:""" +str(form1)+"""</span><br>
                        <span>Negative: """+str(form2)+"""</span><br>
                        <span>Neutral: """+str(form3)+"""</span>
                    </td>
                </tr>
              </tbody>
            </table><br>
    <div role="main" class="container">
        <div class="row">
            <div class="col-md-2"></div>
            <div class="col-md-7">            
                    <article class="media content-section">
                        <div class="media-body">
                          <div class="article-metadata">
                            <a class="mr-2" href="#">"""+str(form4)+"""</a>
                            <small class="text-muted">"""+str(form5)+"""</small>
                          </div>
                          <div class="table-responsive-sm">
                            <table class="table">
                                <thead>
                                    <tr>
                                      <th scope="col">Overall Rating</th>
                                      <th scope="col">Positive</th>
                                      <th scope="col">Negative</th>
                                      <th scope="col">Neutral</th>
                                      <th scope="col">Rating</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    <tr>
                                      <th scope="row">"""+str(form6)+"""%</th>
                                      <td>"""+str(form1)+"""%</td>
                                      <td>"""+str(form2)+"""%</td>
                                      <td>"""+str(form3)+"""%</td>
                                      <td>"""+str(form7)+"""%</td>
                                    </tr>
                                  </tbody>
                            </table>
                          </div>
                        </div>
                      </article>
            </div>
    </div>
    <div id="piechart" style="width: 800px; height: 350px;"></div>
    <script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
</body>
</html>

        """
        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, "html")
        the_msg.attach(part_1)
        the_msg.attach(part_2)
        email_conn.sendmail(from_email, to_list, the_msg.as_string())
        email_conn.quit()
    except smtplib.SMTPException:
        print("error sending message")


    return render(request,'sentiment/analysis.html')


class fileListView(ListView):
    model = fileupload
    template_name = 'sentiment/home.html'
    context_object_name = 'file'
    ordering = ['-upload_date'] 
    paginate_by = 4

class UserFileListView(ListView):
    model = fileupload
    template_name = 'sentiment/user_fileupload.html'
    context_object_name = 'file'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return fileupload.objects.filter(user=user).order_by('-upload_date')



class fileDetailView(DetailView):
    model = fileupload


class fileCreateView(LoginRequiredMixin ,CreateView):
    model = fileupload
    
    fields = ['filename','filetype']

    def form_valid(self, form):
        form.instance.user = self.request.user
        filename = form.cleaned_data.get('filename')
        filetype = str(form.cleaned_data.get('filetype'))
        messages.success(self.request, f'Uploaded filename is "{filename}" and filetype is media/filefolder/{filetype}!')
        return super().form_valid(form)


class fileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = fileupload
    success_url = '/sentiment/'
    
    def test_func(self):
        fileupload = self.get_object()
        if self.request.user == fileupload.user:
            return True
        return False

def about(request):
    return render(request,'sentiment/about.html')

class PocessingDetail(ListView):
    model = [fileupload, individual_rating]
    template_name = 'sentiment/search.html'
    ordering = ['-upload_date'] 
    success_url = '/'

    def get_queryset(self):
        filename = self.request.GET.get('q')
        user = self.request.user
        object_list = fileupload.objects.filter(Q(filename__icontains=filename))

        filename1 = str(filename)
        filename = str('media/filefolder/{}'.format(filename))
        sfile = filename1.split('.')
        print(sfile)
        sfile1 = str(sfile[0])
        print(sfile)

        analyzer = SentimentIntensityAnalyzer()
        translator = Translator()

        count = 0
        pos_count = 0
        pos_correct = 0
        neg_count = 0
        neg_correct = 0
        neu_count = 0
        neu_correct = 0
        rat = 0

        print("\n")
        with open(filename,'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                rating = float(line[4])
                rt = line[5]
                trans = translator.translate(line[5]).text

                vs = analyzer.polarity_scores(trans)
                if vs['compound'] > 0.3:
                    pos_correct += 1
                    pos_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (POSITIVE {}%) ".format(trans, vs['pos']*100), end='\n')
                    rat1 = str('Positive : {}'.format(vs['pos']*100))
                    individual.objects.create(filename=filename1,review_text=rt, process_review=trans,positive=vs['pos']*100,negative=vs['neg']*100,neutral=vs['neu']*100,rat=rat1)

                elif vs['compound'] < -0.3:
                    neg_correct += 1
                    neg_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (NEGATIVE {}%) ".format(trans, vs['neg']*100), end='\n')
                    rat1 = str('Negative : {}'.format(vs['neg']*100))
                    individual.objects.create(filename=filename1,review_text=rt, process_review=trans, positive=vs['pos']*100,negative=vs['neg']*100,neutral=vs['neu']*100,rat=rat1)
                elif (vs['compound'] <= 0.3 and vs['compound'] >= -0.3):
                    neu_correct += 1
                    neu_count += 1
                    print(" - {:-<65} ===> {}% ".format(trans, vs), end='\n')
                    print(" - {:-<65} ===> (NEUTRAL {}%) ".format(trans, vs['neu']*100), end='\n')
                    rat1 = str('Neutral : {}'.format(vs['neu']*100))
                    individual.objects.create(filename=filename1,review_text=rt, process_review=trans, positive=vs['pos']*100,negative=vs['neg']*100,neutral=vs['neu']*100,rat=rat1)
                print(rating)
                rat += rating
                print(rat)
                count += 1

        print("\n")
        print("Total count = {} sentences".format(count))
        print("Positive Accuracy = {}% , {} positive sentences".format(pos_correct / count * 100.0, pos_count))
        print("Negative Accuracy = {}% , {} negative sentences".format(neg_correct / count * 100.0, neg_count))
        print("Neutral Accuracy = {}% , {} neutral sentences".format(neu_correct / count * 100.0, neu_count))        
        print("Rating Accuracy = {}% , {} Rating sentences".format(rat / count * 10.0 + rat / count * 10.0, count))
        print("\n")

        pos = pos_correct/count*100.0
        neg = neg_correct/count*100.0
        neu = neu_correct/count*100.0
        rating = rat/count*10.0 + rat/count*10.0

        if pos > neg :
            overall = str('Positive : {} '.format(pos))
            print(overall)
            overall_rating.objects.create(filename=filename1,rating=rating,positive=pos,negative=neg,neutral=neu,rat=overall,user=user)
        elif neu > neg:
            overall = str('Neutral : {} '.format(neu))
            print(overall)
            overall_rating.objects.create(filename=filename1,rating=rating,positive=pos,negative=neg,neutral=neu,rat=overall,user=user)
        else:
            overall = str('Negative : {} '.format(neg))
            print(overall)
            overall_rating.objects.create(filename=filename1,rating=rating,positive=pos,negative=neg,neutral=neu,rat=overall,user=user)

        with open(filename,'r',encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            next(csv_reader)
            for line in csv_reader:
                product_id = line[0]
                product_name = line[1]
                category = line[2]
                review_date = line[3]
                rating = line[4]
                review_text = line[5]
                trans = translator.translate(line[5]).text
                vs = analyzer.polarity_scores(trans)
                pos = vs['pos']*100
                neg = vs['neg']*100
                neu = vs['neu']*100
                f=overall_rating.objects.get(filename=filename1)
                individual_rating.objects.create(filename=f,product_id=product_id,product_name=product_name,review_date=review_date,review_text=review_text,process_review=trans,rating=rating,positive=pos,negative=neg,neutral=neu)


@login_required
def filehome(request):
    context = {
        'ov': overall_rating.objects.all()
    }
    return render(request,'sentiment/filehome.html',context)

class fileoverallListView(ListView):
    model = overall_rating
    template_name = 'sentiment/filehome.html'
    context_object_name = 'ov'
    ordering = ['-process_date'] 
    paginate_by = 6

class UserPostListView(ListView):
    model = overall_rating
    template_name = 'sentiment/user_file.html'
    context_object_name = 'ov'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return overall_rating.objects.filter(user=user).order_by('-process_date')


class fileoverallDetailView(DetailView):
    model = overall_rating

class fileoverallDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = overall_rating
    success_url = '/sentiment/filehome/'

    def test_func(self):
        overall_rating = self.get_object()
        if self.request.user == overall_rating.user:
            return True
        return False


@login_required
def individualhome(request):
    context = {
        'ir': individual_rating.objects.all()
    }
    return render(request,'sentiment/individualhome.html',context)

class individualListView(ListView):
    model = individual_rating
    template_name = 'sentiment/individualhome.html'
    context_object_name = 'ir'
    ordering = ['-id'] 
    paginate_by = 6

class filenameListView(ListView):
    model = individual_rating
    template_name = 'sentiment/filename.html'
    context_object_name = 'ir'

    def get_queryset(self):
        filename = get_object_or_404(individual_rating, filename=self.kwargs.get('filename'))
        filename = str(filename)
        print(filename)
        sfile = str(filename.split("."))
        print(sfile)
        return individual_rating.objects.filter(filename=sfile).order_by('-id')

class individualDetailView(DetailView):
    model = individual_rating


class individualDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = individual_rating
    success_url = '/sentiment/individualhome/'

    def test_func(self):
        return True

@login_required
def piechart(request):
    form = overall_rating.objects.latest('id')
    form1 = form.positive
    form2 = form.negative
    form3 = form.neutral
    context = {
        'form': overall_rating.objects.latest('id')
    }
    return render(request, 'sentiment/piechart.html', {'form1':form1, 'form2':form2, 'form3':form3,'context':context})


def indhome(request):
    context = {
        'ir': individual.objects.all()
    }
    return render(request,'sentiment/indhome.html',context)


class indListView(ListView):
    model = individual
    template_name = 'sentiment/indhome.html'
    context_object_name = 'ir'
    ordering = ['-id'] 
    paginate_by = 6


def piechart1(request):
    i = request.GET.get('q')
    form = overall_rating.objects.get(id=i)
    form1 = form.positive
    form2 = form.negative
    form3 = form.neutral
    context = {
        'form': overall_rating.objects.get(id=i)
    }
    return render(request, 'sentiment/piechart1.html', {'form1':form1, 'form2':form2, 'form3':form3,'context':context})

def piechart2(request):
    i = request.GET.get('q')
    form = individual.objects.get(id=i)
    form1 = form.positive
    form2 = form.negative
    form3 = form.neutral
    context = {
        'form': individual.objects.get(id=i)
    }
    return render(request, 'sentiment/piechart2.html', {'form1':form1, 'form2':form2, 'form3':form3,'context':context})

class piechartDetailView(DetailView):
    model = overall_rating


def piedetail(request,ov_id):
    detailblog = get_object_or_404(overall_rating, pk=ov_id)
    return render(request,'sentiment/piechartdetail.html',{'detailblog':detailblog})

def pieinddetail(request,ind_id):
    inddetail = get_object_or_404(individual, pk=ind_id)
    return render(request,'sentiment/piechart_inddetail.html',{'inddetail':inddetail})

def pieinddetail1(request,ind_id):
    inddetail = get_object_or_404(individual_rating, pk=ind_id)
    return render(request,'sentiment/piechart_inddetail1.html',{'inddetail':inddetail})

def filedetail(request,filename):
    filedetail = individual_rating.objects.filter(filename__filename=filename).order_by('-id')
    filename = filename
    return render(request,'sentiment/filedetail.html',{'filedetail':filedetail, 'filename': filename })

from django.db.models import Avg, Max, Min, Sum
def productdetail(request,product_name):
    product_detail = individual_rating.objects.filter(product_name=product_name)
    pos_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('positive'))
    neg_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('negative'))
    neu_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('neutral'))
    rat_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('rating'))
    
    positive_avg = pos_avg["positive__avg"]
    negative_avg = neg_avg["negative__avg"]
    neutral_avg = neu_avg["neutral__avg"]
    rating_avg = rat_avg["rating__avg"]

    avg = {
        'pos_avg': float(positive_avg),
        'neg_avg': float(negative_avg),
        'neu_avg': float(neutral_avg),
        'rating_avg': float(rating_avg)
    }
    print('{} {} {} {}'.format(positive_avg, negative_avg, neutral_avg, rating_avg))
    product_name = product_name
    return render(request,'sentiment/productdetail.html',{'product_detail':product_detail, 'product_name': product_name, 'avg':avg })


def avg_piedetail(request,product_name):
    
    product_detail = individual_rating.objects.filter(product_name=product_name)
    pos_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('positive'))
    neg_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('negative'))
    neu_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('neutral'))
    rat_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('rating'))
    
    positive_avg = pos_avg["positive__avg"]
    negative_avg = neg_avg["negative__avg"]
    neutral_avg = neu_avg["neutral__avg"]
    rating_avg = rat_avg["rating__avg"]

    avg = {
        'pos_avg': float(positive_avg),
        'neg_avg': float(negative_avg),
        'neu_avg': float(neutral_avg),
        'rating_avg': float(rating_avg)
    }
    print('{} {} {} {}'.format(positive_avg, negative_avg, neutral_avg, rating_avg))
    product_name = product_name

    return render(request,'sentiment/piechartdetail1.html',{'avg':avg, 'product_name':product_name})


def product_mail(request,product_name):
    product_detail = individual_rating.objects.filter(product_name=product_name)
    pos_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('positive'))
    neg_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('negative'))
    neu_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('neutral'))
    rat_avg = individual_rating.objects.filter(product_name=product_name).aggregate(Avg('rating'))
    
    positive_avg = float(pos_avg["positive__avg"])
    negative_avg = float(neg_avg["negative__avg"])
    neutral_avg = float(neu_avg["neutral__avg"])
    rating_avg = float(rat_avg["rating__avg"])
    
    form1 = positive_avg
    form2 = negative_avg
    form3 = neutral_avg
    form4 = product_name

    if positive_avg > negative_avg and positive_avg > neutral_avg :
        form6 = str("Positive : {}".format(positive_avg))
    elif negative_avg > neutral_avg :
        form6 = str("Negative : {}".format(negative_avg))
    else :
        form6 = str("Neutral : {}".format(neutral_avg))

    form7 = rating_avg
    host = "smtp.gmail.com"
    port = 587
    username = "email@gmail.com"
    password = "pwd"
    from_email = 'email@gmail.com'
    to_list = ['second_email@gmail.com']
    try:
        email_conn = smtplib.SMTP(host, port)
        email_conn.ehlo()
        email_conn.starttls()
        email_conn.login(username, password)
        the_msg = MIMEMultipart("alternative")
        the_msg['Subject'] = str("Report {}".format(form4))
        the_msg["From"] = from_email
        the_msg["To"] = to_list[0]
        plain_txt = "Testing the message"
        html_txt ="""\
        <html>

<head>
    
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm"
        crossorigin="anonymous">
    <style>
        @page {
            @bottom-right {
                content: counter(page) " of " counter(pages);
            }
        }
        .table-bordered > tbody > tr > td{
            border:1px solid black;
}
    </style>
</head>
        <div class="container" style="page-break-before: always;">
        <div class="row">
            
        </div><br>
        
       
        
        <table class="table table-bordered table-condensed">
            <tbody>
              
                <tr>
                    <td>
                        <h4>
                            <strong>Product name:</strong>
                        </h4>
                        <span>"""+str(form4)+"""</span><br>
                    </td>
                </tr>
                <tr>
                    <td>

                        <h4>
                            <strong>Overall Rating:</strong>
                        </h4>
                        <span>""" +str(form6)+"""</span><br>

                        <h4>
                            <strong>Rating:</strong>
                        </h4>
                        <span>Positive:""" +str(form1)+"""</span><br>
                        <span>Negative: """+str(form2)+"""</span><br>
                        <span>Neutral: """+str(form3)+"""</span><br>
                        <span>Rating: """+str(form7)+"""</span>

                    </td>
                </tr>
              </tbody>
            </table><br>
</body>
</html>

        """
        part_1 = MIMEText(plain_txt, 'plain')
        part_2 = MIMEText(html_txt, "html")
        the_msg.attach(part_1)
        the_msg.attach(part_2)
        email_conn.sendmail(from_email, to_list, the_msg.as_string())
        email_conn.quit()
    except smtplib.SMTPException:
        print("error sending message")


    return render(request,'sentiment/analysis.html')
