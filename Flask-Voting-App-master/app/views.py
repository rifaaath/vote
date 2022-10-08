from app import app
from .models import VotesModel,CandidateModel, UserModel,db
from flask import redirect, render_template, flash,url_for,request
from flask_login import login_required, current_user,logout_user
from flask_cors import cross_origin
import string
import json
import random

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/profile")
@login_required
def profile():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    bc = CandidateModel.query.filter_by(post="Branch-Captain").all()
    secretary = CandidateModel.query.filter_by(post="Secretary").all()
    treasurer = CandidateModel.query.filter_by(post="Treasurer").all()
    c_sec = CandidateModel.query.filter_by(post="Cultural-Secretary").all()
    s_sec = CandidateModel.query.filter_by(post="Sports-Secretary").all()
    t_sec = CandidateModel.query.filter_by(post="Techincal-Secretary").all()
    creative = CandidateModel.query.filter_by(post="Creative-Head").all()
    s_cord = CandidateModel.query.filter_by(post="SocialMedia-Coordinator").all()
    p_cord = CandidateModel.query.filter_by(post="Photography-Coordinator").all()
    graph = CandidateModel.query.filter_by(post="Graphic-Designer").all()
    website = CandidateModel.query.filter_by(post="Website-Manager").all()
    voter = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    return render_template("profile.html",name=current_user.name,prez=prez,vice=vice,bc=bc,secretary=secretary,treasurer=treasurer,c_sec=c_sec,t_sec=t_sec,s_sec=s_sec,creative=creative,s_cord=s_cord,p_cord=p_cord,graph=graph,website=website,voter=voter)
    
@app.route("/profile", methods=["POST"])
def post_vote():
    president = request.form.get('president')
    vicepresident = request.form.get('vice-president')
    bc = request.form.get('bc')
    secretary = request.form.get('secretary')
    treasurer = request.form.get('treasurer')
    c_sec = request.form.get('c_sec')
    s_sec = request.form.get('s_sec')
    t_sec = request.form.get('t_sec')
    creative = request.form.get('creative')
    s_cord = request.form.get('s_cord')
    p_cord = request.form.get('p_cord')
    graph = request.form.get('graph')
    website = request.form.get('website')
    

    voted = VotesModel.query.filter_by(roll_num=current_user.roll_num).first()
    if not voted:
        voter = VotesModel(roll_num=current_user.roll_num,voter_id=current_user.id,post_1=president,post_2=vicepresident,post_3=bc,post_4=secretary,post_5=treasurer,post_6=c_sec,post_7=s_sec,post_8=t_sec,post_9=creative,post_10=s_cord,post_11=p_cord,post_12=graph,post_13=website)
        print("\033[91m {} has voted \033[00m" .format(current_user.name))
        db.session.add(voter)
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('profile'))
    

@app.route("/candidate")
def candidate():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    bc = CandidateModel.query.filter_by(post="Branch-Captain").all()
    secretary = CandidateModel.query.filter_by(post="Secretary").all()
    treasurer = CandidateModel.query.filter_by(post="Treasurer").all()
    c_sec = CandidateModel.query.filter_by(post="Cultural-Secretary").all()
    s_sec = CandidateModel.query.filter_by(post="Sports-Secretary").all()
    t_sec = CandidateModel.query.filter_by(post="Techincal-Secretary").all()
    creative = CandidateModel.query.filter_by(post="Creative-Head").all()
    s_cord = CandidateModel.query.filter_by(post="SocialMedia-Coordinator").all()
    p_cord = CandidateModel.query.filter_by(post="Photography-Coordinator").all()
    graph = CandidateModel.query.filter_by(post="Graphic-Designer").all()
    website = CandidateModel.query.filter_by(post="Website-Manager").all()

    return render_template("candidate.html",prez=prez,vice=vice,bc=bc,secretary=secretary,treasurer=treasurer,c_sec=c_sec,t_sec=t_sec,s_sec=s_sec,creative=creative,s_cord=s_cord,p_cord=p_cord,graph=graph,website=website)

@app.route("/candidate_register")
@login_required
def candidate_register():
    if current_user.admin !=1:
        logout_user()
        flash('You do not have required authorization')
        return redirect(url_for('auth.login'))
    else:
        return render_template("candidate_register.html")

