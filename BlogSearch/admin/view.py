import threading
import time

import redis
from flask import render_template, redirect, request, url_for, session
from redis import Redis
from scrapyd_api import ScrapydAPI

from .config import Account
from . import admin
from .login import logincheck


redis = Redis(host="10.10.10.1")
scrapyd = ScrapydAPI("http://127.0.0.1:6800")
# scrapyd_remote = ScrapydAPI("http://10.10.10.128:6800")


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        account = request.form.get('account')
        password = request.form.get('password')
        if account == Account.username and\
                        password == Account.password:
            session['login'] = 'login'
            return redirect(url_for('.admin_index'))
        else:
            return redirect(url_for('.login'))


@admin.route('/admin', methods=['GET', 'POST'])
@logincheck
def admin_index():
    projects = scrapyd.list_projects()
    master = []
    slave = []
    for project in projects:
        if "master" in project:
            name = project
            jobs = scrapyd.list_jobs(project)
            id = ''
            if jobs['running']:
                try:
                    id = jobs['running'][0]['id']
                    status = 'Running'
                except:
                    pass
            else:
                status = 'Not Running'
            master.append([name, id, status])
        else:
            name = project
            jobs = scrapyd.list_jobs(project)
            id = ''
            if jobs['running']:
                try:
                    id = jobs['running'][0]['id']
                    status = 'Running'
                except:
                    pass
            else:
                status = 'Not Running'
            slave.append([name, id, status])
    return render_template("admin.html", master=master, slave=slave)


@admin.route('/admin/<project>', methods=['GET', 'POST'])
@logincheck
def spider_detail(project):
    jobs = scrapyd.list_jobs(project)
    running = jobs['running']
    finished = jobs['finished']
    return render_template("spider_detail.html", running=running,
                           finished=finished, project=project)


@admin.route('/admin/master/<project>', methods=['GET', 'POST'])
@logincheck
def start_master(project):
    redis.lpush('freebuf:start_url', 'http://www.freebuf.com')
    id = scrapyd.schedule(project, 'freebuf_master_spider')
    return redirect(url_for(".spider_detail", project=project, id=id))


@admin.route('/admin/slave/<project>', methods=['GET', 'POST'])
@logincheck
def start_slave(project):
    def push_start():
        while True:
            print("pusher running now")
            time.sleep(2000)
            redis.lpush('freebuf_slave:start_url', "http://www.freebuf.com")
    t1 = threading.Thread(target=push_start)
    t1.start()
    id = scrapyd.schedule(project, 'freebuf_slave_spider')
    return redirect(url_for(".spider_detail", project=project))


@admin.route('/admin/cancel/<project>', methods=['GET', 'POST'])
@logincheck
def stop(project):
    jobs = scrapyd.list_jobs(project)
    for job in jobs['running']:
        scrapyd.cancel(project, job['id'])
    return redirect(url_for(".spider_detail", project=project))


@admin.route("/admin/show_jobs", methods=['GET', 'POST'])
@logincheck
def show_jobs():
    return redirect("http://127.0.0.1:6800/jobs")