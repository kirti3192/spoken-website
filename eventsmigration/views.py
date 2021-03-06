from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import render
from django.db import connection
from django.conf import settings
from shutil import copyfile
import random, string
import datetime
#from datetime import date, datetime, time, timedelta
import os, sys

from workshop.models import *
from events.models import *
from cms.models import *
from django.db.models import Sum
from cdeep.models import *

def update_old_city(request):
    newac = AcademicCenter.objects.filter(city = City.objects.filter(name="Uncategorized"))
    for nac in newac:
        oldac = WAcademicCenter.objects.get(academic_code=nac.academic_code)
        #find in new City
        city = City.objects.filter(name=oldac.city)
        if city and city.first():
            city = city.first()
            nac.city = city
            nac.save()
            print nac.institution_name, " => ", city.name, " Saved!" 
    return HttpResponse("Done")
    
def get_dept(dept):
    getDept = {
        ###
        'CSE' : 'Computer Science and Engineering',
        'cse' : 'Computer Science and Engineering',
        'cse ' : 'Computer Science and Engineering',
        'Dept. of Computer Science and Engineering' : 'Computer Science and Engineering',
        'Computer Science & Engineering' : 'Computer Science and Engineering',
        'DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING' : 'Computer Science and Engineering',
        'Computer Science Engineering' : 'Computer Science and Engineering',
        'Computer Science Engineering ' : 'Computer Science and Engineering',
        'Computer Science Engg.' : 'Computer Science and Engineering',
        'DEPARTMENT OF COMPUTER ENGINEERING' : 'Computer Science and Engineering',
        'Department of Computer Engineering' : 'Computer Science and Engineering',
        'Computer Engineering ' : 'Computer Science and Engineering',
        'Computer Engineering' : 'Computer Science and Engineering',
        'computer engineering' : 'Computer Science and Engineering',
        'COMPUTER ENGINEERING' : 'Computer Science and Engineering',
        'Computer engineering' : 'Computer Science and Engineering',
        'Department of Computer Science' : 'Computer Science and Engineering',
        'Department of Computer Science and Engineering' : 'Computer Science and Engineering',
        'Computer Sc and Engg' : 'Computer Science and Engineering',
        'Computer science and engineering department' : 'Computer Science and Engineering',
        'COMPUTER SCIENCE AND ENGINEERING DEPARTMENT' : 'Computer Science and Engineering',
        'CSE Department' : 'Computer Science and Engineering',
        'COMPUTER ENGG' : 'Computer Science and Engineering',
        'COMPUTER SCIENCE & ENGINEERING' : 'Computer Science and Engineering',
        'department of computer science' : 'Computer Science and Engineering',
        'COMPUTER SCIENCE & ENGINEERING ' : 'Computer Science and Engineering',
        'computer science & engineering' : 'Computer Science and Engineering',
        'Computer Science and Enggineering' : 'Computer Science and Engineering',
        
        ###
        'CST' : 'Computer Science and Technology',
        'Department of Computer Science and Technology' : 'Computer Science and Technology',
        
        ###
        'Information Tehnology' : 'Information Technology',
        'COMPUTER INFORMATION TECHNOLOGY' : 'Information Technology',
        'Department of Technology' : 'Information Technology',
        'IT' : 'Information Technology',
        'Department of IT' : 'Information Technology',
        'Department of Information Technology' : 'Information Technology',
        'computers and information technology' : 'Information Technology',
        'INFORMATION TECH' : 'Information Technology',
        
        ###
        'Department of Computer Application' : 'Computer Applications',
        'Department of Computer Applications' : 'Computer Applications',
        'Computer Applications' : 'Computer Applications',
        'BCA' : 'Computer Applications',
        'BCA-III Students' : 'Computer Applications',
        'Master of Computer' : 'Computer Applications',
        'BCA' : 'Computer Applications',
        'MCA' : 'Computer Applications',
        'Computer Application' : 'Computer Applications',
        'Master of Computer Application' : 'Computer Applications',
        
        ###
        'Computer' : 'Computer Science',
        'computers' : 'Computer Science',
        'Computer GU' : 'Computer Science',
        'cs' : 'Computer Science',
        'CS' : 'Computer Science',
        'School of Computer Science' : 'Computer Science',
        'School Of Computer Science' : 'Computer Science',
        'ComputerScience' : 'Computer Science',
        'computer Science Dept' : 'Computer Science',
        'Computer Scince' : 'Computer Science',
        'COMPUTERS' : 'Computer Science',
        'School of computer science' : 'Computer Science',
        'SCHOOL OF COMPUTER SCIENCE' : 'Computer Science',
        'Comuter Science' : 'Computer Science',
        
        
        ###
        'ELECTRONICS AND COMMUNICATION ENGINEERING DEPARTME' : 'Electronics and Communication Engineering',
        'Dept. of Electronics and Communication Engineering' : 'Electronics and Communication Engineering',
        'ECE' : 'Electronics and Communication Engineering',
        'Electrical and Communication Engineering' : 'Electronics and Communication Engineering',
        'EC' : 'Electronics and Communication Engineering',
        'ELECTRONICS AND COMMUNICATION' : 'Electronics and Communication Engineering',
        'EC Department' : 'Electronics and Communication Engineering',
        'EXTC' : 'Electronics and Communication Engineering',
        'EECE' : 'Electronics and Communication Engineering',
        'Electronics and Communication' : 'Electronics and Communication Engineering',
        'ece' : 'Electronics and Communication Engineering',
        
        ###
        'EEE' : 'Electrical and Electronics Engineering',
        'Department of Electrical and Electronics Engineeri' : 'Electrical and Electronics Engineering',
        'electrical and electronics' : 'Electrical and Electronics Engineering',
        'ELECTRONICCS' : 'Electrical and Electronics Engineering',
        'electronics' : 'Electrical and Electronics Engineering',
        'Electronics' : 'Electrical and Electronics Engineering',
        
        ###
        'ETC' : 'Electronics and Telecommunication',
        
        ###
        #'Electrical Engineering'
        
        ###
        'INSTRUMENTATION AND CONTROL' : 'Electronics and instrumentation Engineering',
        'INSTRUMENTATION ENGINEERING' : 'Electronics and instrumentation Engineering',
        'ICE' : 'Electronics and instrumentation Engineering',
        
        ###
        'ME' : 'Mechanical Engineering',
        ' PRODUCTION ENGINEERING' : 'Mechanical Engineering',
        'Mechanical' : 'Mechanical Engineering',
        'MECHANICAL' : 'Mechanical Engineering',
        
        ###
        'Civil' : 'Civil Engineering',
        'CIVIL' : 'Civil Engineering',
        'CE' : 'Civil Engineering',
        
        ###
        'AERONAUTICAL' : 'Aeronautical Engineering',
        
        ###
        'E&TC' : 'Electronics and Telecommunication',
        'Electronics & Telecomunication' : 'Electronics and Telecommunication',
        'E&TC ENGINEERING' : 'Electronics and Telecommunication',
        
        ###
        'EE' : 'Electronics Engineering',
        'Department of Electronics' : 'Electronics Engineering',
        'ELECTRONIC ' : 'Electronics Engineering',
        
        ###
        'FDP' : 'Faculty Development Program',
        'All(Faculity Members, FDP)' : 'Faculty Development Program',
        'Central Library KKHSOU' : 'Faculty Development Program',
        'Central Library' : 'Faculty Development Program',
        'Faculty' : 'Faculty Development Program',
        'Library' : 'Faculty Development Program',
        'THE FUTURE COMPUTER SCIENCE COLLEGE' : 'Faculty Development Program',
        'Sowdambika Polytechnic College ' : 'Faculty Development Program',
        'Future Computer Science College' : 'Faculty Development Program',
        'Kamani Science College' : 'Faculty Development Program',
        'P S HIRPARA MAHILA COLLEGE' : 'Faculty Development Program',
        'MCA staff and faculty' : 'Faculty Development Program',
        'Administrative' : 'Faculty Development Program',
        'Telecommunication and Engineering ' : 'Telecommunication Engineering',
        'GYANBHARTI COMPUTER SCIENCE COLLEGE' : 'Faculty Development Program',
        'G K C K BOSAMIYA COLLEGE' : 'Faculty Development Program',
        'VARMORA COLLEGE' : 'Faculty Development Program',
        'GAJERA SANKUL' : 'Faculty Development Program',
        'Morigaon College' : 'Faculty Development Program',
        
        ###
        #Chemical Engineering
        
        ###
        'MATHEMATICS' : 'Applied Mathematics',
        'DEPARTMENT OF MATHEMATICS' : 'Applied Mathematics',
        'Mathematics' : 'Applied Mathematics',
        
        ###
        'BTECH' : 'Batchelor of Tehchnology',
        'Btech' : 'Batchelor of Tehchnology',
        ###
        'Department of Physics' : 'Physics',
        'Physics' : 'Physics',
        'Department of Physics,  Sri Sathya Sai Institute o' : 'Physics',
        
        ###
        'Information Science' : 'Information Science',
        
        ###
        'ECE, IT, CSE, EEE, MCA' : 'ECE,IT,CSE,EEE,MCA',
        'CSE & IT' : 'CSE,IT',
        'E&TC and CS' : 'ECE,CS',
        'CSE MCA' : 'CSE,MCA',
        'CSEIT' : 'CSE,IT',
        'ECE CIVIL CSE' : 'ECE,CIVIL,CSE',
        'CSE IT ' : 'CSE,IT',
        'CSE IT MCA' : 'CSE,IT,MCA',
        'EEE ECE' : 'EEE,ECE',
        'EEE ECE' : 'EEE,ECE',
        'ECE CSE CIVIL IT' : 'ECE,CSE,CIVIL,IT',
        'CSE IT' : 'CSE,IT',
        'CSE ECE CIVIL' : 'CSE,ECE,CIVIL',
        'ECE EEE ICE CSE ' : 'ECE,EEE,ICE,CSE',
        'Computer Science / Information Technology' : 'CS,IT',
        'MAC BTECH' : 'MCA,BTECH',
        'Civil Mech' : 'Civil,Mechanical',
        'Civil Mechanical' : 'Civil,Mechanical',
        'Computer and IT Department' : 'CS,IT',
        'Information Technology and Computer science and en' : 'IT,CSE',
        'IT and Computer Science' : 'IT,CS',
        'School of Elect. Engg and IT': 'EE,IT',
        'BCA B.Com B.SC' : 'BCA,Commerce and Management,CS',
        'School of Chemical and Biotechnology' : 'Chemical Engineering,Biotechnology',
        'Computational Biology and Bioinformatics' : 'Biology,Bioinformatics',
        
        ### Uncategorized
        '50' : 'Others',
        'Common to all Branches - 1st semester' : 'Others',
        'Linux' : 'Others',
        'BSH' : 'Others',
        'KTurtle Pilot Workshop for class VII students' : 'Others',
        'COPA' : 'Others',
        'TechFest-2013 participants' : 'Others',
        'CSI-IT2020 Participants' : 'Others',
        'Open to All' : 'Others',
        'ALL' : 'Others',
        'Others' : 'Others',
        'others' : 'Others',
        'Oceanography' : 'Oceanography',
        '' : 'Others',
    }
    #print "**********************"
    #print dept
    #print getDept[dept]
    #print "**********************"
    return getDept[dept]
    
