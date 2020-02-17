import os
import linecache

def distinct_tag():
    # with is like your try .. finally block in this case
    with open('templates//First_part.html', 'r') as file:
        # read a list of lines into data
        first_data = file.readlines()
    file.close()
    # with is like your try .. finally block in this case
    with open('templates//End_part.html', 'r') as file:
        # read a list of lines into data
        end_data = file.readlines()
    file.close()

    return first_data, end_data

def make_tag(username, first_part, end_part):
    #first part
    first_part.append('\t<div class="top-brands-login">\n')
    first_part.append('\t\t<div class="container">\n')
    first_part.append('\t\t\t<h3>فیلم های رنگی شده </h3>\n')
    #middle part
    str_list = []
    videoDirectory = os.listdir('static//UserColorizedVideos//' + username)
    if videoDirectory:
        count=0
        str_list.append('\t\t\t<div class="horizontal-scroll-wrapper squares">\n')
        for f in videoDirectory:
            count+=1
            str_list.append('\t\t\t\t<div>\n')
            str_list.append('\t\t\t\t\t<video id="video{}" controls width="200px" height="150px">\n'.format(count))
            str_list.append('\t\t\t\t\t\t<source id="vid{}" src="../static/ColorizedVideo.mp4" type="video/mp4">\n'.format(count))
            str_list.append('\t\t\t\t\t\t<script>\n')
            str_list.append('\t\t\t\t\t\t\tusername = document.getElementById("u1").innerHTML;\n')
            str_list.append('\t\t\t\t\t\t\tdocument.getElementById("vid{}").src = "../static/UserColorizedVideos/" + username + "/{}";\n'.format(count, f))
            str_list.append('\t\t\t\t\t\t</script>\n')
            str_list.append('\t\t\t\t\t\tYour browser does not support HTML5 video.\n')
            str_list.append('\t\t\t\t\t</video>\n')
            str_list.append('\t\t\t\t</div>\n')
        str_list.append('\t\t\t</div>\n')
    
    #end part
    firstEnd_part = []
    firstEnd_part.append('\t\t</div>\n')
    firstEnd_part.append('\t</div>\n')
    
    end_part = firstEnd_part + end_part
    # and write everything back
    with open('templates//indexlogin.html', 'w') as file:
        file.writelines(first_part + str_list + end_part)
    file.close()
    
