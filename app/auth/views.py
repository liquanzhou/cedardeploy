#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
import ldap
from . import auth
from ..models import db, User
from ..config import *
from .forms import LoginForm


@auth.route('/', methods=['GET', 'POST'])
@auth.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        try:
            user = User.query.filter_by(username=username).first()

            if Ldap:
                my_ldap = ldap.initialize(LDAP_HOST)
                my_ldap.simple_bind_s("uid=%s,%s" %(username, LDAP_BASE), pwd)
                if user is None:
                    user = User(email='%s@xc.cn' %username, username=username,password=pwd)
                    db.session.add(user)
                    db.session.commit()
                    user = User.query.filter_by(username=username).first()
            else:
                if not user.check_password(pwd):
                    raise Exception("user passwd error")

            login_user(user, form.remember_me.data)
            session.permanent = True
            return redirect(request.args.get('next') or url_for('main.index'))

        except Exception as err:
            print(str(err))
    return render_template('login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # flash('You have been logged out.')
    return redirect(url_for('.login'))