@app.route("/candidate_register", methods=["POST"])
def candidate_post():
    roll_num = request.form.get('roll_num')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    batch = request.form.get('batch')
    course = request.form.get('course')
    department = request.form.get('department')
    post = request.form.get('post')
    pic_path = request.form.get('pic_path')
    agenda = request.form.get('agenda')
    
    roll_no = UserModel.query.filter_by(roll_num =roll_num).first()
    cand = CandidateModel.query.filter_by(roll_num = roll_num).first()

    error = False
    print(roll_no)
    if not len(roll_no.roll_num) == 10:
        flash('USN is not valid.','error')
        error = True

    if cand:
        flash('Candidate has already been registered.','error')
        return redirect(url_for('candidate_register'))
    
    if not set(first_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True
    
    if not set(last_name).issubset(string.ascii_letters + " "):
        flash('Name can only contain alphabets.','error')
        error = True

    if not first_name and not last_name:
        flash('Name cannot be left blank.','error')
        error = True

    if not batch and not course and not department:
        flash('Please fill in all the details. Batch, Course and Department information is neccessary.','error')
        error = True
    
    if error:
        return redirect(url_for('candidate_register'))
    else:
        candidate = CandidateModel(roll_num=roll_num, first_name=first_name,last_name=last_name,batch=batch,course=course,department=department,post=post,pic_path=pic_path,agenda=agenda)
        db.session.add(candidate)
        db.session.commit()
        flash('Candidate successfully registered.','success')
        return redirect(url_for('candidate_register'))

@app.route("/live_result")
def live_result():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    bc = CandidateModel.query.filter_by(post="Branch-Captain").all()
    secretary = CandidateModel.query.filter_by(post="Secretary").all()
    treasurer = CandidateModel.query.filter_by(post="Treasurer").all()
    c_sec = CandidateModel.query.filter_by(post="Cultural-Secretary").all()
    s_sec = CandidateModel.query.filter_by(post="Sports-Secretary").all()
    t_sec = CandidateModel.query.filter_by(post="Techincal-Secretary").all()
    creative = CandidateModel.query.filter_by(post="Creative-Head").all()
    s_cord = CandidateModel.query.filter_by(post="SocialMedia-Coordinator").all()
    p_cord = CandidateModel.query.filter_by(post="Photography-Coordinator").all()
    graph = CandidateModel.query.filter_by(post="Graphic-Designer").all()
    website = CandidateModel.query.filter_by(post="Website-Manager").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    labels2=[]
    data2=[]
    labels3=[]
    data3=[]
    labels4=[]
    data4=[]
    labels5=[]
    data5=[]
    labels6=[]
    data6=[]
    labels7=[]
    data7=[]
    labels8=[]
    data8=[]
    labels9=[]
    data9=[]
    labels10=[]
    data10=[]
    labels11=[]
    data11=[]
    labels12=[]
    data12=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.roll_num).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.roll_num).count()
        data1.append(vote)
    for candidate in bc:
        name = candidate.first_name+" "+candidate.last_name
        labels2.append(name)
        vote=VotesModel.query.filter(VotesModel.post_3==candidate.roll_num).count()
        data2.append(vote)
    for candidate in secretary:
        name = candidate.first_name+" "+candidate.last_name
        labels3.append(name)
        vote=VotesModel.query.filter(VotesModel.post_4==candidate.roll_num).count()
        data3.append(vote)
    for candidate in treasurer:
        name = candidate.first_name+" "+candidate.last_name
        labels4.append(name)
        vote=VotesModel.query.filter(VotesModel.post_5==candidate.roll_num).count()
        data4.append(vote)
    for candidate in c_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels5.append(name)
        vote=VotesModel.query.filter(VotesModel.post_6==candidate.roll_num).count()
        data5.append(vote)
    for candidate in s_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels6.append(name)
        vote=VotesModel.query.filter(VotesModel.post_7==candidate.roll_num).count()
        data6.append(vote)
    for candidate in t_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels7.append(name)
        vote=VotesModel.query.filter(VotesModel.post_8==candidate.roll_num).count()
        data7.append(vote)
    for candidate in creative:
        name = candidate.first_name+" "+candidate.last_name
        labels8.append(name)
        vote=VotesModel.query.filter(VotesModel.post_9==candidate.roll_num).count()
        data8.append(vote)
    for candidate in s_cord:
        name = candidate.first_name+" "+candidate.last_name
        labels9.append(name)
        vote=VotesModel.query.filter(VotesModel.post_10==candidate.roll_num).count()
        data9.append(vote)
    for candidate in p_cord:
        name = candidate.first_name+" "+candidate.last_name
        labels10.append(name)
        vote=VotesModel.query.filter(VotesModel.post_11==candidate.roll_num).count()
        data10.append(vote)
    for candidate in graph:
        name = candidate.first_name+" "+candidate.last_name
        labels11.append(name)
        vote=VotesModel.query.filter(VotesModel.post_12==candidate.roll_num).count()
        data11.append(vote)
    for candidate in website:
        name = candidate.first_name+" "+candidate.last_name
        labels12.append(name)
        vote=VotesModel.query.filter(VotesModel.post_13==candidate.roll_num).count()
        data12.append(vote)
 
    return render_template('graph.html',labels=labels,data=data,labels1=labels1,data1=data1,labels2=labels2,data2=data2,labels3=labels3,data3=data3,labels4=labels4,data4=data4,labels5=labels5,data5=data5,labels6=labels6,data6=data6,labels7=labels7,data7=data7,labels8=labels8,data8=data8,labels9=labels9,data9=data9,labels10=labels10,data10=data10,labels11=labels11,data11=data11,labels12=labels12,data12=data12)