def department(request):
    wd = WDepartments.objects.all().values_list('name')
    wwrd = WWorkshopRequests.objects.exclude(department__in = wd).values_list('department').distinct()
    #print list(wwrd)
    newDept = ['Batchelor of Tehchnology', 'Others', 'Electronics Engineering', 'Faculty Development Program', 'Physics', 'Oceanography', 'Information Science', 'Computer Applications', 'Computer Science and Technology', 'Biotechnology', 'Bioinformatics', 'Biology', 'Computer Science and Engineering', 'Information Technology', 'Information Science', 'Batchelor of Tehchnology', 'Computer Science and Engineering', 'Computer Science and Technology', 'Computer Applications', 'Computer Science', 'Electronics and Communication Engineering', 'Electrical and Electronics Engineering', 'Electronics and Telecommunication', 'Electronics and instrumentation Engineering', 'Mechanical Engineering', 'Civil Engineering', 'Aeronautical Engineering', 'Electronics and Telecommunication', 'Electronics Engineering', 'Faculty Development Program', 'Applied Mathematics', 'Batchelor of Tehchnology']
    for dept in newDept:
        try:
            Department.objects.get(name = dept)
        except Exception, e:
            Department.objects.create(name = dept)
            print e
    
    return HttpResponse("Department migration complted!")

def states(request):
    wstate = WStates.objects.all()
    for ws in wstate:
        try:
            s = State.objects.get(name=ws.name)
            s.code = ws.code.upper()
            s.latitude = ws.latitude
            s.longitude = ws.longitude
            s.image_map_area = ws.image_map_area
            s.save()
        except Exception, e:
            print e
            State.objects.create(code = ws.code, name = ws.name)
            print "created => ", ws.name
    return HttpResponse("States migration complted!")

def testimonials(request):
    anodes = Node.objects.filter(type = 'credentials')
    for nodeid in anodes:
        node = NodeRevisions.objects.get(nid = nodeid.nid)
        r = ContentTypeCredentials.objects.get(nid = nodeid.nid)
        try:
            Testimonials.objects.get(user_name = r.field_credentials_source_value)
        except Exception, e:
            pass
        
        try:
            t = Testimonials()
            t.user_id = 1
            t.user_name = r.field_credentials_source_value
            t.actual_content = node.body
            t.minified_content = r.field_short_description_value
            t.short_description = r.field_short_description_value
            t.source_title = r.field_credentials_source_link_title
            t.source_link = r.field_credentials_source_link_url
            t.status = 1
            t.save()
        except Exception, e:
            print e
    return HttpResponse("testimonials migration complted!")

def articles(request):
    from django.template.defaultfilters import slugify
    import shutil
    dtypes = ['article', 'media_reports', 'news_and_events', 'official_letters_or_links']
    newstype = {'article' : 1, 'media_reports' : 2, 'news_and_events' :3, 'official_letters_or_links' : 4}
    for dt in dtypes:
        anodes = Node.objects.filter(type = dt)
        for nodeid in anodes:
            node = NodeRevisions.objects.get(nid = nodeid.nid)
            
            try:
                nodefile = None
                if dt == 'article':
                    nodeextra = ContentTypeArticle.objects.get(nid = nodeid.nid)
                    nodefile = Files.objects.get(fid  = nodeextra.field_photo_fid)
                elif dt == 'media_reports':
                    nodeextra = ContentTypeMediaReports.objects.get(nid = nodeid.nid)
                    nodefile = Files.objects.get(fid  = nodeextra.field_media_report_image_fid)
                elif dt == 'news_and_events':
                    nodeextra = ContentTypeNewsAndEvents.objects.get(nid = nodeid.nid)
                    nodefile = Files.objects.get(fid  = nodeextra.field_event_image_fid)
                elif dt == 'official_letters_or_links':
                    nodeextra = ContentTypeOfficialLettersOrLinks.objects.get(nid = nodeid.nid)
                    nodefile = Files.objects.get(fid  = nodeextra.field_official_litter_fid)
            except:
                pass
                
            #print node
            #print nodeextra
            #print nodefile
            
            try:
                News.objects.get(title = node.title)
                #print "Already exits!"
                continue
            except:
                pass
            
            #return HttpResponse("Articles migration complted!")
            try:
                n = News()
                n.news_type_id = newstype[dt]
                n.title = node.title
                n.body = node.body
                n.slug = slugify(node.title)
                
                nodelink = None
                nodeltile = None
                if dt == 'article':
                    nodelink = nodeextra.field_link_url
                    nodeltile = nodeextra.field_link_title
                elif dt == 'media_reports':
                    nodelink = nodeextra.field_media_report_link_url
                    nodeltile = nodeextra.field_media_report_link_title 
                elif dt == 'news_and_events':
                    nodelink = nodeextra.field_event_link_url
                    nodeltile = nodeextra.field_event_link_title
                elif dt == 'official_letters_or_links':
                    nodelink = nodeextra.field_official_link_url
                    nodeltile = nodeextra.field_official_link_title
                
                n.url = nodelink
                n.url_title = nodeltile
                duser = get_user(node.uid)
                n.created_by_id = duser.id
                
                if nodeid.created:
                    n.created = datetime.datetime.fromtimestamp(int(nodeid.created)).strftime('%Y-%m-%d %H:%M:%S')
                    n.updated = datetime.datetime.fromtimestamp(int(nodeid.changed)).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    n.created = datetime.datetime.now()
                    n.updated = datetime.datetime.now()
                
                n.save()
                if nodefile:
                    srcfile = settings.PROFILE_PATH + nodefile.filepath
                    file_ext = nodefile.filename.split('.')[1]
                    dstdir = settings.MEDIA_ROOT + 'news/' + str(n.id) + '/'
                    
                    try:
                        os.makedirs(dstdir)
                    except:
                        pass
                        
                    copyfile(srcfile, dstdir + str(n.id) + '.' + file_ext)
                    n.picture = 'news/' + str(n.id) + '/' + str(n.id) + '.' + file_ext
                    n.save()
                    
            except Exception, e:
                print e, "+++++++++", node.nid, node.title, "++++++++++++"
        
    return HttpResponse("Articles migration complted!")
    
def resource_person(request):
    wrps = WResourcePerson.objects.all()
    for wrp in wrps:
        try:
            duser = get_user(wrp.user_uid)
            duser.groups.add(Group.objects.get(name='Resource Person'))
        except:
            continue
        wstates = wrp.states.split(',')
        for wstate in wstates:
            try:
                state = State.objects.get(code = wstate)
                print "******", wstate, "******"
                ResourcePerson.objects.get_or_create(state=state, user=duser, assigned_by = 1, status = 1)
            except Exception, e:
                print e, "ResourcePerson => ", duser, wrp.user_uid
    return HttpResponse("Rp migration complted!")

