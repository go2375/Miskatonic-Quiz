from app.database import get_quiz_collection

def add_question(question, responses, correct_responses, subjects, categories, created_by):
    doc = {
        "question": question,
        "all_responses": responses,
        "correct_responses": correct_responses,
        "subject": subjects,
        "use": categories,
        "created_by": created_by
    }
    get_quiz_collection().insert_one(doc)

def get_subjects():
    return get_quiz_collection().distinct("subject")

def get_categories():
    return get_quiz_collection().distinct("use")