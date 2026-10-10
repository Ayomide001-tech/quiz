from django.urls import path
from .views import (
    dashboard,
    homepage,
    superuserpage,
    adminpage,
    create_categories_api,
    create_categories_page,
    category_questions,
    viewaddedquestion,
    create_question,
    create_question_api,
    save_score,
    viewScores,
    display_questions,
    download_question_template,
    import_questions_from_excel,
    upload_questions,
    categoryDeleteView,
    categoryUpdateView,
    QuestionDeleteView,
    QuestionUpdateView,
    generate_questions_with_ai,
    category_question_with_ai,


    
    

    

)

urlpatterns = [
    path('dashboard/', dashboard, name ='dashboard'),
    path('homepage/', homepage, name ='homepage'),
    path('superuserpage/', superuserpage, name ='superuserpage'),
    path('adminpage/', adminpage, name ='adminpage'),
    path('create_categories_api/', create_categories_api, name ='create_categories_api'),
    path('create_categories_page/', create_categories_page, name ='create_categories_page'),
    path('create_question/', create_question, name ='create_question'),
    path('create_question_api/', create_question_api, name ='create_question_api'),
    path('category/<int:category_id>/', category_questions, name='category_questions'),
    path('viewaddedquestion/', viewaddedquestion, name ='viewaddedquestion'),
    path('display_questions/<int:categorys_id>/', display_questions, name ='display_questions'),
    path('save_score/', save_score, name ='save_score'),
    path('viewScores/', viewScores, name ='viewScores'),
    path('download_question_template/', download_question_template, name ='download_question_template'),
    path('import_questions_from_excel/', import_questions_from_excel, name ='import_questions_from_excel'),
    path('upload_questions/', upload_questions, name ='upload_questions'),
    path("category/<int:pk>/update/", categoryUpdateView.as_view(), name="category_update"),
    path("category/<int:pk>/delete/", categoryDeleteView.as_view(), name="category_delete"),
    path("question/<int:pk>/update/", QuestionUpdateView.as_view(), name="question_update"),
    path("question/<int:pk>/delete/", QuestionDeleteView.as_view(), name="question_delete"),
    path('generate-questions/', generate_questions_with_ai, name='generate_questions'),
    path('category-with-ai/', category_question_with_ai, name='category_with_ai'),

    
     

]   
   
