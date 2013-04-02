
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
import os
import re
import sys
from django.db import connection, transaction
from streetsite.models import Fight


def home(request):
    st = ' KFWI! <p> <a href="/fight">Go and Fight!</a> '

    return HttpResponse(st, mimetype='text/html')

def fid(request,word):
    """ look up a fid in the feature table """
    connection.text_factory=str
    cursor = connection.cursor()
    sql = """
            select f.fid, f.street, f.zip, count(f.fid) as cnt 
            from feature f, edge e, feature_edge fe 
            where f.fid=fe.fid and e.tlid=fe.tlid and f.fid=857307 
            group by f.fid, f.zip order by f.street
     """

    cursor.execute(' select f.fid, f.street, f.zip, p.city, p.state, p.lat, p.lon, p.fips_county from feature f, place p where f.zip=p.zip and f.fid=%s', [word])
    data = cursor.fetchall()
    return render_to_response('fid.html', {'data':data} )

def street(request,street):
    """ look up a street in the feature table """
    connection.text_factory=str
    cursor = connection.cursor()

    cursor.execute(' select f.fid, f.street, f.zip, p.city, p.state, p.lat, p.lon, p.fips_county from feature f, place p where f.zip=p.zip and f.street=%s', [street])
    data = cursor.fetchall()
    return render_to_response('fid.html', {'data':data} )

def zip(request,zip):
    """ look up a street in the feature table """
    connection.text_factory=str
    cursor = connection.cursor()
    sql = """
            select distinct f.street, f.zip 
            from feature f where f.zip=%s order by street """

    sql = """
            select f.fid, f.street, f.zip, count(f.fid) as cnt 
            from feature f, edge e, feature_edge fe 
            where f.fid=fe.fid and e.tlid=fe.tlid and f.zip=%s
            group by f.fid, f.zip order by f.street
     """


    cursor.execute(sql, [zip])
    #cursor.execute(' select f.fid, f.street, f.zip, p.city, p.state, p.lat, p.lon, p.fips_county from feature f, place p where f.zip=p.zip and f.street=%s', [street])
    data = cursor.fetchall()

    sql = """
            select  count(distinct f.fid) as street_count, 
            count(distinct e.tlid) as segment_count 
            from feature f, edge e, feature_edge fe 
            where f.fid=fe.fid and e.tlid=fe.tlid and f.zip=%s;
          """

    cursor.execute(sql, [zip])
    totals = cursor.fetchall()

    return render_to_response('zip.html', {'data':data, 'totals':totals} )

def zip_form(request):
    if 'zip' in request.GET:
        return zip(request, request.GET['zip'])


def build_query_string(list):
    return ','.join(['%s'] * len(list))

def pastfights(request):
    """ show us past fights with links to refight them """
    #data = Fight.objects.all().order_by('-id')


    sql = """ select distinct word, count(word) as cnt , max(id) as max 
              from streetsite_fight group by word order by max desc; """
    connection.text_factory=str
    cursor = connection.cursor()
    cursor.execute(sql,[])
    data = cursor.fetchall()

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
    sql="""select street, count(street) as cnt from feature 
            where fid in (select fid from street_word where word=%s) 
            group by street order by cnt desc"""

    cursor.execute(sql, [word])
    #cursor.execute(sql' select fid, street, zip from feature where fid in (select fid from street_word where word=%s) order by zip ',[word])
    #cursor.execute(sql,[word])
    #cursor.execute(sql,[word])
    data = cursor.fetchall()
    return render_to_response('streetword.html', {'data':data} )

