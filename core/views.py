from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
import csv
from io import TextIOWrapper

from .models import Category, Quiz, Question, Option, Attempt, Answer


@staff_member_required
def admin_manage_quizzes(request):
    quizzes = Quiz.objects.all()
    return render(request, 'core/admin_quizzes.html', {'quizzes': quizzes})

@staff_member_required
def admin_add_quiz(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'active')

        category = get_object_or_404(Category, id=category_id)

        Quiz.objects.create(title=title, category=category, status=status)
        messages.success(request, "Quiz added successfully.")
        return redirect('admin_manage_quizzes')

    return render(request, 'core/admin_add_quiz.html', {'categories': categories})

@staff_member_required
def admin_edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    categories = Category.objects.all()

    if request.method == 'POST':
        quiz.title = request.POST.get('title')
        category_id = request.POST.get('category')
        quiz.category = get_object_or_404(Category, id=category_id)
        quiz.status = request.POST.get('status', 'active')
        quiz.save()
        messages.success(request, "Quiz updated successfully.")
        return redirect('admin_manage_quizzes')

    return render(request, 'core/admin_edit_quiz.html', {'quiz': quiz, 'categories': categories})

@staff_member_required
def admin_delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    quiz.delete()
    messages.success(request, "Quiz deleted.")
    return redirect('admin_manage_quizzes')

@staff_member_required
def upload_quizzes_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        for row in reader:
            category_name = row.get('category', '').strip()
            if not category_name:
                continue
            category, _ = Category.objects.get_or_create(name=category_name)

            Quiz.objects.create(
                title=row.get('title', '').strip(),
                category=category,
                status=row.get('status', 'active').strip()
            )

        messages.success(request, "Quizzes uploaded successfully.")
        return redirect('admin_manage_quizzes')

    return render(request, 'core/admin_upload_quizzes.html')


@staff_member_required
def admin_manage_users(request):
    users = User.objects.all()
    return render(request, 'core/admin_users.html', {'users': users})

@staff_member_required
def admin_add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "User created successfully.")
        return redirect('admin_manage_users')
    return render(request, 'core/admin_add_user.html')

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, "User deleted.")
    return redirect('admin_manage_users')

@staff_member_required
def upload_users_csv(request):
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        file_data = TextIOWrapper(csv_file.file, encoding='utf-8')
        reader = csv.DictReader(file_data)

        for row in reader:
            username = row.get('username', '').strip()
            email = row.get('email', '').strip()
            password = row.get('password', '').strip()
            if not username:
                continue
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(username=username, email=email, password=password)

        messages.success(request, "Users uploaded successfully.")
        return redirect('admin_manage_users')

    return render(request, 'core/admin_upload_users.html')

@staff_member_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')

        if password:
            user.set_password(password)

        user.save()
        messages.success(request, "User updated successfully.")
        return redirect('admin_manage_users')

    return render(request, 'core/admin_edit_user.html', {'user': user})


@staff_member_required
def admin_dashboard(request):
    # Use the auth.User model and quiz/attempt counts
    context = {
        'total_users': User.objects.count(),
        'total_quizzes': Quiz.objects.count(),
        'total_attempts': Attempt.objects.count(),
        # annotate with the number of attempts per quiz; use the related_name 'attempts'
        'top_quizzes': Quiz.objects.annotate(
            attempt_count=Count('attempts')
        ).order_by('-attempt_count')[:5],
    }

    return render(request, 'core/admin_dashboard.html', context)


@login_required
def my_attempts(request):
    attempts = Attempt.objects.filter(user=request.user).order_by('-completed_at')
    return render(request, 'core/my_attempts.html', {'attempts': attempts})


@login_required
def quiz_result(request):
    score = request.session.get('score', 0)
    quiz_id = request.session.get('quiz_id')
    if quiz_id is None:
        messages.error(request, "No quiz in session.")
        return redirect('home')

    quiz = get_object_or_404(Quiz, pk=quiz_id)
    total_questions = quiz.questions.count()
    answers = request.session.get('answers', {})

    # Save attempt
    attempt = Attempt.objects.create(
        user=request.user,
        quiz=quiz,
        score=score,
        total=total_questions,
    )

    # Save each answer (session keys might be strings)
    for qid_str, oid in answers.items():
        try:
            qid = int(qid_str)
        except ValueError:
            continue
        question = Question.objects.filter(pk=qid).first()
        option = Option.objects.filter(pk=oid).first()
        if question and option:
            Answer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=option
            )

    # Clear session keys used for the quiz
    for key in ['score', 'quiz_id', 'question_index', 'answers']:
        request.session.pop(key, None)

    return render(request, 'core/quiz_result.html', {
        'score': score,
        'total_questions': total_questions,
        'quiz': quiz
    })


@login_required
def attempt_quiz(request):
    # quiz_id must already be in session (set by start_quiz)
    quiz_id = request.session.get('quiz_id')
    if quiz_id is None:
        messages.error(request, "Quiz not started.")
        return redirect('home')

    quiz = get_object_or_404(Quiz, pk=quiz_id)

    # ensure session keys exist
    question_index = request.session.get('question_index', 0)
    if 'answers' not in request.session:
        request.session['answers'] = {}
    if 'score' not in request.session:
        request.session['score'] = 0

    questions = list(quiz.questions.all())
    total = len(questions)
    if question_index >= total:
        return redirect('quiz_result')

    current_question = questions[question_index]
    options = current_question.options.all()

    if request.method == 'POST':
        selected_option_id = request.POST.get('option')
        if selected_option_id:
            try:
                selected_option = Option.objects.get(id=int(selected_option_id), question=current_question)
            except (Option.DoesNotExist, ValueError):
                selected_option = None

            # store user's answer in session (use question id as string)
            if selected_option:
                answers = request.session['answers']
                answers[str(current_question.id)] = selected_option.id
                request.session['answers'] = answers  # reassign to trigger session save

                # update score in session
                if selected_option.is_correct:
                    request.session['score'] = request.session.get('score', 0) + 1

        # Move to next question
        request.session['question_index'] = request.session.get('question_index', 0) + 1
        return redirect('attempt_quiz')

    return render(request, 'core/quiz_attempt.html', {
        'question': current_question,
        'options': options,
        'question_number': question_index + 1,
        'total_questions': total,
    })


@login_required
def start_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if quiz.status != 'active':
        messages.warning(request, "This quiz is not currently active.")
        return redirect('home')

    # Initialize session state for the quiz
    request.session['quiz_id'] = quiz.id
    request.session['question_index'] = 0
    request.session['score'] = 0
    request.session['answers'] = {}

    # redirect into the attempt flow which reads the session
    return redirect('attempt_quiz')


def category_quizzes(request, category_id):
    quizzes = Quiz.objects.filter(category_id=category_id)
    return render(request, 'core/quizzes_by_category.html', {'quizzes': quizzes})


def home(request):
    categories = Category.objects.all()
    return render(request, 'core/home.html', {'categories': categories})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request, 'core/login.html')


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        # Validate form
        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        # Save user (use create_user to ensure password is hashed and other fields initialized)
        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, 'core/register.html')