def academic_center(request):
    state_list = {'' : 36L, 'ANP' : 2L, 'ANR' : 1L, 'ARP' : 3L, 'ASM' : 4L, 'BHR' : 5L, 'CHG' : 6L, 'CTG' : 7L, 'DDU' : 9L, 'DEL' : 10L, 'DNG' : 8L, 'GOA' : 11L, 'GUJ' : 12L, 'HAR' : 13L, 'HMP' : 14L, 'INL' : 37L, 'JHD' : 16L, 'JNK' : 15L, 'KAR' : 17L, 'KER' : 18L, 'LKD' : 19L, 'MAH' : 21L, 'MAN' : 22L, 'MDP' : 20L, 'MEG' : 23L, 'MIZ' : 24L, 'NAG' : 25L, 'ODI' : 26L, 'PCY' : 27L, 'PJB' : 28L, 'RAJ' : 29L, 'SIK' : 30L, 'TAM' : 31L, 'TRP' : 32L, 'UTK' : 34L, 'UTP' : 33L, 'WBN' : 35L}
    wacs = WAcademicCenter.objects.all()
    for wac in wacs:
        try:
            ac = AcademicCenter.objects.get(academic_code = wac.academic_code)
            #print "Already exits => ", wac.academic_code
        except Exception, e:
            #print e,
            #print " Not exits =>", wac.academic_code
            try:
                #print "Create new Academic Center .."
                it = InstituteType.objects.get(name="Uncategorized")
                ic = InstituteCategory.objects.get(name="Uncategorized")
                u = University.objects.get(name="Uncategorized")
                d = District.objects.get(name="Uncategorized")
                c = City.objects.get(name="Uncategorized")
                
                ac = AcademicCenter()
                ac.user_id = 1
                ac.state_id = state_list[str(wac.state_code)]
                ac.academic_code = wac.academic_code.upper()
                ac.school_college = wac.school_college
                ac.institution_name = wac.institution_name.strip()
                ac.address = wac.street
                ac.resource_center = wac.resource_center
                ac.rating = wac.star_rating
                ac.contact_person = wac.contact_details
                ac.remarks = wac.remarks
                
                ac.institution_type_id = it.id
                ac.institute_category_id = ic.id
                ac.university_id = u.id
                ac.district_id = d.id
                ac.city_id = c.id
                ac.status = 1
                
                if wac.pincode:
                    ac.pincode = wac.pincode
                else:
                    ac.pincode = 0
                
                if wac.created_at:
                    ac.created = wac.created_at
                    ac.updated = wac.updated_at
                else:
                    ac.created = datetime.datetime.now()
                    ac.updated = datetime.datetime.now()
                    
                ac.save()
            except Exception, e:
                print "********************"
                print e
                print "Failed while creating ...", wac.academic_code
                print "********************"
                
    return HttpResponse("AcademicCenter migration complted!")

def organiser(request):
    worganisers = WOrganiser.objects.all()
    for wo in worganisers:
        duser = get_user(wo.organiser_id)
        if duser == None:
            print 'id:', wo.id, 'user missing in auth_user'
            continue
        try:
            o = Organiser.objects.get(user_id  = duser.id)
            #print "Organiser Already Exits!", "Django user id => ", duser.id, "Drupal id => ", wo.organiser_id
            continue
        except Exception, e:
            #print e
            #print "*********** => 1"
            try:
                #find academic_id
                if 'ANR' in wo.academic_code:
                    continue
                
                try:
                    ac = AcademicCenter.objects.get(academic_code = wo.academic_code)
                except Exception, e:
                    #print e
                    #print "******* Getting workshop academic code *********"
                    wwr = WWorkshopRequests.objects.filter(organiser_id = wo.organiser_id).first()
                    #if not wwr:
                    #    print "******* workshop academic code not there ******", wo.organiser_id
                    #    #continue
                    if not wwr:
                        print 'id:', wo.id, 'Academic Code Missing'
                        continue
                    try:
                        ac = AcademicCenter.objects.get(academic_code = wwr.academic_code)
                    except:
                        print 'id:', wo.id, 'Academic Code Missing'
                        continue
                #profile
                try:
                    p = Profile.objects.get(user_id = duser.id)
                    p.address = wo.address
                    p.phone = wo.phone
                    p.save()
                except Exception, e:
                    print 'id:', wo.id, 'error adding profile info'
                #save organiser name ad user first name
                try:
                    u = User.objects.get(pk = duser.id)
                    u.first_name = wo.organiser_name
                    u.save()
                    try:
                        u.groups.get(name='Organiser')
                    except Exception, e:
                        try:
                            u.groups.add(Group.objects.get(name='Organiser'))
                        except:
                            print 'id:', wo.id, 'error while Orgainser group'
                except Exception, e:
                    print e
                    #print "*********** => 3", "Django user id => ", duser.id, "Drupal id => ", wo.organiser_id
                    #print "User not exits => ", wo.organiser_id
                try:
                    o = Organiser()
                    o.user_id  = duser.id
                    o.academic_id = ac.id
                    o.status = wo.status
                    if wo.created_at:
                        o.created = wo.created_at
                        o.updated = wo.updated_at
                    else:
                        o.created = datetime.datetime.now()
                        o.updated = datetime.datetime.now()
                    
                    o.save()
                except Exception, e:
                    print e
                    #print "******** 4 "
                    
            except Exception, e:
                print e
                print "*********** => 5 => ", "Django user id => ", duser.id, "Drupal id => ", wo.organiser_id
                #print "Something went wrong"
                
    return HttpResponse("Organiser migration Done!")

def invigilator(request):
    winvigilators = WInvigilator.objects.all()
    for wo in winvigilators:
        duser = get_user(wo.invigilator_id)
        if duser == None:
            print 'id:', wo.id, 'user missing in auth_user'
            continue
        try:
            o = Invigilator.objects.get(user_id  = duser.id)
            continue
        except Exception, e:
            #print e
            #print "*********** => 1"
            try:
                #find academic_id
                if 'ANR' in wo.academic_code:
                    continue
                try:
                    ac = AcademicCenter.objects.get(academic_code = wo.academic_code)
                except Exception, e:
                    print e
                    print "******* Getting workshop academic code *********"
                    wwr = WTestRequests.objects.filter(invigilator_id = wo.invigilator_id).first()
                    if not wwr:
                        print "******* workshop academic code not there ******", wo.invigilator_id
                        continue
                    try:
                        ac = AcademicCenter.objects.get(academic_code = wwr.academic_code)
                    except:
                        print 'id:', wo.id, 'Academic Code Missing'
                        continue
                        
                #profile
                try:
                    p = Profile.objects.get(user_id = duser.id)
                    p.address = wo.address
                    p.phone = wo.phone
                    p.save()
                except Exception, e:
                    print 'id:', wo.id, 'error adding profile info'
                #save invigilator name ad user first name
                try:
                    u = User.objects.get(pk = duser.id)
                    u.first_name = wo.invigilator_name
                    u.save()
                    try:
                        u.groups.get(name='Invigilator')
                    except Exception, e:
                        try:
                            u.groups.add(Group.objects.get(name='Invigilator'))
                        except:
                            print 'id:', wo.id, 'error while Invigilator group'
                except Exception, e:
                    print e
                    #print "*********** => 3", "Django user id => ", duser.id, "Drupal id => ", wo.invigilator_id
                    #print "User not exits => ", wo.invigilator_id
                try:
                    o = Invigilator()
                    o.user_id  = duser.id
                    o.academic_id = ac.id
                    o.status = wo.status
                    if wo.created_at:
                        o.created = wo.created_at
                        o.updated = wo.updated_at
                    else:
                        o.created = datetime.datetime.now()
                        o.updated = datetime.datetime.now()
                    
                    o.save()
                except Exception, e:
                    print e
                    #print "******** 4 "
                    
            except Exception, e:
                print e
                print "*********** => 5 => ", "Django user id => ", duser.id, "Drupal id => ", wo.invigilator_id
                print "Something went wrong"
                
    return HttpResponse("Invigilator migration Done!")

