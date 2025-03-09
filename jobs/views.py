from django.http import JsonResponse
from rest_framework.decorators import api_view
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

@api_view(['POST'])
def match_jobs(request):

    user_skills = request.data.get("skills", [])
    jobs = request.data.get("jobs", [])

    if not user_skills or not jobs:
        return JsonResponse({"error": "Skills or Jobs missing"}, status=400)

 
    try:
        user_embedding = model.encode(", ".join(user_skills), convert_to_tensor=True)
    except Exception as e:
        return JsonResponse({"error": "Failed to process skills", "details": str(e)}, status=500)

    job_texts = [f"{job['title']} {', '.join(job['required_skills'])}" for job in jobs]
    job_embeddings = model.encode(job_texts, convert_to_tensor=True)


    similarities = util.pytorch_cos_sim(user_embedding, job_embeddings)[0].tolist()

    matched_job_ids = [job["id"] for job, _ in sorted(zip(jobs, similarities), key=lambda x: x[1], reverse=True)]

    return JsonResponse({"matched_jobs": matched_job_ids})
