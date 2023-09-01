from django.shortcuts import redirect,render
from django.contrib import messages
from app.models import Student,Student_notification,Student_Feedback,Student_Leave,Attendance,Student_Result,Attendance_Report,Subject


def HOME(request):
    return render(request,'Student/home.html')


def NOTIFICATIONS(request):
    student = Student.objects.filter(admin=request.user.id)
    for i in student:
        student_id = i.id

        notification = Student_notification.objects.filter(student_id=student_id)
        context = {
            'notification': notification,
        }
        return render(request,'Student/notification.html',context)


def STUDENT_NOTIFICAYION_MARK_DONE(request,status):
    notification = Student_notification.objects.get(id=status)
    notification.status = 1
    notification.save()
    return redirect('student_notification')


def STUDENT_FEEDBACK(request):
    student_id = Student.objects.get(admin=request.user.id)
    feedback_history = Student_Feedback.objects.filter(student_id=student_id)

    context = {
        'feedback_history':feedback_history,
    }
    return render(request,'Student/feedback.html',context)


def STUDENT_FEEDBACK_SAVE(request):
    if request.method == "POST":
        feedback = request.POST.get('feedback')
        student = Student.objects.get(admin=request.user.id)

        feedback = Student_Feedback(
            student_id=student,
            feedback=feedback,
            feedback_reply="",
        )
        feedback.save()
        messages.success(request,"Feedback Send Successfully")
    return redirect('student_feedback')


def STUDENT_APPLY_LEAVE(request):
    student = Student.objects.get(admin=request.user.id)
    student_leave_history = Student_Leave.objects.filter(student_id=student)

    context ={
        'student_leave_history':student_leave_history,
    }
    return render(request,'Student/apply_leave.html',context)


def STUDENT_LEAVE_SAVE(request):
    if request.method == "POST":
        leave_date = request.POST.get('leave_date')
        leave_message = request.POST.get('leave_message')
        student = Student.objects.get(admin=request.user.id)
        leave = Student_Leave(
            student_id=student,
            date=leave_date,
            message=leave_message,
        )
        leave.save()
        messages.success(request,'Leave Application Send Successfully')
    return redirect('student_apply_leave')


def STUDENT_VIEW_ATTENDANCE(request):
    student = Student.objects.get(admin=request.user.id)

    subjects = Subject.objects.filter(course=student.course_id)
    action = request.GET.get('action')

    get_subject = None
    attendance_report = None
    if action is not None:
        if request.method == "POST":
            subject_id = request.POST.get('subject_id')
            get_subject = Subject.objects.get(id=subject_id)
            attendance_report = Attendance_Report.objects.filter(student_id=student,attendance_id__subject_id=subject_id)
    context={
        'subjects':subjects,
        'action':action,
        'get_subject':get_subject,
        'attendance_report':attendance_report,
    }
    return render(request,'Student/view_attendance.html',context)


def VIEW_RESULT(request):
    mark = None
    student = Student.objects.get(admin=request.user.id)

    result = Student_Result.objects.filter(student_id=student)
    for i in result:
        assignment_mark = i.assignment_mark
        exam_mark = i.exam_mark

        mark =  assignment_mark + exam_mark
    context ={
        'result':result,
        'mark':mark,
    }
    return render(request,'Student/view_result.html',context)
