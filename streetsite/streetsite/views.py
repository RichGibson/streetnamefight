
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import os
import re
import sys
from django.db import connection, transaction
from streetsite.models import Fight


def home(request):
    return HttpResponse( 'KFWI!', mimetype='text/html')

def fid(request,word):
    """ look up a fid in the feature table """
    connection.text_factory=str
    cursor = connection.cursor()

    cursor.execute(' select f.fid, f.street, f.zip, p.city, p.state, p.lat, p.lon, p.fips_county from feature f, place p where f.zip=p.zip and f.fid=%s', [word])
    data = cursor.fetchall()
    return render_to_response('fid.html', {'data':data} )

def build_query_string(list):
    return ','.join(['%s'] * len(list))

def pastfights(request):
    """ show us past fights with links to refight them """
    data = Fight.objects.all().order_by('-id')
    return render_to_response('pastfights.html',{'data':data})

def fight(request):
    connection.text_factory=str
    cursor = connection.cursor()
    #import pdb
    #pdb.set_trace()
    l=[]
    if 'words' in request.GET:
        words = request.GET['words']
        f = Fight()
        f.word = words
        f.save()
        l=words.split()
        w = build_query_string(l)
        sql = "select word, count(word) as cnt  from street_word where word in (%s) group by word order by cnt desc" %w
        #import pdb
        #pdb.set_trace()
        cursor.execute(sql,l)
        data = cursor.fetchall()
        
    else:
        w = """'Washington', 'Adams','Jefferson','Madison','Monroe', 'Adams', 'Jackson','Buren','Harrison', 'Tyler','Polk','Taylor','Filmore','Pierce','Buchanan','Lincoln','Johnson','Grant','Hayes','Garfield','Arthur','Cleveland', 'Harrison','McKinkley','Mckinley','Roosevelt','Wilson','Harding','Taft','Coolidge','Hoover','Truman','Eisenhower','Kennedy','Nixon','Ford','Carter','Reagan','Bush','Clinton','Obama'"""
        sql = "select word, count(word) as cnt  from street_word where word in (%s) group by word order by cnt desc"
        cursor.execute(sql,[w])
        data = cursor.fetchall()
    # Data retrieval operation - no commit required
    
    #sql = "select word, count(word) as cnt  from street_word where word in ('Love', 'Dreams','Wisdom','Money','Truth') group by word order by cnt desc"
    return render_to_response('fight.html', {'data':data} )
    #return HttpResponse(data, mimetype='text/html')

def streetword(request,word):
    """ look up a word in the feature table """
    connection.text_factory=str
    cursor = connection.cursor()

    # Data retrieval operation - no commit required
    #sql = "select fid, street, zip from feature where street like '%%' order by zip"
    #import pdb
    #pdb.set_trace()
    sql = "select street, count(street) from feature where fid in (select fid from street_word where word=%s) order by zip"
    #sql = "select fid, street, zip from feature where fid in (select * from streetword where word=?) order by zip"
    #print >>sys.stderr, sql
    cursor.execute(sql, [word])
    #cursor.execute(sql' select fid, street, zip from feature where fid in (select fid from street_word where word=%s) order by zip ',[word])
    #cursor.execute(sql,[word])
    #cursor.execute(sql,[word])
    data = cursor.fetchall()
    return render_to_response('streetword.html', {'data':data} )

