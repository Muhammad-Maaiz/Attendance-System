from datetime import datetime, time
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Employee, Attendance

def markattandence(request):
    message = ""
    if request.method == "POST":
        try:
            # Get the User object by ID
            user = User.objects.get(id=request.user.id)
            
            # Create or get the Employee object
            employee, created = Employee.objects.get_or_create(user=user)
            
            # Get the current local time, date, and day
            now = datetime.now()  # Get current local datetime
            current_time = now.time()  # Get the current time
            current_date = now.date()  # Get the current date
            current_day = now.strftime('%A')  # Get the current day
            
            # Define Group timings from 7:00 PM to 9:00 PM
            start_time = time(19, 0)  # 7:00 PM
            end_time = time(21, 0)  # 9:00 PM
            late_time = time(19, 10)  # 7:10 PM for fine
            absent_time = time(21, 10)  # 9:10 PM for marking absent

            # Check if attendance is too early
            if current_time < start_time:
                message = 'Attendance starts at 7:00 PM'
            
            # Check if attendance is late but before the end time
            elif current_time > late_time and current_time < absent_time:
                if Attendance.objects.filter(employee=employee, date=current_date).exists():
                    message = 'Attendance already marked for today'
                else:
                    employee.fine += 50  # Fine Rs 50 for late attendance
                    employee.save()
                    Attendance.objects.create(employee=employee, date=current_date, time=current_time, day=current_day, status='Late')
                    message = 'Attendance marked as late and fined Rs 50'

            # Check if attendance is after 9:10 PM (mark as absent and fine Rs 100)
            elif current_time > absent_time:
                if Attendance.objects.filter(employee=employee, date=current_date).exists():
                    message = 'Attendance already marked for today'
                else:
                    Attendance.objects.create(employee=employee, date=current_date, time=current_time, day=current_day, status='Absent')
                    employee.fine += 100  # Fine Rs 100 for being absent
                    employee.save()
                    message = 'You are marked absent and fined Rs 100'

            # Mark attendance as present
            else:
                if Attendance.objects.filter(employee=employee, date=current_date).exists():
                    message = 'Attendance already marked for today'
                else:
                    Attendance.objects.create(employee=employee, date=current_date, time=current_time, day=current_day, status='Present')
                    message = 'Attendance marked successfully'

        except Exception as e:
            print(f"Error: {e}")
            message = 'An error occurred while marking attendance.'

    return render(request, "attandence.html", {'message': message})