#MAH-00029 Live workshop
def workshop(request):
    workshop_status = 0
    if workshop_status == 2:
        wwrs = WWorkshopRequests.objects.filter(status = workshop_status)
    elif workshop_status == 1:
        wwrs = WWorkshopRequests.objects.filter(status = workshop_status)
    else:
        wwrs = WWorkshopRequests.objects.filter(status = workshop_status)
        
    for wwr in wwrs:
        #Save department
        try:
            duser = get_user(wwr.organiser_id)
            if duser == None:
                print 'id:', wwr.id, 'user missing in auth_user'
                continue
            # Save Workshop
            w = None
            try:
                w = Training.objects.get(training_code = wwr.workshop_code)
                #print "Already exits !"
                continue
            except Exception, e:
                if not wwr.workshop_code and wwr.status == 2:
                    print 'id:', wwr.id, 'workshop code missing'
                    continue
                if not wwr.workshop_code:
                    wwr.workshop_code = "WC-"+str(wwr.id)
                #print e, " => 3 ", wwr.workshop_code
            #check organiser there or not
            organiser = None
            try:
                organiser = Organiser.objects.get(user_id = duser.id)
            except Exception, e:
                #print e
                print 'id:', wwr.id, "Organiser Not there => ", wwr.organiser_id
                continue
            #check dept in WDepartments
            wdept = wwr.department
            try:
                WDepartments.objects.get(name=wdept)
            except Exception, e:
                #print e, " => 1", wwr.workshop_code
                wdept = get_dept(wdept)
            
            # check in Department
            """dept = None
            try:
                dept = Department.objects.get(name=wdept)
            except Exception, e:
                #print e, " => 2",
                if ',' in wdept:
                    cwdept = wdept.split(',');
                    for d in cwdept:
                        try:
                            d = Department.objects.get(name = d)
                        except Exception, e:
                            print e, " => 2aa ", wwr.id, " => ", d
                            d = get_dept(d)
                        try:
                            Department.objects.get(name=d)
                        except Exception, e:
                            print e, " => 2ab ", wwr.id, " => ", d
                            #sys.exit(0)
                if not ',' in wdept:
                    try:
                        dept = Department.objects.create(name = wdept)
                    except:
                        dept = Department.objects.get(name = 'Others')"""
            
            #find academic_center id
            ac = None
            try:
                ac = AcademicCenter.objects.get(academic_code = wwr.academic_code)
            except Exception, e:
                #get organiser academic and set to workshop
                try:
                    o  = Organiser.objects.get(user_id = duser.id)
                    ac = AcademicCenter.objects.get(pk = o.academic_id)
                except Exception, e:
                    print 'id:', wwr.id, 'academic code missing'
                    continue
            #find foss_category_id
            foss = None
            try:
                if wwr.foss_category == 'Linux-Ubuntu':
                    wwr.foss_category = 'Linux'
                foss = FossCategory.objects.get(foss = wwr.foss_category.replace("-", " ").replace('+', 'p'))
            except Exception, e:
                #print e, " => 5 ", wwr.foss_category
                print 'id:', wwr.id, 'foss category missing', wwr.foss_category
                continue
                
             #find language_id
            lang = None
            try:
                lang = Language.objects.get(name = wwr.pref_language)
            except Exception, e:
                #print e, " => 6 ", wwr.pref_language
                print 'id:', wwr.id, 'language missing', wwr.pref_language
                continue
            
            # get participants count
            if workshop_status == 2:
                wp = None
                try:
                    wp = WWorkshopDetails.objects.get(workshop_code = wwr.workshop_code)
                except Exception, e:
                    #print e, " => 7 ", wwr.workshop_code
                    print 'id:', wwr.id, 'workshop details missing', wwr.workshop_code
                    continue
            """elif workshop_status == 1:
                try:
                    #WWorkshopFeedback.objects.filter(workshop_code = wwf.workshop_code).count()
                    wp = WWorkshopDetails.objects.get(workshop_code = wwr.workshop_code)
                    print "7aaa,  yes yes", wwr.workshop_code
                except Exception, e:
                    pass
            else:
                pass"""
                
            # new status
            wstatus = {0 : 0, 1 : 0, 2 : 4}
            w = Training()
            w.id = wwr.id
            w.organiser_id = organiser.id
            if workshop_status == 0:
                w.training_code = None
            else:
                w.training_code = wwr.workshop_code.upper()
            w.academic_id = ac.id
            w.foss_id = foss.id
            w.language_id = lang.id
            if workshop_status == 2:
                w.trdate = wwr.cfm_wkshop_date
                w.trtime = wwr.cfm_wkshop_time
            else:
                w.trdate = wwr.pref_wkshop_date
                w.trtime = wwr.pref_wkshop_time
            w.status = wstatus[wwr.status]
            w.skype = wwr.skype_request
            
            if 'MAH-00029' == wwr.academic_code:
                w.training_type = 2
            else:
                w.training_type = 1
            
            w.course_id = 1
            if workshop_status == 2:
                w.participant_counts = wp.no_of_participants
            else:
                w.participant_counts = 0
            
            if wwr.created_at:
                w.created = wwr.created_at
                w.updated = wwr.updated_at
            else:
                w.created = datetime.datetime.now()
                w.updated = datetime.datetime.now()
            try:
                #continue
                w.save()
            except Exception, e:
                #print "Duplicate ---", wwr.workshop_code, " => ", wwr.academic_code, wwr.cfm_wkshop_date, wwr.foss_category
                post_time = 5
                for i in range(150):
                    try:
                        post_five_min = datetime.datetime.combine(datetime.date.today(), wwr.cfm_wkshop_time) + datetime.timedelta(minutes=post_time)
                        w.trtime = post_five_min.time()
                        w.save()
                        break
                    except Exception, e:
                        #duplicate because of unique_together
                        #print "Duplicate post change time save ******", wwr.workshop_code, " => ", wwr.academic_code, wwr.cfm_wkshop_date, 
                        post_time = post_time + 5
                        if i >= 149:
                            print 'i exceeded 149'
                        continue
            
            #save departments
            try:
                try:
                    d = Department.objects.get(name = wdept)
                    w.department.add(d)
                    w.save()
                except Exception, e:
                    if ',' in wdept:
                        cwdept = wdept.split(',');
                        #print "*********", cwdept
                        #w.department.clear()
                        for dept in cwdept:
                            try:
                                dept = Department.objects.get(name = dept)
                            except Exception, e:
                                #print e, " => sss ", wwr.workshop_code, " => ", dept
                                dept = get_dept(dept)
                            try:
                                dept = Department.objects.get(name = dept)
                                w.department.add(dept)
                            except:
                                pass
                    w.save()
            
            except Exception, e:
                print e, " => 8", wwr.workshop_code, " => ", wdept
                w.delete()
                continue
        except Exception, e:
            #print "Something went wrong!"
            print e, "Something went wrong => 9", wwr.id," => ", wwr.workshop_code, "Organiser => ", wwr.organiser_id
            #sys.exit(0)
            continue
    return HttpResponse("Workshop migration Done!")
    

def workshop_feedback(request):
    wwfs = WWorkshopFeedback.objects.all()
    for wwf in wwfs:
        #existing record
        try:
            TrainingFeedback.objects.get(training_id = training.id, mdluser_id = wwf.user_id )
            continue
        except:
            pass
        # find the training id
        training = None
        try:
            training = Training.objects.get(training_code = wwf.workshop_code)
        except Exception, e:
            print e, " => 1 ", wwf.workshop_code, " => ", wwf.user_id, " => ", wwf.id
            
            #get the workshop form WWorkshopRequests where status = 3
            wpc = WWorkshopFeedback.objects.filter(workshop_code = wwf.workshop_code).count()
            #if wpc > 0:
            #    training.status = 4
            #    training.participant_counts = wpc
            #    training.save()
            #    print "Workshop Details fil", wwf.workshop_code, " => p ", wpc
            #else:
            continue
            #sys.exit()
        
         #find language_id
        lang = None
        try:
            lang = Language.objects.get(name = wwf.workshop_language)
        except Exception, e:
            #todo: if reginal get language from w
            try:
                if wwf.workshop_language == 'Regional':
                    te = Training.objects.get(training_code = wwf.workshop_code)
                    lang = Language.objects.get(name = te.language)
                else:
                    lang = Language.objects.get(name = 'English')
            except Exception, ee:
                print e, " => 6 ", wwf.workshop_language
                print ee, " => 6aa ", wwf.workshop_language
                continue
                
        try:
            TrainingFeedback.objects.get(training_id = training.id, mdluser_id = wwf.user_id )
            #print "already exits!"
            continue
        except Exception, e:
            print e, " => 2", wwf.workshop_code, " => ", wwf.user_id
            try:
                t = TrainingFeedback()
                t.mdluser_id  = wwf.user_id
                t.training_id  = training.id
                t.rate_workshop  = wwf.rate_workshop
                t.content  = wwf.content
                t.sequence  = wwf.logical_arrangement
                t.clarity  = wwf.clarity
                t.interesting  = wwf.understandable
                t.appropriate_example  = wwf.included_examples
                t.instruction_sheet  = wwf.instruction_sheet
                t.assignment  = wwf.assignments
                t.pace_of_tutorial  = wwf.pace_tutorial
                t.workshop_learnt  = wwf.useful_thing
                t.weakness_workshop  = wwf.weakness_duration
                t.weakness_narration  = wwf.weakness_narration
                t.weakness_understand  = wwf.weakness_understand
                t.other_weakness  = wwf.other_weakness
                t.tutorial_language  = lang.id
                t.apply_information  = wwf.info_received
                t.setup_learning  = wwf.comfortable_learning
                t.computers_lab  = wwf.working_computers
                t.audio_quality  = wwf.audio_quality
                t.video_quality  = wwf.video_quality
                t.workshop_orgainsation  = wwf.orgn_wkshop
                t.faciliate_learning  = wwf.facil_learning
                t.motivate_learners  = wwf.motiv_learning
                t.time_management  = wwf.time_mgmt
                t.knowledge_about_software  = wwf.soft_klg
                t.provide_clear_explanation  = wwf.prov_expn
                t.answered_questions  = wwf.ans_cln
                t.interested_helping  = wwf.help_lern
                t.executed_workshop  = wwf.exec_effly
                t.workshop_improved  = wwf.ws_improved
                t.recommend_workshop  = wwf.recomm_wkshop
                t.use_information  = wwf.reason_why
                t.other_comments  = wwf.general_comment
                
                if wwf.updated_at:
                    t.created  = wwf.updated_at
                else:
                    t.created  = datetime.datetime.now()
                t.save()
                
                #Save training attendance register
                try:
                    TrainingAttendance.objects.get(training_id = training.id, mdluser_id = wwf.user_id)
                except Exception, e:
                    print e, " => sss"
                    t = TrainingAttendance()
                    t.training_id = training.id
                    t.mdluser_id = wwf.user_id
                    t.status = 1
                    
                    if wwf.updated_at:
                        t.created  = wwf.updated_at
                        t.updated  = wwf.updated_at
                    else:
                        t.created  = datetime.datetime.now()
                        t.updated  = datetime.datetime.now()
                    t.save()
            except Exception, e:
                print e, " => 3", wwf.workshop_code, " => ", wwf.user_id
                sys.exit()
    return HttpResponse("Workshop Feedback migration Done!")
    

