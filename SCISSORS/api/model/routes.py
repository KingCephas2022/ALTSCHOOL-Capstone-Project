from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_share import share
from flask_mail import Message
from werkzeug.security import generate_password_hash, check_password_hash
import qrcode
import shortuuid
from random import randint
from .user import User, url
import io
from . import app, db, mail, cache

