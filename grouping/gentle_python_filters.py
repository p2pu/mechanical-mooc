from classphoto import models as classphoto_model

def filter_group_with_photo(x):
    conditions = [
        x['questions']['groupRadios'] == 'true',
        classphoto_model.has_bio(x['email'], x['sequence'])
    ]
    return all(conditions)


def filter_group_without_photo(x):
    conditions = [
        x['questions']['groupRadios'] == 'true',
        not classphoto_model.has_bio(x['email'], x['sequence'])
    ]
    return all(conditions)