def workshop_livefeedback(request):
    wwfs = WLiveWorkshopParticipants.objects.all()
    for wwf in wwfs:
        # find the training id
        training = None
        try:
            training = Training.objects.get(training_code = wwf.workshop_code)
        except Exception, e:
            print e, " => 1 ", wwf.workshop_code, " => ", wwf.user_id, " => ", wwf.id
            #wpc = WWorkshopFeedback.objects.filter(workshop_code = wwf.workshop_code).count()
            continue
            
        #existing record
        try:
            TrainingLiveFeedback.objects.get(training_id = training.id, email = wwf.email )
            continue
        except:
            pass
        
        lang = None
        try:
            lang = Language.objects.get(name = wwf.workshop_language)
        except Exception, e:
            #todo: if reginal get language from w
            try:
                if wwf.workshop_language == 'Regional':
                    te = Training.objects.get(training_code = wwf.workshop_code)
                    lang = Language.objects.get(name = te.language)
                else:
                    lang = Language.objects.get(name = 'English')
            except Exception, ee:
                print e, " => 6 ", wwf.workshop_language
                print ee, " => 6aa ", wwf.workshop_language
                continue
                
        try:
            TrainingLiveFeedback.objects.get(training_id = training.id, mdluser_id = wwf.user_id )
            #print "already exits!"
            continue
        except Exception, e:
            #print e, " => 2", wwf.workshop_code, " => ", wwf.user_id
            try:
                t = TrainingLiveFeedback()
                
                t.name = wwf.pname
                t.email = wwf.email
                t.branch = wwf.branch
                t.institution = wwf.institution
                
                t.training_id  = training.id
                t.rate_workshop  = wwf.rate_workshop
                t.content  = wwf.content
                t.sequence  = wwf.logical_arrangement
                t.clarity  = wwf.clarity
                t.interesting  = wwf.understandable
                t.appropriate_example  = wwf.included_examples
                t.instruction_sheet  = wwf.instruction_sheet
                t.assignment  = wwf.assignments
                t.pace_of_tutorial  = wwf.pace_tutorial
                t.workshop_learnt  = wwf.useful_thing
                t.weakness_workshop  = wwf.weakness_duration
                t.weakness_narration  = wwf.weakness_narration
                t.weakness_understand  = wwf.weakness_understand
                t.other_weakness  = wwf.other_weakness
                t.tutorial_language  = lang.id
                t.apply_information  = wwf.info_received
                t.setup_learning  = wwf.comfortable_learning
                t.computers_lab  = wwf.working_computers
                t.audio_quality  = wwf.audio_quality
                t.video_quality  = wwf.video_quality
                t.workshop_orgainsation  = wwf.orgn_wkshop
                t.faciliate_learning  = wwf.facil_learning
                t.motivate_learners  = wwf.motiv_learning
                t.time_management  = wwf.time_mgmt
                t.knowledge_about_software  = wwf.soft_klg
                t.provide_clear_explanation  = wwf.prov_expn
                t.answered_questions  = wwf.ans_cln
                t.interested_helping  = wwf.help_lern
                t.executed_workshop  = wwf.exec_effly
                t.workshop_improved  = wwf.ws_improved
                t.recommend_workshop  = wwf.recomm_wkshop
                t.use_information  = wwf.reason_why
                t.other_comments  = wwf.general_comment
                
                if wwf.updated_at:
                    t.created  = wwf.updated_at
                else:
                    t.created  = datetime.datetime.now()
                t.save()
                    
                if wwf.updated_at:
                    t.created  = wwf.updated_at
                    t.updated  = wwf.updated_at
                else:
                    t.created  = datetime.datetime.now()
                    t.updated  = datetime.datetime.now()
                t.save()
            except Exception, e:
                print e, " => 3", wwf.workshop_code, " => ", wwf.email
                sys.exit()
    return HttpResponse("Workshop Feedback migration Done!")

def test(request):
    test_status = 0
    if test_status == 4:
        wtrs = WTestRequests.objects.filter(status = test_status)
    elif test_status == 2:
        wtrs = WTestRequests.objects.filter(status = test_status, cfm_test_date__gte = datetime.datetime.today())
    elif test_status == 1:
        wtrs = WTestRequests.objects.filter(status = test_status, pref_test_date__gte = datetime.datetime.today())
    elif test_status == 0:
        wtrs = WTestRequests.objects.filter(status = test_status, pref_test_date__gte = datetime.datetime.today())

    for wtr in wtrs:
        print old_treq.cfm_test_date, "sssssss", old_treq.test_code, old_treq.cfm_test_date, old_treq.cfm_test_time
        #Save department
        douser = get_user(old_treq.organiser_id)
        if douser == None:
            print 'id', old_treq.id, 'Organiser id missing', old_treq.organiser_id
            continue
        try:
            # Save Workshop
            w = None
            try:
                w = Test.objects.get(test_code = old_treq.test_code)
                print "Already exits !"
                continue
            except Exception, e:
                pass
                #print e, " => 3 ", old_treq.test_code, old_treq.academic_code
                #if not old_treq.test_code:
                    #old_treq.test_code = "TC-"+str(old_treq.id)
            #check organiser there or not
            organiser = None
            try:
                organiser = Organiser.objects.get(user_id = douser.id)
            except Exception, e:
                #print e
                print 'id', old_treq.id, 'Organiser record missing', old_treq.organiser_id
                continue
            
            #check organiser there or not
            diuser = get_user(old_treq.invigilator_id)
            if diuser == None:
                print 'id', old_treq.id, 'Invigilator id missing', old_treq.invigilator_id
            invigilator = None
            new_invigilator_id = None
            try:
                invigilator = Invigilator.objects.get(user_id = diuser.id)
                new_invigilator_id = invigilator.id
            except Exception, e:
                if not old_treq.invigilator_id:
                    try:
                        ac = AcademicCenter.objects.get(academic_code = old_treq.academic_code)
                        invigilator = Invigilator.objects.filter(academic_id = ac.id).first()
                        if not invigilator:
                            new_invigilator_id = None
                        else:
                            new_invigilator_id = invigilator.id
                    except Exception, e:
                        new_invigilator_id = None
                else:
                    print 'id:', old_treq.id, 'Invigilator record missing', old_treq.invigilator_id
                    new_invigilator_id = None
            ac = None
            try:
                ac = AcademicCenter.objects.get(academic_code = old_treq.academic_code)
            except Exception, e:
                try:
                    o  = Organiser.objects.get(user_id = old_treq.douser.id)
                    ac = AcademicCenter.objects.get(pk = o.academic_id)
                except Exception, e:
                    print 'id:', old_treq.id, 'Academic code missing'
                #continue
            #find foss_category_id
            foss = None
            try:
                if old_treq.foss_category == 'Linux-Ubuntu':
                    old_treq.foss_category = 'Linux'
                if old_treq.foss_category in ['C', 'C-Plus-Plus', 'C-and-C-Plus-Plus']:
                    old_treq.foss_category = 'C and Cpp'
                foss = FossCategory.objects.get(foss = old_treq.foss_category.replace("-", " "))
            except Exception, e:
                print 'id:', old_treq.id, 'Foss category missing', old_treq.foss_category.replace("-", " ")
                continue
            # get participants count
            wp = None
            if old_treq.status == 4:
                try:
                    wp = WTestDetails.objects.filter(test_code = old_treq.test_code).aggregate(Sum('no_of_participants'))
                except Exception, e:
                    print 'id:', old_treq.id, 'Test Details Missing', old_treq.test_code
                    continue
            if test_status == 4 and not wp['no_of_participants__sum']:
                print 'id:', old_treq.id, 'Test Details Missing', old_treq.test_code
                continue
            w = Test()
            w.id = old_treq.id
            w.organiser_id = organiser.id
            w.invigilator_id = new_invigilator_id
            w.test_code = old_treq.test_code.upper()
            w.academic_id = ac.id
            w.foss_id = foss.id
            
            if old_treq.cfm_test_date and old_treq.cfm_test_time:
                w.tdate = old_treq.cfm_test_date
                w.ttime = old_treq.cfm_test_time
            else:
                w.tdate = old_treq.pref_test_date
                w.ttime = old_treq.pref_test_time
            
            w.status = old_treq.status
            
            w.test_category_id = 1
            
            if test_status == 4:
                w.participant_count = wp['no_of_participants__sum']
            else:
                w.participant_count = 0
            
            if old_treq.created_at:
                w.created = old_treq.created_at
                w.updated = old_treq.updated_at
            else:
                w.created = datetime.datetime.now()
                w.updated = datetime.datetime.now()
            try:
                #continue
                w.save()
            except Exception, e:
                print e, "Duplicate ---", old_treq.test_code, " => ", old_treq.academic_code, old_treq.cfm_test_date, old_treq.foss_category
                #sys.exit(0)
                post_time = 5
                for i in range(150):
                    try:
                        post_five_min = datetime.datetime.combine(datetime.date.today(), old_treq.cfm_test_time) + datetime.timedelta(minutes=post_time)
                        w.ttime = post_five_min.time()
                        w.save()
                        break
                    except Exception, e:
                        #duplicate because of unique_together
                        print e, "Duplicate post change time save ******", old_treq.test_code, " => ", old_treq.academic_code, old_treq.cfm_test_date, 
                        if i >= 149:
                            print 'i exceeded'
                        post_time = post_time + 5
                        continue
            #save departments
            try:
                try:
                    d = Department.objects.get(name = wdept)
                    w.department.add(d)
                    w.save()
                except Exception, e:
                    if ',' in wdept:
                        cwdept = wdept.split(',');
                        #print "*********", cwdept
                        #w.department.clear()
                        for dept in cwdept:
                            try:
                                dept = Department.objects.get(name = dept)
                            except Exception, e:
                                print e, " => sss ", old_treq.test_code, " => ", dept
                                dept = get_dept(dept)
                            if dept:
                                dept = Department.objects.get(name = dept)
                                w.department.add(dept)
                    w.save()
            
            except Exception, e:
                print e, " => 8", old_treq.test_code, " => ", wdept, old_treq.department
                w.delete()
                continue
        except Exception, e:
            print "Something went wrong!"
            print e, " => 9", old_treq.id," => ", old_treq.test_code
            print "Organiser => ", old_treq.organiser_id
            continue
    return HttpResponse("Test migration Done!")
    
