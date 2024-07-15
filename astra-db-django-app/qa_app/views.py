from django.shortcuts import render
from qa_app.models import TextQaVectors, Answers
from django.views.decorators.http import require_POST
from qa_app.question_answering import run_retrieval_qa_pipeline
from uuid import uuid4

# Create your views here.
def index(request):
    context = {'articles': TextQaVectors.objects.all()}
    return render(request, 'index.html', context)

@require_POST
def submit_question(request):
    prompt = request.POST.get('prompt')
    instructions = request.POST.get('qa-instructions')
    answer = run_retrieval_qa_pipeline(prompt, instructions)
    Answers.objects.create(row_id=uuid4(), question=prompt, answer=answer)
    context = {'question': prompt, 'answer': answer}
    return render(request, 'answer.html', context)