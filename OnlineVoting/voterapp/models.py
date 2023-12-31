from django.db import models
# Create your models here.
class Candidate:
    candidate_id:int
    name:str
    rollnumber:str
    email:str
    password:str
    branch:str
    semester:str
    section:str
    position:str
    image:str
    mobile:int
    gender:str
    age:int
    address:str
    username:str
    password:str
    branch:str    
    address:str
    status:int

class Student:
    studentid:int
    name:str
    rollnumber:str
    email:str
    password:str
    branch:str
    semester:str
    section:str
    image:str
    mobile:int
    gender:str
    age:int
    address:str
    username:str
    password:str
    branch:str    
    address:str
    status:int
class Contact:
    id:int
    firstname:str
    lastname:str
    rollnumber:str
    email:str
    message:str

class Admin:
    admin_id:int
    name:str
    email:str
    password:str

class Election(models.Model):
    electionid:models.IntegerField()
    electionname:models.CharField(max_length=200)
    starttime:models.CharField(max_length=200)
    endtime:models.CharField(max_length=200)
    voters:models.CharField(max_length=200)
    date:models.DateField()
    status:models.IntegerField()

class Voting:
    id:int
    electionid:int
    studentid:int
    name:str
    rollnumber:str
    semester:str
    president:str
    vicepresident:str
    secretary:str
    treasurer:str

class Sem:
    semester:str
class Cand:
    cand_president:str
    cand_vicepresident:str
    cand_secretary:str
    cand_treasurer:str
class Emailid:
    mail:str

class Candidateresults:
    candidatename:str
    candidaterole:str
    noofvotes:int