def test_attendance(request):
    tas = WAttendanceRegister.objects.all()
    for ta in tas:
        
        mdluser = None
        try:
            mdluser = MdlUser.objects.get(id = ta.moodle_uid)
        except:
            print 'id:', ta.id, 'MdlUser missing', ta.moodle_uid
            continue
        
        test = None
        try:
            test = Test.objects.get(test_code = ta.test_code)
        except Exception, e:
            print 'id:', ta.id, 'Test missing', ta.test_code
            continue
        
        try:
            TestAttendance.objects.get(test_id = test.id, mdluser_id = ta.moodle_uid)
            continue
        except:
            pass
        
        #check weather student attent in current foss mdl courses available
        mdlcourse = None
        try:
            mdlcourse = FossMdlCourses.objects.get(foss = test.foss)
        except:
            print 'id:', test.id, 'FossMdlCourses missing', test.foss
            continue
            
        mdlcourse_id = 0
        mdlquiz_id = 0
        try:
            mdlgrade = MdlQuizGrades.objects.filter(quiz = mdlcourse.mdlquiz_id, userid = ta.moodle_uid).first()
            if mdlgrade:
                mdlcourse_id = mdlcourse.mdlcourse_id
                mdlquiz_id = mdlcourse.mdlquiz_id
            #else:
            #    print 'id:', ta.id, 'student grade missing, Old Quiz', ta.moodle_uid
        except:
            #print 'id:', ta.id, 'student grade missing, Old Quiz', ta.moodle_uid
            pass
        
        try:
            t = TestAttendance()
            t.mdluser_id = ta.moodle_uid
            t.test_id = test.id
            
            t.mdlcourse_id = mdlcourse_id
            t.mdlquiz_id = mdlquiz_id
            
            t.mdluser_firstname = mdluser.firstname.lower().title()
            t.mdluser_lastname = mdluser.lastname.lower().title()
            
            t.status = 3
            if ta.status == 0:
                t.status = 0
            
            t.created = datetime.datetime.now()
            t.updated = datetime.datetime.now()
            
            t.save()
        except Exception, e:
            print 'id:', ta.id, 'Failed', ta.moodle_uid
            return HttpResponse("Test attendance migration Done!")
    return HttpResponse("Test attendance migration Done!")

def get_user(old_user_id):
#find the user
    user = None
    try:
        user = Users.objects.get(pk = old_user_id)
    except Exception, e:
        #print e, " user not getting"
        return None

    name = user.name
    if len(name) > 30:
        name = user.mail
        if len(name) > 30:
            tmp_name = name.split("@")
            name = tmp_name[0]

    duser = None
    try:
        duser = User.objects.get(email = user.mail)
    except:
        try:
            duser = User.objects.get(username = name)
        except Exception, e:
            #print e, " ======> ", user.mail, user.name
            pass
    return duser

def test_foss_fix(request):
    tests = Test.objects.all()
    for test in tests:
        wtest = WTestRequests.objects.get(pk = test.id)
        foss = None
        if wtest.foss_category == 'C':
            foss = FossCategory.objects.get(foss = 'C')
        if wtest.foss_category == 'C-Plus-Plus':
            foss = FossCategory.objects.get(foss = 'Cpp')
            
        if not foss:
            continue
        
        test.foss = foss
        test.save()
        print "completed => ", test.test_code
    return HttpResponse("Test foss fix migration Done!")

def test_workshop_link(request):
    old_treqs = WTestRequests.objects.all()
    for old_treq in old_treqs:
        if old_treq.workshop_code == '' or old_treq.workshop_code == None or old_treq.test_code == '' or old_treq.test_code == None:
            continue
        try:
            new_wr = Training.objects.get(training_code = old_treq.workshop_code)
        except Exception, e:
            print e, "id:", old_treq.id
            continue
        try:
            new_treq = Test.objects.get(test_code = old_treq.test_code)
        except Exception, e:
            print e, "id:", old_treq.id
            continue
        new_treq.training = new_wr
        
        dept = None
        wdept = old_treq.department
        try:
            dept = Department.objects.get(name=wdept)
        except Exception, e:
            print e, "id:", old_treq.id
            dept = Department.objects.get(name='Others')
            #wdept = get_dept(wdept)
                
        #save dept
        new_treq.department.add(dept.id)
        new_treq.save()

def test_workshop_pending_link(request):
    old_treqs = WTestRequests.objects.all()
    for old_treq in old_treqs:
        if old_treq.workshop_code == '' or old_treq.workshop_code == None:
            continue
        try:
            new_wr = Training.objects.get(training_code = old_treq.workshop_code)
        except Exception, e:
            print e, "id:", old_treq.id
            continue
        try:
            new_treq = Test.objects.get(id = old_treq.id)
        except Exception, e:
            print e, "id:", old_treq.id
            continue
        new_treq.training = new_wr
        if new_treq.test_code == '' or new_treq.test_code == None:
            new_treq.test_code = 'TC-' + str(new_treq.id)
        dept = None
        wdept = old_treq.department
        try:
            dept = Department.objects.get(name=wdept)
        except Exception, e:
            print e, "id:", old_treq.id
            dept = Department.objects.get(name='Others')
            #wdept = get_dept(wdept)
                
        #save dept
        new_treq.department.add(dept.id)
        new_treq.save()

