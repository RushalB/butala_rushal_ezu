from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.views import View

from courseinfo.forms import InstructorForm, StudentForm, SectionForm, CourseForm, RegistrationForm, SemesterForm
from courseinfo.models import Instructor, Student, Section, Course, Registration, Semester
from courseinfo.utils import ObjectCreateMixin


class SectionList(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_section'
    def get(self, request):
        return render(
            request,
            'courseinfo/section_list.html',
            {'section_list': Section.objects.all()}
        )


class SectionDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_section'
    def get(self, request, pk):
        section = get_object_or_404(
            Section,
            pk=pk,
        )
        semester = section.semester
        course = section.course
        instructor = section.instructor
        registration_list = section.registrations.all()
        return render(
            request,
            'courseinfo/section_detail.html',
            {'instructor': instructor,
             'course': course,
             'section': section,
             'semester': semester,
             'registration_list': registration_list
             }
        )


class InstructorList(LoginRequiredMixin,PermissionRequiredMixin,View):
    page_kwarg = 'page'
    paginate_by = 25;  # 25 instructors per page
    template_name = 'courseinfo/instructor_list.html'
    permission_required = 'courseinfo.view_instructor'

    def get(self, request):
        instructors = Instructor.objects.all()
        paginator = Paginator(
            instructors,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages)
        if page.has_previous():
            prev_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.previous_page_number())
        else:
            prev_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.next_page_number())
        else:
            next_url = None
        context = {
            'is_paginated':
                page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'instructor_list': page,
        }
        return render(
            request, self.template_name, context)


class InstructorDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_instructor'
    def get(self, request, pk):
        instructor = get_object_or_404(
            Instructor,
            pk=pk,
        )
        section_list = instructor.sections.all()
        return render(
            request,
            'courseinfo/instructor_detail.html',
            {'instructor': instructor, 'section_list': section_list}
        )


class InstructorCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin,View):
    form_class = InstructorForm
    template_name = 'courseinfo/instructor_form.html'
    permission_required = 'courseinfo.add_instructor'


class SectionCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin,View):
    form_class = SectionForm
    template_name = 'courseinfo/section_form.html'
    permission_required = 'courseinfo.add_section'


class CourseCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin,View):
    form_class = CourseForm
    template_name = 'courseinfo/course_form.html'
    permission_required = 'courseinfo.add_course'


class StudentCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin, View):
    form_class = StudentForm
    template_name = 'courseinfo/student_form.html'
    permission_required = 'courseinfo.add_student'


class RegistrationCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin, View):
    form_class = RegistrationForm
    template_name = 'courseinfo/registration_form.html'
    permission_required = 'courseinfo.add_registration'

class SemesterCreate(LoginRequiredMixin,PermissionRequiredMixin,ObjectCreateMixin, View):
    form_class = SemesterForm
    template_name = 'courseinfo/semester_form.html'
    permission_required = 'courseinfo.add_semester'


class StudentList(LoginRequiredMixin,PermissionRequiredMixin,View):
    page_kwarg = 'page'
    paginate_by = 25;  # 25 instructors per page
    template_name = 'courseinfo/student_list.html'
    permission_required = 'courseinfo.view_student'

    def get(self, request):
        students = Student.objects.all()
        paginator = Paginator(
            students,
            self.paginate_by
        )
        page_number = request.GET.get(
            self.page_kwarg
        )
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(
                paginator.num_pages)
        if page.has_previous():
            prev_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.previous_page_number())
        else:
            prev_url = None
        if page.has_next():
            next_url = "?{pkw}={n}".format(
                pkw=self.page_kwarg,
                n=page.next_page_number())
        else:
            next_url = None
        context = {
            'is_paginated':
                page.has_other_pages(),
            'next_page_url': next_url,
            'paginator': paginator,
            'previous_page_url': prev_url,
            'student_list': page,
        }
        return render(
            request, self.template_name, context)


class StudentDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_student'
    def get(self, request, pk):
        student = get_object_or_404(
            Student,
            pk=pk,
        )
        registration_list = student.registrations.all()
        return render(
            request,
            'courseinfo/student_detail.html',
            {'student': student,
             'registration_list': registration_list
             }
        )


