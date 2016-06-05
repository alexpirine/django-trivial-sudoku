# coding: utf-8
# Copyright (c) 2016, Alexandre Syenchuk (alexpirine), 2016

import itertools
import re
import sudokumaker

from django.contrib import messages
from django.shortcuts import render
from sudoku import SudokuProblem
from . import forms

# Create your views here.

def home(request):
    action = request.POST.get('action', None)
    suggest = request.GET.get('suggest', False)
    matrix = request.POST.getlist('matrix')
    solution = None

    solved = False

    initial_data = None
    if suggest:
        matrix = sudokumaker.make_problem()
        initial_data = [{'value': v or None} for k, v in enumerate(itertools.chain.from_iterable(matrix))]
    form = forms.SudokuForm(request.POST or None, initial=initial_data)

    if action == 'solve' and form.is_valid():
        user_data = [v['value'] or 0 for v in form.cleaned_data]
        matrix = [user_data[i:i+9] for i in xrange(0, len(user_data), 9)]
        problem = SudokuProblem(matrix)
        solution = problem.solve()
        if solution:
            initial_data = [{'value': v} for k, v in enumerate(itertools.chain.from_iterable(solution.matrix))]
            form = forms.SudokuForm(initial=initial_data)
            for k, f in enumerate(form):
                if not bool(user_data[k]):
                    f.fields['value'].widget.attrs['class'] += ' text-success'
                else:
                    f.fields['value'].widget.attrs['class'] += ' font-bold'
            solved = True

    c = {
        'action': action,
        'form': form,
        'solved': solved,
    }

    return render(request, 'home.html', c)