def old_test_to_new(request):
    old_treqs = WTestRequests.objects.all()

    for old_treq in old_treqs:
        if old_treq.status == 5:
            continue

        #fetching academic center record
        try:
            academic_center = AcademicCenter.objects.get(academic_code = old_treq.academic_code)
        except:
            print 'id:', old_treq.id, 'Academic record missing:', old_treq.academic_code
            continue

        # Fetching organiser record
        organiser_user = get_user(old_treq.organiser_id)
        if organiser_user == None:
            print 'id:', old_treq.id, 'Organiser user record missing - uid:', old_treq.organiser_id
            continue
        try:
            organiser = Organiser.objects.get(user = organiser_user)
        except Exception, e:
            #print e
            #break
            organiser = Organiser.objects.create(
                user = organiser_user,
                academic = academic_center,
                status = 1,
            )
        try:
            organiser_user.groups.get(name='Organiser')
        except:
            try:
                organiser_user.groups.add(Group.objects.get(name='Organiser'))
            except:
                pass

        #Fetching invigilator record
        invigilator_user = get_user(old_treq.invigilator_id)
        if invigilator_user == None:
            #print 'id:', old_treq.id, 'Invigilator user record missing - uid:', old_treq.invigilator_id
            invigilator = None
            #continue
        else:
            try:
                invigilator = Invigilator.objects.get(user = invigilator_user)
            except:
                invigilator = Invigilator.objects.create(
                    user = invigilator_user,
                    academic = academic_center,
                    status = 1,
                )
                try:
                    invigilator_user.groups.get(name='Invigilator')
                except:
                    try:
                        invigilator_user.groups.add(Group.objects.get(name='Invigilator'))
                    except:
                        pass

        foss = None
        try:
            if old_treq.foss_category == 'Linux-Ubuntu':
                old_treq.foss_category = 'Linux'
            if old_treq.foss_category in ['C', 'C-Plus-Plus', 'C-and-C-Plus-Plus']:
                old_treq.foss_category = 'C and Cpp'
            foss = FossCategory.objects.get(foss = old_treq.foss_category.replace("-", " "))
        except Exception, e:
            print 'id:', old_treq.id, 'Foss category missing', old_treq.foss_category.replace("-", " ")
            continue

        #Fetching workshop record
        workshop = None
        test_category = TestCategory.objects.get(name='Others')
        if old_treq.workshop_code != '' and old_treq.workshop_code != None:
            try:
                workshop = Training.objects.get(training_code = old_treq.workshop_code)
                test_category = TestCategory.objects.get(name='Workshop')
            except:
                pass

        try:
            department = Department.objects.get(name = old_treq.department)
        except:
            department = Department.objects.get(name = 'Others')
        participants_count = 0
        td_recs = WTestDetails.objects.filter(test_code = old_treq.test_code)
        for td_rec in td_recs:
            participants_count = participants_count + int(td_rec.no_of_participants)
        created = None
        updated = None
        if old_treq.cfm_test_date and old_treq.cfm_test_time:
            tdate = old_treq.cfm_test_date
            ttime = old_treq.cfm_test_time
        else:
            tdate = old_treq.pref_test_date
            ttime = old_treq.pref_test_time
        if old_treq.created_at:
            created = old_treq.created_at
            created_str = str(old_treq.created_at)
        else:
            created = datetime.datetime.now()
            created_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        test_code = 'TC-' + str(old_treq.id)
        try:
            new_treq = Test.objects.get(pk = old_treq.id)
            new_treq.organiser = organiser
            new_treq.test_category = test_category
            new_treq.invigilator = invigilator
            new_treq.academic = academic_center
            new_treq.training = workshop
            new_treq.foss = foss
            new_treq.test_code = test_code
            new_treq.tdate = tdate
            new_treq.ttime = ttime
            #new_treq.status = old_treq.status
            new_treq.participant_count = participants_count
            new_treq.created = created
            new_treq.updated = created
            try:
                new_treq.save()
            except:
                post_time = 5
                for i in range(150):
                    try:
                        post_five_min = datetime.datetime.combine(datetime.date.today(), ttime) + datetime.timedelta(minutes=post_time)
                        ttime = post_five_min.time()
                        new_treq.ttime = ttime
                        new_treq.save()
                        break
                    except:
                        if i >= 149:
                            print '1 - i exceeded'
                        post_time = post_time + 5
        except Exception, e:
            #print 'main', e
            try:
                new_treq = Test.objects.create(
                    id = old_treq.id,
                    organiser = organiser,
                    test_category = test_category,
                    invigilator = invigilator,
                    academic = academic_center,
                    training = workshop,
                    foss = foss,
                    test_code = test_code,
                    tdate = tdate,
                    ttime = ttime,
                    status = old_treq.status,
                    participant_count = participants_count,
                    created = created,
                    updated = created
                )
            except Exception, e:
                #print 'sub', e
                post_time = 5
                for i in range(150):
                    try:
                        post_five_min = datetime.datetime.combine(datetime.date.today(), ttime) + datetime.timedelta(minutes=post_time)
                        ttime = post_five_min.time()
                        new_treq = Test.objects.create(
                            id = old_treq.id,
                            organiser = organiser,
                            test_category = test_category,
                            invigilator = invigilator,
                            academic = academic_center,
                            training = workshop,
                            foss = foss,
                            test_code = test_code,
                            tdate = tdate,
                            ttime = ttime,
                            status = old_treq.status,
                            participant_count = participants_count,
                            created = created,
                            updated = updated
                        )
                        break
                    except Exception, e:
                        #print e
                        if i >= 149:
                            print '2 - i exceeded'
                        post_time = post_time + 5
        cursor = connection.cursor()
        cursor.execute("""update events_test set created='""" + str(created_str) + """', updated='""" + str(created_str) + """' where id=""" + str(new_treq.id))
        new_treq.department.add(department.id)
    return HttpResponse("Success!")

def get_course(dept):
    getCourse = {
        'CSE':'BE',
        'Others':'Others',
        'Dept. of Computer Science and Engineering':'BE',
        'COMPUTER INFORMATION TECHNOLOGY':'BE',
        'ECE, IT, CSE, EEE, MCA':'BE',
        'Department of Computer Application':'MCA',
        'INFORMATION TECHNOLOGY':'BE',
        'Computer Science & Engineering':'BE',
        '50':'Others',
        'E&TC':'BE',
        'Department of Computer Applications':'MCA',
        'Common to all Branches - 1st semester':'Others',
        'Computer Applications':'MCA',
        'Computer Science':'BE',
        'CSE & IT':'BE',
        'DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING':'BE',
        'School':'Others',
        'ELECTRONICS AND COMMUNICATION ENGINEERING DEPARTME':'BE',
        'School of Elect. Engg and IT':'BE',
        'Computer Science Engineering':'BE',
        'E&TC and CS':'BE',
        'BCA B.Com B.SC':'BE',
        'COMPUTER SCIENCE AND ENGINEERING':'BE',
        'BCA-III Students':'BCA',
        'Department of Electronics':'BE',
        'Computer Science Engg.':'BE',
        'DEPARTMENT OF COMPUTER ENGINEERING':'BE',
        'Computer Engineering':'BE',
        'Electronics & Telecomunication':'BE',
        'EECE':'BE',
        'Computer':'BE',
        'MECHANICAL ENGINEERING':'BE',
        'E&TC ENGINEERING':'BE',
        'CIVIL ENGINEERING':'BE',
        'PRODUCTION ENGINEERING':'BE',
        'INSTRUMENTATION ENGINEERING':'BE',
        'Dept. of Electronics and Communication Engineering':'BE',
        'All(Faculity Members, FDP)':'Others',
        'Mechanical':'BE',
        'IT':'BE',
        'Oceanography':'Others',
        'Chemistry':'BSc',
        'CSE Department':'BE',
        'Linux':'Others',
        'Electrical Engineering':'BE',
        'BSH':'Others',
        'Central Library KKHSOU':'Others',
        'Central Library':'Others',
        'KTurtle Pilot Workshop for class VII students':'Others',
        'COPA':'Others',
        'Morigaon College':'Others',
        'Computer GU':'Others',
        'Civil':'BE',
        'CSE IT MCA':'BE',
        'EEE ECE':'BE',
        'Civil Mech':'BE',
        'MCA':'MCA',
        'Computer and IT Department':'BE',
        'Department of Computer Science':'BE',
        'TechFest-2013 participants':'Others',
        'CSI-IT2020 Participants':'Others',
        'ECE':'BE',
        'AERONAUTICAL':'BE',
        'EEE':'BE',
        'Department of IT':'BE',
        'Electronics and Communication Engineering':'BE',
        'Library':'Others',
        'cs':'BE',
        'School of Computer Science':'Others',
        'School of Chemical and Biotechnology':'Others',
        'Faculty':'Others',
        'THE FUTURE COMPUTER SCIENCE COLLEGE':'Others',
        'Information Technology and Computer science and en':'BE',
        'MATHEMATICS':'Others',
        'EC':'BE',
        'Information Science':'BE',
        'Civil Mechanical':'BE',
        'DEPARTMENT OF MATHEMATICS':'Others',
        'Open to All':'Others',
        'IT and Computer Science':'BE',
        'BCA':'BCA',
        'Department of Information Technology':'BE',
        'Sowdambika Polytechnic College':'Diploma',
        'computers and information technology':'BE',
        'electronics':'BE',
        'ELECTRONICS AND COMMUNICATION':'BE',
        'Future Computer Science College':'Others',
        'Kamani Science College':'Others',
        'P S HIRPARA MAHILA COLLEGE':'Others',
        'ComputerScience':'BE',
        'Master of Computer':'MCA',
        'Computer science and engineering department':'BE',
        'computer Science Dept':'BE',
        'MCA staff and faculty':'MCA',
        'Administrative':'Others',
        'Physics':'MSc',
        'Telecommunication and Engineering':'BE',
        'GYANBHARTI COMPUTER SCIENCE COLLEGE':'Others',
        'Department of Computer Science and Technology':'BE',
        'ELECTRONIC':'BE',
        'INFORMATION TECH':'BE',
        'ECE CIVIL CSE':'BE',
        'CSE IT':'BE',
        'ALL':'Others',
        'Department of Electrical and Electronics Engineeri':'BE',
        'ELECTRONICCS':'BE',
        'Electrical and Communication Engineering':'BE',
        'CSE MCA':'BE',
        'CSEIT':'BE',
        'VARMORA COLLEGE':'Others',
        'Department of Physics':'MSc',
        'Electronics and Telecommunication':'BE',
        'Computer Sc and Engg':'BE',
        'Chemical Engineering':'BE',
        'Computer Scince':'BE',
        'Department of Computer Science and Engineering':'BE',
        'AUTOMOBILE ENGINEERING':'BE',
        'Department of Technology':'BE',
        'GAJERA SANKUL':'Others',
        'electrical and electronics':'BE',
        'INSTRUMENTATION AND CONTROL':'BE',
        'ME':'BE',
        'Information Tehnology':'BE',
        'Computational Biology and Bioinformatics':'BE',
        'EC Department':'BE',
        'G K C K BOSAMIYA COLLEGE':'Others',
        'CST':'BSc',
        'COMPUTERS':'BE',
        'EXTC':'BE',
        'CE':'BE',
        'MAC BTECH':'BTech',
        'Electrical and Electronics Engineering':'BE',
        'Telecommunication Engineering':'BE',
        'Master of Bussiness Administration':'MBA',
        'Electronics and instrumentation Engineering':'BE',
        'Science':'Others',
        'Earth Sciences':'Others',
        'Aeronautical Engineering':'BE',
        'Aerospace':'BE',
        'Arts':'BSc',
        'Law':'BL',
        'Polytechnic':'Diploma',
        'Petrochemical Engineering':'BE',
        'Textile Engineering':'BE',
        'Biomedical Engineering':'BE',
        'Production Engineering':'BE',
        'Mechanical Design Engineering':'BE',
        'Applied Physics':'Others',
        'Applied Mathematics':'Others',
        'Commerce and Management':'BComm',
        'Soil and Water Engineering':'BE',
        'Thermal Engineering':'BE',
        'Agricultural Process and Food Engineering':'BE',
        'Structural Engineering':'BE',
        'Instrumentation and  Control Engineering':'BE',
        'Department of Foods and Nutrition':'Others',
        'Biochemical Engineering':'BE',
        'Energy Engineering':'BE',
    }

    if dept in getCourse:
        return getCourse[dept]

    return 'Others'