class RegistrationList(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_registration'
    def get(self, request):
        return render(
            request,
            'courseinfo/registration_list.html',
            {'registration_list': Registration.objects.all()}
        )


class RegistrationDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_registration'
    def get(self, request, pk):
        registration = get_object_or_404(
            Registration,
            pk=pk,
        )
        student = registration.student
        section = registration.section
        return render(
            request,
            'courseinfo/registration_detail.html',
            {'registration': registration,
             'section': section,
             'student': student,
             }
        )


class CourseList(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_course'
    def get(self, request):
        return render(
            request,
            'courseinfo/course_list.html',
            {'course_list': Course.objects.all()}
        )
        # section_list = instructor.sections.all()
        # return render(
        #     request,
        #     'courseinfo/instructor_detail.html',
        #     {'instructor': instructor, 'section_list': section_list}
        # )


class CourseDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_course'
    def get(self, request, pk):
        course = get_object_or_404(
            Course,
            pk=pk,
        )
        section_list = course.sections.all()
        return render(
            request,
            'courseinfo/course_detail.html',
            {'course': course, 'section_list': section_list}
        )


class SemesterList(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_semester'
    def get(self, request):
        return render(
            request,
            'courseinfo/semester_list.html',
            {'semester_list': Semester.objects.all()}
        )


class SemesterDetail(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.view_semester'
    def get(self, request, pk):
        semester = get_object_or_404(
            Semester,
            pk=pk,
        )
        section_list = semester.sections.all()
        return render(
            request,
            'courseinfo/semester_detail.html',
            {'semester': semester, 'section_list': section_list}
        )
# def student_list_view(request):
#     student_list = Student.objects.all()
#     return render(request, "courseinfo/student_list.html", {'student_list': student_list})
# def instructor_list_view(request):
#     instructor_list = Instructor.objects.all()
#     # instructor_list = Instructor.objects.none()
#     return render(request, "courseinfo/instructor_list.html", {'instructor_list': instructor_list})
# def sections_list_view(request):
#     section_list = Section.objects.all()
#     # section_list = Section.objects.none()
#     return render(request, "courseinfo/section_list.html", {'section_list': section_list})
# def registration_list_view(request):
#     registration_list = Registration.objects.all()
#     return render(request, "courseinfo/registration_list.html", {'registration_list': registration_list})
# def courses_list_view(request):
#     course_list = Course.objects.all()
#     return render(request, "courseinfo/course_list.html", {'course_list': course_list})
# def semesters_list_view(request):
#     semester_list = Semester.objects.all()
#     return render(request, "courseinfo/semester_list.html", {'semester_list': semester_list})


class InstructorUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_instructor'
    form_class = InstructorForm
    model = Instructor
    template_name = 'courseinfo/instructor_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        instructor = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=instructor),
            'instructor': instructor,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        instructor = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=instructor)
        if bound_form.is_valid():
            new_instructor = bound_form.save()
            return redirect(new_instructor)
        else:
            context = {
                'form': bound_form,
                'instructor': instructor,
            }
            return render(
                request,
                self.template_name,
                context)


class SectionUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_section'
    form_class = SectionForm
    model = Section
    template_name = 'courseinfo/section_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        section = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=section),
            'section': section,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        section = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=section)
        if bound_form.is_valid():
            new_section = bound_form.save()
            return redirect(new_section)
        else:
            context = {
                'form': bound_form,
                'section': section,
            }
            return render(
                request,
                self.template_name,
                context)


class StudentUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_student'
    form_class = StudentForm
    model = Student
    template_name = 'courseinfo/student_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        student = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=student),
            'student': student,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        student = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=student)
        if bound_form.is_valid():
            new_student = bound_form.save()
            return redirect(new_student)
        else:
            context = {
                'form': bound_form,
                'student': student,
            }
            return render(
                request,
                self.template_name,
                context)


class RegistrationUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_registration'
    form_class = RegistrationForm
    model = Registration
    template_name = 'courseinfo/registration_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        registration = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=registration),
            'registration': registration,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        registration = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=registration)
        if bound_form.is_valid():
            new_registration = bound_form.save()
            return redirect(new_registration)
        else:
            context = {
                'form': bound_form,
                'registration': registration,
            }
            return render(
                request,
                self.template_name,
                context)


class SemesterUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_semester'
    form_class = SemesterForm
    model = Semester
    template_name = 'courseinfo/semester_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        semester = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=semester),
            'semester': semester,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        semester = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=semester)
        if bound_form.is_valid():
            new_semester = bound_form.save()
            return redirect(new_semester)
        else:
            context = {
                'form': bound_form,
                'semester': semester,
            }
            return render(
                request,
                self.template_name,
                context)


class CourseUpdate(LoginRequiredMixin,PermissionRequiredMixin,View):
    permission_required = 'courseinfo.change_course'
    form_class = CourseForm
    model = Course
    template_name = 'courseinfo/course_form_update.html'

    def get_object(self, pk):
        return get_object_or_404(
            self.model,
            pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        context = {
            'form': self.form_class(
                instance=course),
            'course': course,
        }
        return render(
            request, self.template_name, context)

    def post(self, request, pk):
        course = self.get_object(pk)
        bound_form = self.form_class(
            request.POST, instance=course)
        if bound_form.is_valid():
            new_course = bound_form.save()
            return redirect(new_course)
        else:
            context = {
                'form': bound_form,
                'course': course,
            }
            return render(
                request,
                self.template_name,
                context)





