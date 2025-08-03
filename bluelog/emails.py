import os

from flask import url_for
from flask_mail import Message
from app import mail
from flask import current_app

"""
发送邮件有两个场景，一个是作者收到文章有新评论，一个是提醒用户（作者和读者）评论有了新回复
1.实现正常发送邮件的功能
2.在正常发送的邮件正文中显示是那个文章被评论，并且点击邮箱中的链接，可以直接查看文章添加的评论
3.在收到评论被回复的提醒，邮件正文中显示那个文章中的那个评论被回复了，也可以点击链接直接查看回复的评论内容
"""

def send_email(subject,to,html):
    msg = Message(subject,recipients=[to], html=html)
    mail.send(msg)

# 提醒文章被评论
def send_new_comments(post):
    post_url = url_for('blog.show_post', post_id=post.id, _external=True) +'#comments'
    send_email(subject='New Comment', to=current_app.config['MAIL_USERNAME'],
               html='<p>You have new comments of post:<i>%s</i></p>'
                    '<p>please click the link <a href=%s>%s</a></p>'
                    '<p><small style="color:#868e96" >Do not reply this email</small></p>'
                    %(post.title, post_url, post_url)
               )

# 提醒留言的评论被回复
def send_comments_reply(comment):
    post_url = url_for('blog.show_post', post_id=comment.post_id, _external=True)+ '#comments'
    send_email(subject='New reply', to=comment.email,
               html='<p>You have a new reply you left in the post:<i>%s</i></p>'
                    '<p>please click the link to check:<a href="%s">%s</a></p>'
                    %(comment.post.title,post_url,post_url)
               )

