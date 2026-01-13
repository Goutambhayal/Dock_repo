
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth import login
from .forms import UserRegistrationForm, UserLoginForm
from .models import CustomUser


# ----------------------- Registration -----------------------
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_email_verified = False  # mark email unverified until OTP
            user.save()

            # Generate OTP (this also sends email)
            otp = user.generate_otp()

            # Store user id in session for verification
            request.session['pending_user_id'] = user.id
            messages.info(request, "OTP sent to your email address.")
            return redirect('verify_otp')  # make sure this URL name exists
        return render(request, 'users/register.html', {'form': form})


# ----------------------- OTP Verification -----------------------
class VerifyOTPView(View):
    def get(self, request):
        return render(request, 'users/verify_otp.html')

    def post(self, request):
        otp_entered = request.POST.get("otp")
        user_id = request.session.get("pending_user_id")

        if not user_id:
            messages.error(request, "Session expired. Please register again.")
            return redirect('register')

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            messages.error(request, "Invalid user. Please register again.")
            return redirect('register')

        if user.verify_otp(otp_entered):
            login(request, user)
            messages.success(request, "Email verified successfully!")
            return redirect('home')
        else:
            messages.error(request, "Invalid OTP. Please try again.")
            return redirect('verify_otp')


# ----------------------- Login -----------------------
class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        return render(request, 'users/login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            remember = request.POST.get("remember_me")  # '1' if checked

            try:
                user = CustomUser.objects.get(username=username, email=email)
            except CustomUser.DoesNotExist:
                messages.error(request, "Invalid credentials.")
                return render(request, 'users/login.html', {'form': form})

            if not user.check_password(password):
                messages.error(request, "Invalid password.")
                return render(request, 'users/login.html', {'form': form})

            if not user.is_email_verified:
                messages.error(request, "Email not verified. Please verify your OTP.")
                request.session['pending_user_id'] = user.id
                return redirect('verify_otp')

            # login user
            login(request, user)
            if remember:
                # Keep session for SESSION_COOKIE_AGE (default 2 weeks or as set)
                request.session.set_expiry(None)   # None -> use global SESSION_COOKIE_AGE
                # or explicitly: request.session.set_expiry(60*60*24*30) for 30 days
            else:
                # Expire when the browser is closed
                request.session.set_expiry(0)
            messages.success(request, "Login successful!")
            return redirect('home')

        return render(request, 'users/login.html', {'form': form})
