from django.http import HttpResponse, Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import UploadFileForm
import json
import copy

# views functions

'''
Renders the landing page for the app
in case of GET request it show a form.
in case of POST request it tries to handle the request and render it otherwise redirect to error page.
'''
def home(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        user_file = request.FILES['linux_file']
        if (user_file.size > 10000000):
            return redirect('/error')
        with open('temp_user_file', 'wb+') as destination:
            for chunk in user_file.chunks():
                destination.write(chunk)
            try:
                data = open('temp_user_file', 'r')
                user_file_data = data.readlines()
                output = extract(another=user_file_data)
                return render(request, 'packages/user.html', {'jsonfile': output, 'title': 'All Packages'})
            except:
                return redirect('/error#badInput')
    else:
        form = UploadFileForm()
        return render(request, 'packages/home.html', {'form': form})


'''
This is a view function that shows the main page for a sample file where it lists all the packages.
'''

def show(request):
    jsonoutput = extract(
        'status.real')
    return render(request, 'packages/show.html', {'jsonfile': jsonoutput, 'title': 'All Packages'})


'''
This is a view function that return a specific package page for the sample file.
'''


def show_package(request, package_name):
    jsonoutput = extract(
        'status.real')
    package = get_package_by_name(jsonoutput, package_name)
    return render(request, 'packages/package.html', {'package': package, 'title': package["PackagName"]})

#about page view
def about(request):
    return render(request, 'packages/about.html')


'''
This function shows the packages that the user uploaded, there is only possibility to see last upload of the user
'''

def show_package_user(request, package_name):
    try:
        jsonoutput = extract('temp_user_file')
        package = get_package_by_name(jsonoutput, package_name)
        return render(request, 'packages/package_user.html', {'package': package, 'title': package["PackagName"]})
    except:
        return redirect('/error#fileDoesNotExist')


'''
Render all packages from the latest valid file that any user uploaded.
'''
def show_all_package_user(request):
    try:
        jsonoutput = extract('temp_user_file')
        return render(request, 'packages/user.html', {'jsonfile': jsonoutput, 'title': 'All Packages'})
    except:
        return redirect('/error#fileDoesNotExist')


#view for error page
def error(request):
    return render(request, 'packages/error.html')



# helper functions.
'''
Returns a certain package from the big packgage list.
'''
def get_package_by_name(packages, package_name):
    for package in packages:
        if package["PackagName"] == package_name:
            return {"PackagName": package["PackagName"],
                    "dependencies": package["dependencies"],
                    "Description": package["Description"],
                    "dependants": package["dependants"]}


'''
This function reads the file and loops through it to extract the needed info.
it return a list that contains all the packages
'''
def extract(inputfile='status.real', another=None):
    if another is None:
        f = open(inputfile, 'r')
        data = f.readlines()
    else:
        data = another
    output = []
    obj = {"PackagName": "", "dependencies": 'None', "Description": ""}
    for line in data:
        if "Package" in line:
            obj["PackagName"] = check_and_clean_name(
                line.rstrip().split(" ")[-1])
        elif "Depends:" in line:
            obj["dependencies"] = check_and_clean_list_names(
                line.replace(' ', '').split(":")[1].split(","))
        elif "Description:" in line:
            obj["Description"] = line.rstrip().split(":")[-1]
        elif line.startswith(" "):
            obj["Description"] = obj["Description"] + line
        elif not line.strip():
            output.append(copy.deepcopy(obj))
    packages = add_dep(output)
    PackagesList = sort_remove_duplicates(packages)
    return PackagesList


'''
This Function looks for all the packages that is depended on a certain package
paramters: 
packagename: the package to find if it is a depency in other packages
package_list: a list with all the packages
Returns a list with the packages that depends on the given package
'''
def find_dep(packagename, package_list):
    dep_list = []
    for package in package_list:
        if packagename["PackagName"] in package["dependencies"]:
            dep_list.append(package["PackagName"])
    return dep_list


'''
This Function adds a field for the packages to show which packages are depends on this package. 
returns a the packages with a new field called dependants. 
'''
def add_dep(packages):
    for package in packages:
        reverse_dep = find_dep(package, packages)
        if reverse_dep:
            package["dependants"] = reverse_dep
        else:
            package["dependants"] = "None"
    return packages


'''
This function removes the versioning at the end of the package name
'''
def check_and_clean_name(name):
    return name[:name.find("(")] if name.find("(") > -1 else name


'''
This function utilizes check_and_clean_name function for a list 
it also makes sure that there is no duplicates in the list
'''
def check_and_clean_list_names(namelist):
    cleaned = []
    for name in namelist:
        cleaned_name = check_and_clean_name(name)
        if cleaned_name not in cleaned:
            cleaned.append(cleaned_name)
    return cleaned



def sort_remove_duplicates(packages):
    seen = set()
    updated_packages = []
    x= 0
    for package in packages:
        Pname = package["PackagName"]
        if Pname not in seen:
            seen.add(Pname)
            updated_packages.append(package)
    sortedPackage = sorted(updated_packages, key=lambda i: i["PackagName"])
    return sortedPackage