@app.route("/vote/count")
@cross_origin()
def voteCount():
    prez = CandidateModel.query.filter_by(post="President").all()
    vice = CandidateModel.query.filter_by(post="Vice-President").all()
    bc = CandidateModel.query.filter_by(post="Branch-Captain").all()
    secretary = CandidateModel.query.filter_by(post="Secretary").all()
    treasurer = CandidateModel.query.filter_by(post="Treasurer").all()
    c_sec = CandidateModel.query.filter_by(post="Cultural-Secretary").all()
    s_sec = CandidateModel.query.filter_by(post="Sports-Secretary").all()
    t_sec = CandidateModel.query.filter_by(post="Techincal-Secretary").all()
    creative = CandidateModel.query.filter_by(post="Creative-Head").all()
    s_cord = CandidateModel.query.filter_by(post="SocialMedia-Coordinator").all()
    p_cord = CandidateModel.query.filter_by(post="Photography-Coordinator").all()
    graph = CandidateModel.query.filter_by(post="Graphic-Designer").all()
    website = CandidateModel.query.filter_by(post="Website-Manager").all()
    labels=[]
    data=[]
    labels1=[]
    data1=[]
    labels2=[]
    data2=[]
    labels3=[]
    data3=[]
    labels4=[]
    data4=[]
    labels5=[]
    data5=[]
    labels6=[]
    data6=[]
    labels7=[]
    data7=[]
    labels8=[]
    data8=[]
    labels9=[]
    data9=[]
    labels10=[]
    data10=[]
    labels11=[]
    data11=[]
    labels12=[]
    data12=[]
    for candidate in prez:
        name = candidate.first_name+" "+candidate.last_name
        labels.append(name)
        vote=VotesModel.query.filter(VotesModel.post_1==candidate.roll_num).count()
        data.append(vote)
    for candidate in vice:
        name = candidate.first_name+" "+candidate.last_name
        labels1.append(name)
        vote=VotesModel.query.filter(VotesModel.post_2==candidate.roll_num).count()
        data1.append(vote)
    for candidate in bc:
        name = candidate.first_name+" "+candidate.last_name
        labels2.append(name)
        vote=VotesModel.query.filter(VotesModel.post_3==candidate.roll_num).count()
        data2.append(vote)
    for candidate in secretary:
        name = candidate.first_name+" "+candidate.last_name
        labels3.append(name)
        vote=VotesModel.query.filter(VotesModel.post_4==candidate.roll_num).count()
        data3.append(vote)
    for candidate in treasurer:
        name = candidate.first_name+" "+candidate.last_name
        labels4.append(name)
        vote=VotesModel.query.filter(VotesModel.post_5==candidate.roll_num).count()
        data4.append(vote)
    for candidate in c_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels5.append(name)
        vote=VotesModel.query.filter(VotesModel.post_6==candidate.roll_num).count()
        data5.append(vote)
    for candidate in s_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels6.append(name)
        vote=VotesModel.query.filter(VotesModel.post_7==candidate.roll_num).count()
        data6.append(vote)
    for candidate in t_sec:
        name = candidate.first_name+" "+candidate.last_name
        labels7.append(name)
        vote=VotesModel.query.filter(VotesModel.post_8==candidate.roll_num).count()
        data7.append(vote)
    for candidate in creative:
        name = candidate.first_name+" "+candidate.last_name
        labels8.append(name)
        vote=VotesModel.query.filter(VotesModel.post_9==candidate.roll_num).count()
        data8.append(vote)
    for candidate in s_cord:
        name = candidate.first_name+" "+candidate.last_name
        labels9.append(name)
        vote=VotesModel.query.filter(VotesModel.post_10==candidate.roll_num).count()
        data9.append(vote)
    for candidate in p_cord:
        name = candidate.first_name+" "+candidate.last_name
        labels10.append(name)
        vote=VotesModel.query.filter(VotesModel.post_11==candidate.roll_num).count()
        data10.append(vote)
    for candidate in graph:
        name = candidate.first_name+" "+candidate.last_name
        labels11.append(name)
        vote=VotesModel.query.filter(VotesModel.post_12==candidate.roll_num).count()
        data11.append(vote)
    for candidate in website:
        name = candidate.first_name+" "+candidate.last_name
        labels12.append(name)
        vote=VotesModel.query.filter(VotesModel.post_13==candidate.roll_num).count()
        data12.append(vote)
    

    output = {"data": data,
            "labels": labels,
            "data1": data1,
            "labels1": labels1,
            "data2": data2,
            "labels2": labels2,
            "data3": data3,
            "labels3": labels3,
            "data4": data4,
            "labels4": labels4,
            "data5": data5,
            "labels5": labels5,
            "data6": data6,
            "labels6": labels6,
            "data7": data7,
            "labels7": labels7,
            "data8": data8,
            "labels8": labels8,
            "data9": data9,
            "labels9": labels9,
            "data10": data10,
            "labels10": labels10,
            "data11": data11,
            "labels11": labels11,
            "data12": data12,
            "labels12": labels12,
            }
    response = app.response_class(
        response=json.dumps(output),
        status=200,
        mimetype='application/json'
    )
    return response