def old_workshop_to_new(request):
    old_wreqs = WWorkshopRequests.objects.all()
    for old_wreq in old_wreqs:
        # skip records with status 3
        if old_wreq.status == 3:
            continue

         #fetching academic center record
        try:
            academic_center = AcademicCenter.objects.get(academic_code = old_wreq.academic_code)
        except:
            print 'id:', old_wreq.id, 'Academic record missing:', old_wreq.academic_code
            continue

        # Fetching organiser record
        organiser_user = get_user(old_wreq.organiser_id)
        if organiser_user == None:
            print 'id:', old_wreq.id, 'Organiser user record missing - uid:', old_wreq.organiser_id
            continue
        try:
            organiser = Organiser.objects.get(user = organiser_user)
        except Exception, e:
            #print e
            #break
            organiser = Organiser.objects.create(
                user = organiser_user,
                academic = academic_center,
                status = 1,
            )
            try:
                organiser_user.groups.get(name='Organiser')
            except:
                try:
                    organiser_user.groups.add(Group.objects.get(name='Organiser'))
                except:
                    pass

        #training code
        training_code = 'WC-' + str(old_wreq.id)

        #language record
        try:
            language = Language.objects.get(name = old_wreq.pref_language)
        except Exception, e:
            language = Language.objects.get(name = 'English')

        #foss category
        foss = None
        try:
            if old_wreq.foss_category == 'Linux-Ubuntu':
                old_wreq.foss_category = 'Linux'
            if old_wreq.foss_category in ['C', 'C-Plus-Plus', 'C-and-C-Plus-Plus', 'C-and-C++', 'C-and-C-Plus-Plus,Geogebra,Java,KTurtle,Linux,Linux-Ubuntu,OpenFOAM,PHP-and-MySQL,Python,Scilab', 'C-and-C-Plus-Plus,Java,PHP-and-MySQL,Python,Scilab']:
                old_wreq.foss_category = 'C and Cpp'
            if old_wreq.foss_category == 'Advanced-C++':
                old_wreq.foss_category = 'Advanced Cpp'
            foss = FossCategory.objects.get(foss = old_wreq.foss_category.replace("-", " "))
        except Exception, e:
            print 'id:', old_wreq.id, 'Foss category missing', '"' + old_wreq.foss_category + '"'
            continue

        # generating date and time
        if old_wreq.cfm_wkshop_date and old_wreq.cfm_wkshop_time:
            tdate = old_wreq.cfm_wkshop_date
            ttime = old_wreq.cfm_wkshop_time
        else:
            tdate = old_wreq.pref_wkshop_date
            ttime = old_wreq.pref_wkshop_time
        if old_wreq.created_at:
            created = old_wreq.created_at
            created_str = str(old_wreq.created_at)
        else:
            created = datetime.datetime.now()
            created_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # get course
        course_name = get_course(old_wreq.department)
        #print course_name
        course = Course.objects.get(name = course_name)

        # participants count
        participants_count = 0
        count_recs = WWorkshopDetails.objects.filter(workshop_code = training_code)
        for count_rec in count_recs:
            participants_count = participants_count + int(count_rec.no_of_participants)
        if participants_count == 0:
            participants_count = WWorkshopFeedback.objects.filter(workshop_code = training_code).count()

        # status
        status = int(old_wreq.status)
        if status == 1:
            status = 0

        # training type
        training_type = 1
        if old_wreq.academic_code == 'MAH-00029':
            training_type = 2
        try:
            new_wreq = Training.objects.get(id = old_wreq.id)
            new_wreq.organiser = organiser
            new_wreq.academic = academic_center
            new_wreq.course = course
            new_wreq.training_type = training_type
            new_wreq.training_code = training_code
            new_wreq.language = language
            new_wreq.foss = foss
            new_wreq.skype = old_wreq.skype_request
            new_wreq.participant_counts = participants_count
            new_wreq.save()
        except Exception, e:
            #print 'main', e, 'id:', old_wreq.id
            try:
                new_wreq = Training.objects.create(
                    id = old_wreq.id,
                    organiser = organiser,
                    appoved_by = None,
                    academic = academic_center,
                    course = course,
                    training_type = training_type,
                    training_code = training_code,
                    language = language,
                    foss = foss,
                    trdate = tdate,
                    trtime = ttime,
                    skype = old_wreq.skype_request,
                    status = status,
                    participant_counts = participants_count,
                    created = created,
                    updated = created
                )
            except Exception, e:
                print 'sub1', e, 'id:', old_wreq.id
                post_time = 5
                for i in range(150):
                    try:
                        post_five_min = datetime.datetime.combine(datetime.date.today(), ttime) + datetime.timedelta(minutes=post_time)
                        ttime = post_five_min.time()
                        new_wreq = Training.objects.create(
                            id = old_wreq.id,
                            organiser = organiser,
                            appoved_by = None,
                            academic = academic_center,
                            course = course,
                            training_type = training_type,
                            training_code = training_code,
                            language = language,
                            foss = foss,
                            trdate = tdate,
                            trtime = ttime,
                            skype = old_wreq.skype_request,
                            status = status,
                            participant_counts = participants_count,
                            created = created,
                            updated = created
                        )
                        break
                    except Exception, e:
                        #print 'sub2', e, 'id:', old_wreq.id
                        if i >= 149:
                            print 'i exceeded', 'id:', old_wreq.id
                        post_time = post_time + 5
        cursor = connection.cursor()
        cursor.execute("""update events_training set created='""" + str(created_str) + """', updated='""" + str(created_str) + """' where id=""" + str(new_wreq.id))
        try:
            dept = Department.objects.get(name = old_wreq.department)
            new_wreq.department.add(dept.id)
        except Exception, e:
            depts = get_dept(old_wreq.department)
            dept_list = depts.split(',')
            for deptrec in dept_list:
                try:
                    dept = Department.objects.get(name = deptrec)
                except:
                    continue
                new_wreq.department.add(dept.id)
    return HttpResponse("Success!")
