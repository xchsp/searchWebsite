from flask import render_template, redirect, request, make_response, url_for
from elasticsearch import Elasticsearch
from datetime import datetime

from . import blog
from .models import ElasticType

import json
import re


client = Elasticsearch(hosts=['127.0.0.1'])


@blog.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@blog.route('/suggest')
def suggest():
    re_datas = dict()
    key_words = request.args['s']
    if key_words:
        s = ElasticType.search()
        s = s.suggest('my_suggest', key_words, completion={
            "field": 'suggest', 'fuzzy': {
                'fuzziness': 2
            },
            'size': 10
        })
        suggestions = s.execute_suggest()

        for sug in suggestions.my_suggest[0].options:
            source = sug._source
            if len(source['title']) > 40:
                re_datas[source['title'][:40] + ' ...'] = source['url']
            else:
                re_datas[source['title']] = source['url']
    response = make_response(json.dumps(re_datas))
    response.mimetype = 'application/json'
    return response


@blog.route('/search', methods=['GET', 'POST'])
def search():
    key_words = request.args['q']
    start_time = datetime.now()
    if not key_words:
        return redirect(url_for(".index"))

    try:
        page = int(request.args['p'])
    except Exception as e:
        page = 1

    response = client.search(
        index='ready2search',
        body={
            "query":{
                "multi_match": {
                    "query": key_words,
                    "fields": ['title', 'html_content']
                }
            },
            "from": (page-1)*10,
            "size": 10,
            "highlight": {
                "pre_tags": ['<span class="keyWord">'],
                "post_tags": ['</span>'],
                "fields": {
                    "title": {},
                    "html_content": {},
                },
            }
        }
    )
    end_time = datetime.now()
    used_time = (end_time-start_time).total_seconds()
    total = response['hits']['total']
    if (page % 10) > 0:
        page_nums = int(total/10) + 1
    else:
        page_nums = int(total/10)

    hit_list = list()
    for hit in response['hits']['hits']:
        hit_dict = dict()
        if "title" in hit["highlight"]:
            hit_dict["title"] = "".join(hit["highlight"]["title"])
        else:
            hit_dict["title"] = hit["_source"]["title"]
        if "content" in hit["highlight"]:
            hit_dict["content"] = "".join(hit["highlight"]["content"])[:500]
        else:
            hit_dict["content"] = hit["_source"]["html_content"][:500]

        # hit_dict["create_date"] = hit["_source"]["create_date"]
        hit_dict["url"] = hit["_source"]["url"]
        hit_dict["score"] = hit["_score"]
        hit_dict["content"] = re.sub(r'<[^>]+>', "", hit_dict["content"])
        hit_dict["content"] = re.sub(r'<.*', "", hit_dict["content"])
        hit_list.append(hit_dict)

    return render_template("search_result.html",
                           key_words=key_words,
                           used_time=used_time,
                           total=total,
                           page=page,
                           page_nums=page_nums,
                           hit_list=hit_list)
