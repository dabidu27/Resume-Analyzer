from resume_analyzer.celery import app
from .models import ResumeAnalyzer
from .services.parse_pdf import PdfParser
from .services.analysis import ResumeAnalyzerTool


# the @shared_task decorator transforms this function into a celery background job
# bind = True will let us access attributes from the celeru job such as request retries, request id with self: self.request.retries, self.request.id
# autoretry_for = (Exception,) => the task is retried if any exception in the tuple occurs in the process of execution; we only have Exception in the tuple, meaning any exception
# retry_backoff = 5 => before 1st retry, wait 5 seconds, before the 2nd wait 10 seconds, before the 3rd wait 20 seconds
# retry_kwargs={"max_retries": 3} => only 3 retries


@app.task(bind=True)
def run_resume_analysis(self, analysis_id):

    analysis = ResumeAnalyzer.objects.get(id=analysis_id)
    analysis.status = "PROCESSING"
    analysis.save()

    pdfParser = PdfParser(analysis.resume_file)
    analysis.resume_text = pdfParser.extract_text()

    resumeAnalyzer = ResumeAnalyzerTool(analysis.resume_text, analysis.job_text)

    match_score, matched_keywords = resumeAnalyzer.analyze_resume()

    analysis.match_score = match_score
    analysis.matched_keywords = matched_keywords
    analysis.status = "COMPLETED"
    analysis.save()
