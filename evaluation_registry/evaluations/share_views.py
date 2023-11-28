from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from evaluation_registry.evaluations.forms import EvaluationCreateForm
from evaluation_registry.evaluations.models import (
    Department,
    Evaluation,
    EvaluationDepartmentAssociation,
)
from evaluation_registry.evaluations.views import (
    evaluation_type_view,
    evaluation_update_description,
)


@require_http_methods(["GET"])
def before_create_view(request):
    return render(request, "share-form/before-start.html")


@require_http_methods(["GET", "POST"])
def choose_evaluation_status_view(request):
    options = Evaluation.Status.choices
    if request.method == "GET":
        return render(request, "share-form/evaluation-status.html", {"options": options, "error": False})
    status = request.POST.get("status")
    if not status:
        return render(request, "share-form/evaluation-status.html", {"options": options, "error": True})
    return redirect("create", page_number=3, status=status)


@require_http_methods(["GET", "POST"])
def evaluation_create_view(request, status):
    errors = {}
    departments = Department.objects.all()
    if request.method == "POST":
        form = EvaluationCreateForm(request.POST)

        form_complete = request.POST.get("form_complete")
        selected_departments = request.POST.getlist("departments")
        selected_lead = request.POST.get("lead_department")
        department_to_remove = request.POST.get("remove_department")

        if form_complete:
            if form.is_valid():
                new_evaluation = form.save()
                EvaluationDepartmentAssociation.objects.create(
                    evaluation=new_evaluation, department=form.cleaned_data["lead_department"], is_lead=True
                )
                if form.cleaned_data["departments"]:
                    for department in form.cleaned_data["departments"]:
                        EvaluationDepartmentAssociation.objects.create(
                            evaluation=new_evaluation,
                            department=department,
                        )

                return redirect("share", uuid=new_evaluation.id, page_number=1)
            errors = form.errors.as_data()

        if department_to_remove and (department_to_remove in selected_departments):
            selected_departments.remove(department_to_remove)

        data = {
            "title": request.POST.get("title"),
            "lead_department": selected_lead,
            "departments": Department.objects.filter(code__in=selected_departments).all(),
        }

    else:
        # create a blank form
        form = EvaluationCreateForm()
        data = {"title": "", "lead_department": "", "departments": []}

    return render(
        request,
        "share-form/evaluation-create.html",
        {"form": form, "status": status, "departments": departments, "data": data, "errors": errors},
    )


@require_http_methods(["GET", "POST"])
def share_confirmation_view(request, evaluation, next_page):
    return render(request, "share-form/confirmation.html", {"evaluation": evaluation})


@require_http_methods(["GET", "POST"])
def create_view(request, page_number=1, status=None):
    if page_number == 1:
        return before_create_view(request)

    if page_number == 2:
        return choose_evaluation_status_view(request)

    if page_number == 3:
        if not status:
            return choose_evaluation_status_view(request)
        return evaluation_create_view(request, status=status)

    raise Http404("No page number %(verbose_name)s found" % {"verbose_name": page_number})


# MAKE SURE YOU ADD PARAM TO SHOW THIS IS SHARE VIEW
@require_http_methods(["GET", "POST"])
def share_view(request, uuid, page_number):
    try:
        evaluation = Evaluation.objects.get(id=uuid)
    except Evaluation.DoesNotExist:
        raise Http404("No %(verbose_name)s found matching the query" % {"verbose_name": Evaluation._meta.verbose_name})

    # TODO: add all of these
    view_options = [
        {
            "view": evaluation_type_view,
            "kwargs": {
                "parent": None,
            },
            "condition": True,
        },
        {
            "view": evaluation_type_view,
            "kwargs": {
                "parent": "impact",
            },
            "condition": evaluation.evaluation_design_types.filter(code="impact").exists(),
        },
        {
            "view": evaluation_type_view,
            "kwargs": {
                "parent": "rct",
            },
            "condition": evaluation.evaluation_design_types.filter(code="rct").exists(),
        },
        {
            "view": evaluation_update_description,
            "kwargs": {},
            "condition": True,
        },
        {
            "view": share_confirmation_view,
            "kwargs": {},
            "condition": True,
        },
    ]

    if (page_number) > len(view_options):
        raise Http404("No page number %(verbose_name)s found" % {"verbose_name": page_number})

    for i in range(page_number - 1, len(view_options)):
        view = view_options[i]
        view["kwargs"]["next_page"] = i + 2

        if view["condition"]:
            return view["view"](request, evaluation, **view["kwargs"])

    return redirect("evaluation-detail", uuid=evaluation.id)
