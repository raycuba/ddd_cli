from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ValidationError

# Import entity-specific forms
from [[ app_name.lower() ]].[[ entity_name.lower() ]]_forms import [[ entity_name.capitalize() ]]Form, [[ entity_name.capitalize() ]]ViewForm, [[ entity_name.capitalize() ]]EditForm

# Import domain-specific services
from [[ app_name.lower() ]].domain.services import (
    create_[[ entity_name.lower() ]],
    retrieve_[[ entity_name.lower() ]],
    update_[[ entity_name.lower() ]],
    delete_[[ entity_name.lower() ]],
)

# Import infrastructure-specific repositories
from [[ app_name.lower() ]].infrastructure.[[ entity_name.lower() ]]_repository import [[ entity_name.capitalize() ]]Repository


def [[ entity_name.lower() ]]_list(request):
    """
    Generic view to display a list of all [[ entity_name.lower() ]] instances.
    """

    # Step 1: Get data from the repository
    repository = [[ entity_name.capitalize() ]]Repository()
    [[ entity_name.lower() ]]List = repository.get_all()

    # Step 2: Render the view with the data
    return render(request, '[[ app_name.lower() ]]/[[ entity_name.lower() ]]_list.html', {
        '[[ entity_name.lower() ]]List': [[ entity_name.lower() ]]List
    })


