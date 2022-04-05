from behave import given

@given('a german speaking user')
def given_english(context):
    context.lang = 'de-de'