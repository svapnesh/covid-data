from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


def required_field_difference(required_field, optional_fields, parameters):
    """
    compare three list and returns the required field and not_needed fields
    :param required_field: the list of fields which required
    :param optional_fields: the list of fields which are optional
    :param parameters:
    :return: list
    """
    required_field_set = set(required_field)
    optional_fields_set = set(optional_fields)
    parameters_set = set(parameters)
    required = required_field_set.difference(parameters_set)
    not_needed = parameters_set.difference(required_field_set).difference(optional_fields_set)
    return list(required), list(not_needed)


def extra_fields_response(list_of_extra_fields):
    """
    generate the response for extra fields
    :param list_of_extra_fields: list_of_extra_fields
    :return: JSONResponse for extra fields
    """
    if len(list_of_extra_fields) == 1:
        return HttpResponse({'code': 0, 'response': {}, 'message': "{} field is {}".format(
            list_of_extra_fields[0], 'not needed')})
    else:
        extra_fields = ", ".join(list_of_extra_fields)
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} fields are {}".format(
            extra_fields, 'not needed')})


def missing_fields_response(list_of_missing_fields):
    """
    generate the response for missing fields
    :param list_of_missing_fields: list_of_missing_fields
    :return: JSONResponse for missing fields
    """
    if len(list_of_missing_fields) == 1:
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} field is {}".format(
            list_of_missing_fields[0], 'missing')})
    else:
        missing_fields = ", ".join(list_of_missing_fields)
        return JSONResponse({'code': 0, 'response': {}, 'message': "{} fields are {}".format(
            missing_fields, 'missing')})