def [[ entity_name.lower() ]]_create(request):
    """
    Generic view to create a new [[ entity_name.lower() ]] instance using a service.
    """

    if request.method == "POST":

        # Step 1: Validate form data
        form = [[ entity_name.capitalize() ]]Form(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            repository = [[ entity_name.capitalize() ]]Repository()

            try:
                # Step 2: Call the creation service
                create_[[ entity_name.lower() ]](repository=repository, **form_data)

                # Step 3: Display success message and redirect
                messages.success(request, f"Successfully created [[ entity_name.lower() ]].")
                return redirect('[[ entity_name.lower() ]]_list')

            except ValidationError as e:
                # Handling domain-specific errors
                form.add_error(None, str(e))
        else:
            messages.error(request, "There were errors in the form. Please correct them.")
    else:
        # Empty form for GET requests
        form = [[ entity_name.capitalize() ]]Form()

    # Render the template with the form
    return render(request, '[[ app_name.lower() ]]/[[ entity_name.lower() ]]_create.html', {'form': form})


def [[ entity_name.lower() ]]_edit(request, id=None): 
    """
    Generic view to edit an existing [[ entity_name.lower() ]] instance.
    """
    if id is None:
        # Redirect if ID is not present
        return redirect('[[ entity_name.lower() ]]_list')

    repository = [[ entity_name.capitalize() ]]Repository()

    try:
        # Step 1: Obtain service data
        [[ entity_name.lower() ]] = retrieve_[[ entity_name.lower() ]](repository=repository, entity_id=id)

    except ValueError:
        # Handle case where the entity does not exist
        messages.error(request, f"The [[ entity_name.lower() ]] with ID {id} does not exist.")
        return redirect('[[ entity_name.lower() ]]_list')

    # Step 2: Initialize the form with the entity data
    form = [[ entity_name.capitalize() ]]EditForm(initial={
        'id': [[ entity_name.lower() ]].id,
        'title': [[ entity_name.lower() ]].title,
        'content': [[ entity_name.lower() ]].content,
        'public': [[ entity_name.lower() ]].public,
    })

    # Step 3: Render the template with the initialized form
    return render(request, '[[ app_name.lower() ]]/[[ entity_name.lower() ]]_edit.html', {'form': form})

    
def [[ entity_name.lower() ]]_save(request):
    """
    Generic view to save changes to an existing [[ entity_name.lower() ]] instance.
    """
    # Step 1: Retrieve the data submitted from the form
    id = request.POST.get('id')
    title = request.POST.get('title')
    content = request.POST.get('content')
    public = request.POST.get('public')

    repository = [[ entity_name.capitalize() ]]Repository()

    try:
        # Step 2: Call the service to update the entity with the provided data
        update_[[ entity_name.lower() ]](
            repository=repository,
            entity_id=id,
            title=title,
            content=content,
            public=public
        )

        # Step 3: Display a success message to the user
        messages.success(request, f"Successfully updated [[ entity_name.lower() ]]: {id} - {title}")

    except ValueError as e:
        # Handle errors related to business rules or validations
        messages.error(request, f"Error saving [[ entity_name.lower() ]]: {str(e)}")

    # Step 4: Redirect to the list of [[ entity_name.lower() ]]s
    return redirect('[[ entity_name.lower() ]]_list')


def [[ entity_name.lower() ]]_edit_save(request, id=None):
    """
    Generic view to edit an existing [[ entity_name.lower() ]] instance using a service.
    """
    if id is None:
        # Redirect if ID is not present
        return redirect('[[ entity_name.lower() ]]_list')

    repository = [[ entity_name.capitalize() ]]Repository()

    try:
        # Step 1: Obtain service data
        [[ entity_name.lower() ]] = retrieve_[[ entity_name.lower() ]](repository=repository, entity_id=id)

    except ValueError:
        # Handle case where the entity does not exist
        messages.error(request, f"The [[ entity_name.lower() ]] with ID {id} does not exist.")
        return redirect('[[ entity_name.lower() ]]_list')

    if request.method == "POST":

        # Step 2: Validate form data
        form = [[ entity_name.capitalize() ]]Form(request.POST)

        if form.is_valid():
            form_data = form.cleaned_data

            try:
                # Step 3: Call the update service
                update_[[ entity_name.lower() ]](repository=repository, entity_id=id, **form_data)

                # Step 4: Display success message and redirect
                messages.success(request, f"Successfully updated [[ entity_name.lower() ]].")
                return redirect('[[ entity_name.lower() ]]_list')

            except ValidationError as e:
                form.add_error(None, str(e))
        else:
            messages.error(request, "There were errors in the form. Please correct them.")

    else:
        # Initialize the form with existing data
        form = [[ entity_name.capitalize() ]]Form(initial={
            'title': [[ entity_name.lower() ]].title,
            'content': [[ entity_name.lower() ]].content,
            'public': [[ entity_name.lower() ]].public
        })

    # Render the template with the form
    return render(request, '[[ app_name.lower() ]]/[[ entity_name.lower() ]]_edit.html', {'form': form})


def [[ entity_name.lower() ]]_detail(request, id=None):
    """
    Generic view to display details of a specific [[ entity_name.lower() ]] instance.
    """
    if id is None:
        return redirect('[[ entity_name.lower() ]]_list')

    repository = [[ entity_name.capitalize() ]]Repository()
    try:
        # Get entity data from the service
        [[ entity_name.lower() ]] = retrieve_[[ entity_name.lower() ]](repository=repository, entity_id=id)

    except ValueError:
        messages.error(request, f"The [[ entity_name.lower() ]] with ID {id} does not exist.")
        return redirect('[[ entity_name.lower() ]]_list')

    # Render details with a read-only form
    form = [[ entity_name.capitalize() ]]ViewForm(initial={
        'title': [[ entity_name.lower() ]].title,
        'content': [[ entity_name.lower() ]].content,
        'public': [[ entity_name.lower() ]].public
    })

    return render(request, '[[ app_name.lower() ]]/[[ entity_name.lower() ]]_detail.html', {'form': form})


def [[ entity_name.lower() ]]_delete(request, id=None):
    """
    Generic view to delete an existing [[ entity_name.lower() ]] instance using a service.
    """
    if id is None:
        return redirect('[[ entity_name.lower() ]]_list')

    repository = [[ entity_name.capitalize() ]]Repository()
    try:
        # Call the disposal service
        delete_[[ entity_name.lower() ]](repository=repository, entity_id=id)
        messages.success(request, f"Successfully deleted [[ entity_name.lower() ]].")
        
    except ValueError:
        messages.error(request, f"The [[ entity_name.lower() ]] with ID {id} does not exist.")

    return redirect('[[ entity_name.lower() ]]_list')

